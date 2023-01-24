from transformers import MarianMTModel, MarianTokenizer
lang = "es"
target_lang = "en"
model_name = f'Helsinki-NLP/opus-mt-{lang}-{target_lang}'
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

def translate(data,target,output):
    data[str(output)] = data[str(target)].map(lambda x: tokenizer.decode(model.generate(**tokenizer.prepare_seq2seq_batch(x))[0]))
    return data