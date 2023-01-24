
'''

**COMPLETA TABLA**

PROYECTO COMPUESTO POR LAS SIGUIENTES ETAPAS
    EXTRAE INFO
    COMPLETA TABLA  
        Agrega Sentimiento *nltk
            Genera Subgrupo Semaforo
        Agrega Edad *.h5
            Genera Subgrupos Edad
        Agrega Sexo *.h5
    ANALIZA 
'''

import pandas as pd 
import indicoio
from PIL import Image
import requests
import os
import numpy as np
import MASTERFILE.Make_predicts_Texto as Y_Txt
import MASTERFILE.Make_predicts_Img as Y_Img
import MASTERFILE.Sentimiento as Sentimiento




#import MASTERFILE.Limpia_Data as limpia

#from translate import Translator
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#import MASTERFILE.Limpia_Data as limpia


'''Carga modelos de predicción '''
PathModelos = r"ENTRENAMIENTO/MODELOS/Entrenados/MODELOS"
PathTokenizer = r"ENTRENAMIENTO/MODELOS/Entrenados/TOKENIZER"
PathEncoder = r"ENTRENAMIENTO/MODELOS/Entrenados/ENCODER"
modeloImagen_sexo = r"%s/model_entrenado_imagen_sexo.h5"%PathModelos
modeloTexto_sexo = r"%s/modelo_entrenado_texto_sexo.h5"%PathModelos
modeloTexto_edad = r"%s/modelo_entrenado_texto_edad.h5"%PathModelos
modeloTexto_loc = r"%s/modelo_entrenado_texto_localizacion.h5"%PathModelos
tokenizerSexoPickle = r"%s/tokenizer_texto_sexo.pickle"%PathTokenizer
tokenizerEdadPickle = r"%s/tokenizer_texto_Edad.pickle"%PathTokenizer
tokenizerLocPickle = r"%s/tokenizer_texto_localizacion.pickle"%PathTokenizer
yTextoSexoPickle = r"%s/y_enc_texto_sexo.pickle"%PathEncoder
yTextoEdadPickle = r"%s/y_enc_texto_edad.pickle"%PathEncoder
yTextoLocPickle = r"%s/y_enc_texto_loc.pickle"%PathEncoder




'''Agrega Sentimiento'''

def AgregaSentimientoIndicoio(df, corpus_col ):
    #Twitter = COMPLETA.AgregaSentimientoIndicoio(Twitter) #YA FUNCIONA
    indicoio.config.api_key = '391a46cc4a63b70742b6eab3d2ff868e'  #key smartia
    #Twitter["Sentiment"] = Twitter.Text_clean.apply(indicoio.sentiment, axis=0)
    df["Sentiment"]=[None]*df.shape[0]
    for i in range(0,df.shape[0]): 
        try:
            df["Sentiment"][i] = indicoio.sentiment(df[corpus_col][i])
        except:
            df["Sentiment"][i] = indicoio.sentiment(df[corpus_col][i])

    return (df)

def AgregaPolaridadIndicoio(df, corpus_col ):
    """
    Por el momento la unica solucion posible es utilizar la libreria "translate"
    La cual tiene un limite de 1000 palabras gratuitas
    Una vez hecha la traducción correcta se debe cambiar el default de translated_col por translated
    """
    df = Sentimiento.calc_polatity(df, corpus_col)
    #df = df.drop("translated", axis=1)
    return df


def AgregaSentimientoNLTK(df, corpus_col ):
    """
    Por el momento la unica solucion posible es utilizar la libreria "translate"
    La cual tiene un limite de 1000 palabras gratuitas
    Una vez hecha la traducción correcta se debe cambiar el default de translated_col por translated
    """
    df = Sentimiento.calc_Sentimiento(df, corpus_col)
    #df = df.drop("translated", axis=1)
    return df







'''Agrega Variables Demograficas'''


