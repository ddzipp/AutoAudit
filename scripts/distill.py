from openai import OpenAI
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time

client = OpenAI(
    api_key="",
    base_url="",
)


def query(prompt):
    completion = client.chat.completions.create(
        model="deepseek-r1",
        messages=[
            {'role': 'user', 'content': prompt}],
    )
    answer = completion.choices[0].message.content
    reason_content = completion.choices[0].message.reasoning_content
    print(answer)
    return answer, reason_content


def process_content(content, num_threads=2):
    time.sleep(0.5)
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        return list(tqdm(executor.map(query, content), total=len(content), desc="Processing"))


def query_stream(prompt):
    reasoning_content = ""
    answer_content = ""
    is_answering = False

    completion = client.chat.completions.create(
        model="deepseek-r1", 
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    # 逐步获取流式响应
    for chunk in completion:
        if not chunk.choices:
            continue  
        delta = chunk.choices[0].delta

        # 处理推理过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content and not is_answering:
                is_answering = True
            # 拼接回复内容
            if delta.content:
                answer_content += delta.content

    return answer_content, reasoning_content

def process_content_stream(content_batch, num_threads=2):
    time.sleep(0.5)
    responses = []
    reasoning_contents = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for response, reasoning in tqdm(executor.map(query_stream, content_batch), total=len(content_batch), desc="Processing"):
            responses.append(response)
            reasoning_contents.append(reasoning)
    
    return responses, reasoning_contents

df = pd.read_csv("./filtered_file.csv")
questions = df['processed_content'] 
questions = df['questions'] 
print(f"Number of questions: {len(questions)}")

batch_size = 10 
total_batches = len(questions) // batch_size + (1 if len(questions) % batch_size != 0 else 0)  

for i in range(total_batches):
    start_idx = i * batch_size
    end_idx = min((i + 1) * batch_size, len(questions))  
    current_batch = questions[start_idx:end_idx]

    try:
        responses, reasoning_contents = process_content_stream(current_batch, num_threads=2)

        df_batch = pd.DataFrame({
            'processed_content': current_batch,
            'response': responses,
            'reason_content': reasoning_contents
        })

        df_batch.to_csv(f'retry_distilled_questions_batch_{i + 1}.csv', index=False)
        print(f"Batch {i + 1} saved.")
    
    except Exception as e:
        print(f"Error processing batch {i + 1}: {e}")
        with open("failed_batches.txt", "a") as f:
            f.write(f"Batch {i + 1} failed. Error: {str(e)}\n")

print("All batches processed and saved.")

# Retry failed batches
# failed_batches = []
# with open("failed_batches.txt", "r") as f:
#     for line in f:
#         if "Batch" in line:
#             batch_number = int(line.split()[1])  # 提取批次号
#             failed_batches.append(batch_number)

# print(f"Failed batches: {failed_batches}")
# df = pd.read_csv("./filtered_file.csv")
# questions = df['processed_content']
# batch_size = 10
# total_batches = len(questions) // batch_size + (1 if len(questions) % batch_size != 0 else 0)

# for i in failed_batches:
#     # 重新执行失败的批次
#     start_idx = (i - 1) * batch_size  # 注意：failed_batches中的批次号是从1开始的
#     end_idx = min(i * batch_size, len(questions))  
#     current_batch = questions[start_idx:end_idx]

#     try:
#         responses, reasoning_contents = process_content_stream(current_batch, num_threads=2)

#         df_batch = pd.DataFrame({
#             'processed_content': current_batch,
#             'response': responses,
#             'reason_content': reasoning_contents
#         })

#         df_batch.to_csv(f'retry_distilled_questions_batch_{i}.csv', index=False)
#         print(f"Batch {i} saved.")

#     except Exception as e:
#         print(f"Error reprocessing batch {i}: {e}")
#         with open("failed_batches.txt", "a") as f:
#             f.write(f"Batch {i} failed again. Error: {str(e)}\n")

# print("Failed batches reprocessed.")