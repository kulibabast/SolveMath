from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

model_path = os.environ.get('MODEL_PATH')
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")


def generate_response(input_text, max_length=100, temperature=0.7):
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to('cpu')
    output = model.generate(
        input_ids,
        max_length=max_length,
        temperature=temperature,
        pad_token_id=tokenizer.eos_token_id,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        top_k=5,
        top_p=0.95,
        eos_token_id=tokenizer.eos_token_id,
        early_stopping=True
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)
