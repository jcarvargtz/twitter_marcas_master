import pickle
import pandas as pd
from textstat.textstat import textstat
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.models import load_model


def create_x(df, pickle_path, compiled_text_col, max_words=5000, max_len=11000, train=False):
    # Creates statistics from the compiled text
    feats = df[compiled_text_col].transform([
        textstat.automated_readability_index,
        textstat.avg_character_per_word,
        textstat.avg_letter_per_word,
        textstat.avg_sentence_per_word,
        textstat.avg_syllables_per_word,
        textstat.coleman_liau_index,
        textstat.dale_chall_readability_score,
        textstat.flesch_kincaid_grade,
        textstat.flesch_reading_ease,
        textstat.gunning_fog,
        textstat.lexicon_count,
        textstat.linsear_write_formula,
        textstat.lix,
        textstat.polysyllabcount,
        textstat.rix,
        textstat.sentence_count,
        textstat.smog_index,
        textstat.syllable_count
    ])
    # feats["Username"] = df.Username
    ## El español tiene mas de 300,000 palabras. Sin embargo de acuerdo a varias fuentes
    ## en promedio se utilizan 300 distintas para comunicarse cotidianamente, vamos a utilizar
    ## 5000 palabras como un "termino medio"
    max_words = 5000
    ## Se opta por una longitud de las oraciones de 11,000 pues abarca el percentil 75 de la data
    max_len = 11000
    # Tokenizes the compiled text, then creates sequences and adds padding
    X_text = df[compiled_text_col]
    if train:
        tokenizer = Tokenizer(num_words=max_words)
        tokenizer.fit_on_texts(X_text)
        seqs = tokenizer.texts_to_sequences(X_text)
        seqs_pad = sequence.pad_sequences(seqs, maxlen=max_len, truncating="post")
        with open(str(pickle_path), 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open(pickle_path, 'rb') as handle:
            tokenizer = pickle.load(handle)
        seqs = tokenizer.texts_to_sequences(X_text)
        seqs_pad = sequence.pad_sequences(seqs, maxlen=max_len, truncating="post",padding="pre")

    return feats, seqs_pad


def predict_sex_text(df, compiled_text_column, model, pickle_token):  #Falta hacer preprocesamiento
    feats, seqs_pad = create_x(df, pickle_token, compiled_text_column)
    modeload = load_model(model)
    #modeload.compile(loss="categorical_crossentropy",
    #                 optimizer="adam", metrics=["categorical_crossentropy","accuracy"])
    classes = modeload.predict_classes([feats, seqs_pad], batch_size=10)
    mapp = {1:"M", 2:"F", 3:"X"}
    s = pd.Series(classes)
    df["Sex_text"] = s.map(mapp).tolist()
    return df

def predict_from_text(df, compiled_text_column,
                      model, pickle_token, pickle_label,
                      new_column):
    feats, seqs_pad = create_x(df, pickle_token, compiled_text_column)
    modeload = load_model(model)
    #modeload.compile(loss="categorical_crossentropy",
    #                 optimizer="adam", metrics=["categorical_crossentropy", "accuracy"])
    classes = modeload.predict({"input_corpus":seqs_pad,"input_stats": feats}, batch_size=10)
    with open(pickle_label, 'rb') as handle:
        pkl_label = pickle.load(handle)
    df[new_column] = pkl_label.inverse_transform(classes)
    return df
