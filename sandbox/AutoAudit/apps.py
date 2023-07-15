import os
import sys

import torch
import transformers
from django.apps import AppConfig
from peft import PeftModel
from transformers import GenerationConfig, LlamaForCausalLM, LlamaTokenizer
# sys.path.append("/root/autodl-tmp/alpaca-lora/utils")
from utils.callbacks import Iteratorize, Stream
from utils.prompter import Prompter


# from callbacks import Iteratorize, Stream
# from prompter import Prompter


class AutoauditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AutoAudit'
    prompter = None
    tokenizer = None
    device = None
    model = None
    count = 7860

    def evaluate(
            self,
            instruction="Analyze this statement and determine whether it contains security risk",
            input=None,
            temperature=0.1,
            top_p=0.75,
            top_k=40,
            num_beams=4,
            max_new_tokens=512,
            stream_output=False,
            **kwargs,
    ):
        # global prompter
        # global tokenizer
        prompt = AutoauditConfig.prompter.generate_prompt(instruction, input)
        inputs = AutoauditConfig.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(AutoauditConfig.device)
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
                    AutoauditConfig.model.generate(**kwargs)

            def generate_with_streaming(**kwargs):
                return Iteratorize(
                    generate_with_callback, kwargs, callback=None
                )

            with generate_with_streaming(**generate_params) as generator:
                for output in generator:
                    # new_tokens = len(output) - len(input_ids[0])
                    decoded_output = AutoauditConfig.tokenizer.decode(output)

                    if output[-1] in [AutoauditConfig.tokenizer.eos_token_id]:
                        break

                    yield AutoauditConfig.prompter.get_response(decoded_output)
            return  # early return for stream_output

        # Without streaming
        with torch.no_grad():
            generation_output = AutoauditConfig.model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
            )
        s = generation_output.sequences[0]
        output = AutoauditConfig.tokenizer.decode(s)
        yield AutoauditConfig.prompter.get_response(output)

    def ready(self):
        def main_alpaca():
            '''
            load_8bit = True,
            base_model = "yahma/llama-7b-hf",
            lora_weights = "model_20230703_attempt2",
            prompt_template = "",  # The prompt template to use, will default to alpaca.
            server_name = "0.0.0.0",  # Allows to listen on all interfaces by providing '0.
            share_gradio = False,'''
            load_8bit = True;
            base_model = "yahma/llama-7b-hf";
            lora_weights = "model_20230703_attempt2";
            prompt_template = "";  # The prompt template to use, will default to alpaca.
            server_name = "0.0.0.0";  # Allows to listen on all interfaces by providing '0.
            share_gradio = False;

            if torch.cuda.is_available():
                AutoauditConfig.device = "cuda"
                print("using cude")
            else:
                AutoauditConfig.device = "cpu"
                print("using cpu")
            try:
                if torch.backends.mps.is_available():
                    AutoauditConfig.device = "mps"
                    print("using mps")
            except:  # noqa: E722
                pass

            version = base_model + lora_weights

            base_model = base_model or os.environ.get("BASE_MODEL", "")
            assert (
                base_model
            ), "Please specify a --base_model, e.g. --base_model='huggyllama/llama-7b'"

            AutoauditConfig.prompter = Prompter(prompt_template)  # changed 7/12

            device_map = "auto"
            world_size = int(os.environ.get("WORLD_SIZE", 1))
            ddp = world_size != 1
            if ddp:
                device_map = {"": int(os.environ.get("LOCAL_RANK") or 0)}
            print("device_map: ", device_map)
            # tokenizer = LlamaTokenizer.from_pretrained(base_model)
            AutoauditConfig.tokenizer = LlamaTokenizer.from_pretrained(base_model, device_map={'': 0})  # add gloabl
            if AutoauditConfig.device == "cuda":
                AutoauditConfig.model = LlamaForCausalLM.from_pretrained(
                    base_model,
                    load_in_8bit=load_8bit,
                    torch_dtype=torch.float16,
                    # device_map="auto",
                    # device_map=device_map,
                    device_map={'': 0}
                )
                AutoauditConfig.model = PeftModel.from_pretrained(
                    AutoauditConfig.model,
                    lora_weights,
                    torch_dtype=torch.float16,
                    device_map={"": 0}  # add in 0704
                    # device_map=device_map
                )
            elif AutoauditConfig.device == "mps":
                AutoauditConfig.model = LlamaForCausalLM.from_pretrained(
                    base_model,
                    device_map={"": AutoauditConfig.device},
                    torch_dtype=torch.float16,
                )
                AutoauditConfig.model = PeftModel.from_pretrained(
                    AutoauditConfig.model,
                    lora_weights,
                    device_map={"": AutoauditConfig.device},
                    torch_dtype=torch.float16,
                )
            else:
                AutoauditConfig.model = LlamaForCausalLM.from_pretrained(
                    base_model, device_map={"": AutoauditConfig.device}, low_cpu_mem_usage=True
                )
                AutoauditConfig.model = PeftModel.from_pretrained(
                    AutoauditConfig.model,
                    lora_weights,
                    device_map={"": AutoauditConfig.device},
                )

            # unwind broken decapoda-research config
            AutoauditConfig.model.config.pad_token_id = AutoauditConfig.tokenizer.pad_token_id = 0  # unk
            AutoauditConfig.model.config.bos_token_id = 1
            AutoauditConfig.model.config.eos_token_id = 2

            if not load_8bit:
                AutoauditConfig.model.half()  # seems to fix bugs for some users.

            AutoauditConfig.model.eval()
            if torch.__version__ >= "2" and sys.platform != "win32":
                AutoauditConfig.model = torch.compile(AutoauditConfig.model)

        # fire.Fire(main_alpaca)
        main_alpaca()