def AgregaIngreso(df):
    data_ingreso = pd.read_csv("MASTERFILE/INGRESO.csv")[["Sexo", "Estado", "GrupoEdad", "Ingreso"]]
    data_ingreso = MascaraRegion(data_ingreso)
    resumen_ingreso = data_ingreso.groupby(["Sexo", "GrupoEdad", "Region"], as_index=False ).mean()
    df = pd.merge(df, resumen_ingreso, on=["Sexo", "GrupoEdad", "Region"])
    df = MascaraIngreso(df)
    return df

def AgregaSexo_Img(df, path_imagenes):
    #df = Y_Img.predict_sex_image(dataframe=df, folder_path=path_imagenes, model_path="model_saved_4.h5")
    df = Y_Img.predict_sex_image(dataframe=df, folder_path=path_imagenes, model_path=modeloImagen_sexo) 
    return df
   
def AgregaEdad_Text(df, text_predict):
    df = Y_Txt.predict_from_text(df, text_predict, modeloTexto_edad, tokenizerEdadPickle, yTextoEdadPickle, "GrupoEdad")
    return df

def AgregaRegion_Text(df, text_predict):
    df = Y_Txt.predict_from_text(df, text_predict, modeloTexto_loc, tokenizerLocPickle, yTextoLocPickle, "Region")
    return df

def AgregaSexo_Text(df, text_predict):
    # df = Y_Txt.predict_from_text(df, text_predict, modeloTexto_sexo, tokenizerSexoPickle, yTextoSexoPickle, "Sexo")
    df = Y_Txt.predict_sex_text(df, text_predict, modeloTexto_sexo, tokenizerSexoPickle)
    return df




'''GenerarSubgrupos'''
def MascaraEdad(df):
    df["GrupoEdad"] = ["Menor" if i<18 else "Joven" if i<30 else "Adulto" if i<45 else "Mayor" for i in df["Edad"] ]
    return df

def MascaraSemaforo(df):
    df["Semaforo"] = ["Rojo" if i<.33 else "Amarillo" if i<.66 else "Verde" for i in df["Sentiment"] ]
    return df

def MascaraIngreso(df):
    df["Rango_Ingreso"] = ["A" if i>20000 else "B" if i>15000 else "C" if i>10000  else "D" for i in df["Ingreso"] ]
    return df       

def MascaraRegion(df):
    noroeste = ["Baja California", "Baja California Sur", "Chihuahua", "Sinaloa" ,"Sonora"]
    sureste = [ "Campeche", "Chiapas", "Guerrero","Oaxaca", "Quintana Roo","Tabasco", "Veracruz", "Yucatán"]
    occidente = ["Aguascalientes", "Colima", "Guanajuato", "Jalisco", "Michoacán", "Nayarit", "Querétaro", "Zacatecas"]
    noreste = ["Coahuila", "Durango", "Nuevo León", "San Luis Potosí", "Tamaulipas"]
    #centro =["Tlaxcala", "Ciudad de México", "Estado de México", "Morelos", "Puebla", "Hidalgo"]
    df["Region"] = ["Noroeste" if i in noroeste else "SurEste" if i in sureste else "Occidente" if i in occidente else "Noreste" if i in noreste else "Centro" for i in df["Estado"] ]
    return (df)

def CompletaTabla(df, path_imagenes, modelo="model_saved_4.h5"):
    df = AgregaSentimientoIndicoio(df)
    df = AgregaEdad(df)
    df = AgregaSexoImagen(df, path_imagenes)
    df = MascaraEdad(df)
    df = MascaraSemaforo(df)
    return(df)








'''
GENERACIÓN DE VARIABLES FALTALNTES ARTIFICIALMENTE
'''

def AgregaEdadArtificial(df):
    edades = ['Menor', 'Joven', 'Adulto', 'Mayor']
    df["GrupoEdad"]=np.random.choice(edades, df.shape[0], p=[0.15, 0.40, 0.30, 0.15])    
    return(df)

