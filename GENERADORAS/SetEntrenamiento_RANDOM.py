import pandas as pd 
import  Scrape_functions.userScrape as userScrape
import Make_predicts_Img as Predict
import Limpia_Data as LIMPIA
import os

'''DEFINICIÓN DE PATH DE ENTRENAMIENTO'''
path="ENTRENAMIENTO"
edades=range(14,61) 

'''SELECCIONA PALABRAS DE CUMPLEAÑOS'''
palabras=["en","a","el","la","con"]

''' REALIZA SCRAPE'''
baseEntrenamiento=pd.DataFrame()
for i in palabras:
    base_aux=userScrape.ScrapeTW(i, path, nUsers=5, nTweetsxUs=10, guardar=False)
    baseEntrenamiento= baseEntrenamiento.append(base_aux) 

'''DESCARGA IMAGENES'''
#Predict.fetch_images(baseEntrenamiento,"Profile Picture","Username","ENTRENAMIENTO\Imagenes_Entrenamiento")


'''LIMPIA TEXTO Y TEXTOCOMPILADO'''
baseEntrenamiento=LIMPIA.LimpiaTwitter(baseEntrenamiento)

'''GUARDA BASE'''
filename="BaseEntrenamiento_Random"
baseEntrenamiento.to_csv(os.path.join("ENTRENAMIENTO", filename), index = False)
