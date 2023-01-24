import pandas as pd 
import  Scrape_functions.userScrape as userScrape
import Make_predicts_Img as Predict
import Limpia_Data as LIMPIA
import os

'''DEFINICIÓN DE PATH DE ENTRENAMIENTO'''
path="ENTRENAMIENTO"
edades1=range(14,20) 
edades2=range(20,30) 
edades3=range(30,45) 
edades4=range(45,60) 

'''SELECCIONA PALABRAS DE CUMPLEAÑOS'''
cumples=["#cumplo","#micumple","#micumpleaños","#hbd"]

''' REALIZA SCRAPE'''
#baseEntrenamiento=pd.DataFrame()  #si no hay un archivo de edad generado
#baseEntrenamiento=pd.read_csv("ENTRENAMIENTO\BaseEntrenamiento_EDAD.csv") #para aumentar la base



for i in cumples:
    for edad in edades4:   #cambiar Edades
        busqueda= i + str(edad)
        base_aux=userScrape.ScrapeTW(busqueda, path, nUsers=5, nTweetsxUs=10, guardar=False)
        base_aux["Edad"]=edad
        baseEntrenamiento= baseEntrenamiento.append(base_aux) 

'''DESCARGA IMAGENES'''
Predict.fetch_images(baseEntrenamiento,"Profile Picture","Username","ENTRENAMIENTO\Imagenes_Entrenamiento")


'''LIMPIA TEXTO Y TEXTOCOMPILADO'''
baseEntrenamiento=LIMPIA.LimpiaTwitter(baseEntrenamiento)

'''GUARDA BASE'''
filename="BaseEntrenamiento_EDAD"
baseEntrenamiento.to_csv(os.path.join("ENTRENAMIENTO", filename), index = False)