def AgregaLocalizacionArtificial(df):
    estados=["Aguascalientes", "Baja California", "Baja California Sur", "Chiapas","Campeche",
     "Chihuahua","Coahuila","Colima","Durango","Guanajuato",
    "Guerrero","Hidalgo","Jalisco","Estado de México","Michoacán",
    "Morelos","Nayarit","Nuevo León","Oaxaca","Puebla",
    "Querétaro","Quintana Roo","San Luis Potosí","Sinaloa","Sonora",
    "Tabasco","Tamaulipas","Tlaxcala","Veracruz","Yucatán",
    "Zacatecas","Ciudad de Mexico"]
    p=[.0103, .0275, .0049, .0415, .0073,
     .0313, .0241, .0055, .0146, .0473,
      .0301, .0227, .0653, .1356, .0384,
       .0156, .0091, .0406, .0339,.0521,
       .0154, .0109, .0233, .0252,.0231, 
       .0192,.0292,.0103,.0688,.0176,
       .0132,.0861]

    df["aux_Loc"]=np.random.choice(estados, df.shape[0], p)
    
    noroeste = ["Baja California", "Baja California Sur", "Chihuahua", "Sinaloa" ,"Sonora"]
    sureste = [ "Campeche", "Chiapas", "Guerrero","Oaxaca", "Quintana Roo","Tabasco", "Veracruz", "Yucatán"]
    occidente = ["Aguascalientes", "Colima", "Guanajuato", "Jalisco", "Michoacán", "Nayarit", "Querétaro", "Zacatecas"]
    noreste = ["Coahuila", "Durango", "Nuevo León", "San Luis Potosí", "Tamaulipas"]
    #centro =["Tlaxcala", "Ciudad de México", "Estado de México", "Morelos", "Puebla", "Hidalgo"]
    df["Region"] = ["Noroeste" if i in noroeste else "SurEste" if i in sureste else "Occidente" if i in occidente else "Noreste" if i in noreste else "Centro" for i in df["aux_Loc"] ]
    df.drop("aux_loc")
    return(df)


def AgregaIngresoArtificial(df):
    Ingresos = ['A/B', 'Cplus', 'C', 'D', 'E']
    df["Ingreso"]=np.random.choice(Ingresos, df.shape[0], p=[0.05, 0.10, 0.20, 0.35, 0.30])    
    return(df)

def AgregaSexoArtificial(df):
    Sexo = ['F', 'M', 'X']
    df["Sexo"]=np.random.choice(Sexo, df.shape[0], p=[0.4,0.4,0.2])    
    return(df)
















#def AgregaSentimientoIndicoio(df):
#    indicoio.config.api_key = 'f8300d7d98580ebd738ed28b61a5cafc'  #key smartia
#    df["Sentiment"] = df.Text.apply(indicoio.sentiment, axis=0)
#    df["Emotions"] = df.Text.apply(indicoio.emotion, axis=0)
#    df = pd.concat([df.drop("Emotions", axis=1), pd.DataFrame(df["Emotions"].tolist())] , axis=1 ) 
#    return df



'''


def AgregaSentimientoNLKT(df, columna):
    """
    Por el momento la unica solucion posible es:
    -Traducir el texto de español a ingles, esto no implica perdida
         de informacion en cuanto al sentimiento.
         Para esto se utiliza la libreria "translate"
        La cual tiene un limite de 1000 palabras gratuitas.
        Utilizar el API de google translate implica varios problemas.
        Ahora se puede utilizar otro proovedor de servicios de traduccion en esa libreria
        Pero impica sacar claves de acceso
        Para mas informacion https://mymemory.translated.net/doc/usagelimits.php
    """
    # df = limpia.Clean_text(df)
    # df["temp"] = df["Text"].apply(lambda row: row.encode("ascii", errors="ignore").decode())
    df = SentimientoNLTK.Agrega_polaridad(df, columna)
    # df = df.drop("temp", axis=1)
    return(df)

'''