import pandas as pd
#from translate import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#import MASTERFILE.Limpia_Data as limpia

#from googletrans import Translator 
#import pandas as pd
import MASTERFILE.Limpia_Data as LIMPIA


from transformers import MarianMTModel, MarianTokenizer
lang = "es"
target_lang = "en"
model_name = f'Helsinki-NLP/opus-mt-{lang}-{target_lang}'
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

def traduce(data,target):
    data['translated'] = data[str(target)].apply(lambda x:tokenizer.decode(model.generate(**tokenizer.prepare_seq2seq_batch([x]))   [0]))
    return data

def calc_polatity(df, corpus_col):
    neg = []
    neu = []
    pos = []
    compound = []
    for text in df[corpus_col]:
        x = SentimentIntensityAnalyzer().polarity_scores(text)
        neg.append(x["neg"])
        neu.append(x["neu"])
        pos.append(x["pos"])
        compound.append(x["compound"])
    df["neg"] = neg
    df["neu"] = neu
    df["pos"] = pos
    df["Sentiment"] = compound
    return df

def calc_Sentimiento(df, corpus_col):
    sentiment = []
    for text in df[corpus_col]:
        analizador = SentimentIntensityAnalyzer().score_valence(x)
        sentiment.append(analizador["compound"])
    df["Sentiment"] = compound
    return df





'''
def AgregaPolaridadIndicoio(df, corpus_col, translated_col= "Text" ):
    """
    Por el momento la unica solucion posible es utilizar la libreria "translate"
    La cual tiene un limite de 1000 palabras gratuitas
    Una vez hecha la traducción correcta se debe cambiar el default de translated_col por translated
    """
    #translate_corpus(df=df, corpus_col=corpus_col)
    if (translated_col != "Text" ):
        traduce(df=df, columna=corpus_col)

    calc_polatity(df, translated_col)
    #df = df.drop("translated", axis=1)
    return df
'''

'''
def traduce(df, columna):
    translator = Translator()
    df['translated'] = df[columna].head().apply(translator.translate,src='es',dest='en').apply(getattr, args=('text',))
    return (df)
'''