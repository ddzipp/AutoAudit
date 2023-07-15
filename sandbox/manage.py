#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

example_result = "1. analysis: The given XSS statement is a closing </span> tag. It is used to close an opening <span> tag in an HTML document.\n2. label: Low\n3. risk: The given statement does not pose any security risk as it is a standard closing tag and does not contain any user-controllable inputs or dynamically generated content."
encoding_name = "cl100k_base"
# encooding_name = "gpt-3.5-turbo"
version = "0.0.1"
# prompter = None
# tokenizer = None

import os
import sys
import time
import re

import fire
import gradio as gr
import torch
import transformers
from peft import PeftModel
from transformers import GenerationConfig, LlamaForCausalLM, LlamaTokenizer

# sys.path.append("/root/autodl-tmp/alpaca-lora/utils")
from utils.callbacks import Iteratorize, Stream
from utils.prompter import Prompter
# from callbacks import Iteratorize, Stream
# from prompter import Prompter



'''
if torch.cuda.is_available():
    device = "cuda"
    print("using cude")
else:
    device = "cpu"
    print("using cpu")
try:
    if torch.backends.mps.is_available():
        device = "mps"
        print("using mps")
except:  # noqa: E722
    pass

def main_alpaca(
load_8bit = True,
base_model = "yahma/llama-7b-hf",
lora_weights = "model_20230703_attempt1",
prompt_template = "",  # The prompt template to use, will default to alpaca.
server_name = "0.0.0.0",  # Allows to listen on all interfaces by providing '0.
    share_gradio = False,):
    version = base_model + lora_weights

    base_model = base_model or os.environ.get("BASE_MODEL", "")
    assert (
        base_model
    ), "Please specify a --base_model, e.g. --base_model='huggyllama/llama-7b'"

    global prompter
    global tokenizer
    prompter = Prompter(prompt_template) # changed 7/12

    device_map = "auto"
    world_size = int(os.environ.get("WORLD_SIZE", 1))
    ddp = world_size != 1
    if ddp:
        device_map = {"": int(os.environ.get("LOCAL_RANK") or 0)}
    print("device_map: ", device_map)
    # tokenizer = LlamaTokenizer.from_pretrained(base_model)
    tokenizer = LlamaTokenizer.from_pretrained(base_model, device_map={'': 0}) # add gloabl
    if device == "cuda":
        model = LlamaForCausalLM.from_pretrained(
            base_model,
            load_in_8bit=load_8bit,
            torch_dtype=torch.float16,
            # device_map="auto",
            # device_map=device_map,
            device_map={'': 0}
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            torch_dtype=torch.float16,
            device_map={"": 0}  # add in 0704
            # device_map=device_map
        )
    elif device == "mps":
        model = LlamaForCausalLM.from_pretrained(
            base_model,
            device_map={"": device},
            torch_dtype=torch.float16,
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            device_map={"": device},
            torch_dtype=torch.float16,
        )
    else:
        model = LlamaForCausalLM.from_pretrained(
            base_model, device_map={"": device}, low_cpu_mem_usage=True
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            device_map={"": device},
        )

    # unwind broken decapoda-research config
    model.config.pad_token_id = tokenizer.pad_token_id = 0  # unk
    model.config.bos_token_id = 1
    model.config.eos_token_id = 2

    if not load_8bit:
        model.half()  # seems to fix bugs for some users.

    model.eval()
    if torch.__version__ >= "2" and sys.platform != "win32":
        model = torch.compile(model)
    
def evaluate(
    instruction=None,
    input=None,
    temperature=0.1,
    top_p=0.75,
    top_k=40,
    num_beams=4,
    max_new_tokens=512,
    stream_output=False,
    prompter = None,
    tokenizer = None,
    **kwargs,
):
    # global prompter
    # global tokenizer
    prompt = prompter.generate_prompt(instruction, input)
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"].to(device)
    generation_config = GenerationConfig(
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        num_beams=num_beams,
        **kwargs,
    )

    generate_params = {
        "input_ids": input_ids,
        "generation_config": generation_config,
        "return_dict_in_generate": True,
        "output_scores": True,
        "max_new_tokens": max_new_tokens,
    }

    if stream_output:
        # Stream the reply 1 token at a time.
        # This is based on the trick of using 'stopping_criteria' to create an iterator,
        # from https://github.com/oobabooga/text-generation-webui/blob/ad37f396fc8bcbab90e11ecf17c56c97bfbd4a9c/modules/text_generation.py#L216-L243.

        def generate_with_callback(callback=None, **kwargs):
            kwargs.setdefault(
                "stopping_criteria", transformers.StoppingCriteriaList()
            )
            kwargs["stopping_criteria"].append(
                Stream(callback_func=callback)
            )
            with torch.no_grad():
                model.generate(**kwargs)

        def generate_with_streaming(**kwargs):
            return Iteratorize(
                generate_with_callback, kwargs, callback=None
            )

        with generate_with_streaming(**generate_params) as generator:
            for output in generator:
                # new_tokens = len(output) - len(input_ids[0])
                decoded_output = tokenizer.decode(output)

                if output[-1] in [tokenizer.eos_token_id]:
                    break

                yield prompter.get_response(decoded_output)
        return  # early return for stream_output

    # Without streaming
    with torch.no_grad():
        generation_output = model.generate(
            input_ids=input_ids,
            generation_config=generation_config,
            return_dict_in_generate=True,
            output_scores=True,
            max_new_tokens=max_new_tokens,
        )
    s = generation_output.sequences[0]
    output = tokenizer.decode(s)
    yield prompter.get_response(output)
    
    # yield example_result
'''

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SandBox.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    '''fire.Fire(main_alpaca)
    if prompter != None and tokenizer != None:
        print("prompter and tokenizer is not None")
        print(prompter)
        print(tokenizer)
    else:
        print("Is None")
    '''
    main()
