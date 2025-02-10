import torch
import transformers

# model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
model_id = "meta-llama/Llama-2-13b-chat-hf"

system_prompt = '''
	For each given words, please create one example sentence in Chinese.
	Your sentence should be easy to understand and useful for students to learn.
	'''

pipeline = transformers.pipeline("text-generation",
	model=model_id, model_kwargs={"torch_dtype": torch.bfloat16},
	device_map="auto")

words = "馒头, 米饭"
output = pipeline(system_prompt + ' ' + words)
print(output)
breakpoint()
