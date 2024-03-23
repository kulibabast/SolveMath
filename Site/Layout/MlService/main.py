from transformers import GPT2LMHeadModel, GPT2Tokenizer, BertTokenizer,\
                         BertTokenizerFast, BertForSequenceClassification
import torch
from env import MODEL_GPT_PATH, MODEL_THEORY_PATH, MODEL_TOPIC_PATH
from models import BERTClass, transcript_theory


NUM_LABELS = 8
ID2LABEL = {
            0: 'Геометрия', 1: 'Дирихле', 2:
            'Инвариант', 3: 'Многочлен', 4:
            'Комбинаторика', 5: 'Оценка+Пример',
             6: 'Теория чисел', 7: 'Графы'
}
LABEL2ID = {
    'Геометрия': 0, 'Дирихле': 1,
    'Инвариант': 2, 'Многочлен': 3,
    'Комбинаторика': 4, 'Оценка+Пример': 5,
    'Теория чисел': 6, 'Графы': 7
}

model_gpt = GPT2LMHeadModel.from_pretrained(MODEL_GPT_PATH)
tokenizer_gpt = GPT2Tokenizer.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")

model_theory = BERTClass()
model_theory.load_state_dict(torch.load(MODEL_THEORY_PATH, map_location='cpu'))
tokenizer_theory = BertTokenizer.from_pretrained('bert-base-uncased')

tokenizer_topic = BertTokenizerFast.from_pretrained('blanchefort/rubert-base-cased-sentiment')
model_topic = BertForSequenceClassification.from_pretrained(MODEL_TOPIC_PATH,
                                                           num_labels=NUM_LABELS, id2label=ID2LABEL,
                                                           label2id=LABEL2ID,
                                                           ignore_mismatched_sizes=True)


def generate_response(input_text, max_length=100, temperature=0.7):
    input_ids = tokenizer_gpt.encode(input_text, return_tensors="pt").to('cpu')
    output = model_gpt.generate(
        input_ids,
        max_length=max_length,
        temperature=temperature,
        pad_token_id=tokenizer_gpt.eos_token_id,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        top_k=5,
        top_p=0.95,
        eos_token_id=tokenizer_gpt.eos_token_id,
        early_stopping=True
    )
    return tokenizer_gpt.decode(output[0], skip_special_tokens=True)


def get_predictions_theory(text, device='cpu'):
    titles = []
    predictions = []
    prediction_probs = []

    with torch.no_grad():
        inputs = tokenizer_theory(text, return_tensors="pt", max_length=128, truncation=True, padding=True)
        ids = inputs["input_ids"].to(device)
        mask = inputs["attention_mask"].to(device)
        token_type_ids = inputs["token_type_ids"].to(device)

        outputs = model_theory(ids, mask, token_type_ids)
        outputs = torch.sigmoid(outputs).detach().cpu()
        preds = (outputs > 0.5).int()

        titles.append(text)
        predictions.append(preds)
        prediction_probs.append(outputs)

    probs = torch.cat(prediction_probs)[0]
    sorted_indices = torch.argsort(probs, descending=True)
    answer = {transcript_theory[idx.item() + 1]: round(probs[idx].item() * 100) for idx in sorted_indices}
    return answer


def get_predictions_topic(text):
    inputs = tokenizer_topic(text, padding=True, truncation=True, max_length=512, return_tensors="pt").to("cpu")

    # Get model output (logits)
    outputs = model_topic(**inputs)
    probs = outputs[0].softmax(1)[0]
    sorted_indices = torch.argsort(probs, descending=True)
    answer = {ID2LABEL[idx.item()]: round(probs[idx].item() * 100) for idx in sorted_indices}
    return answer, probs.detach().numpy()
