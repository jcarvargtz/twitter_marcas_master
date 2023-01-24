'''
Hace Scrape Twitter y Guarda la base
Agrega Sexo, Edad, Localizacion, Sentimiento, Ingreso
Traduce base para agregar "emociones" de nltk
'''


import pandas as pd
import indicoio
import os
import json 
import MASTERFILE.Limpia_Data as LIMPIA
import MASTERFILE.Make_predicts_Img as Y_Img
import MASTERFILE.CountFunctions as CF
import MASTERFILE.Analisis as Reporte
import MASTERFILE.Completa_Tabla as COMPLETA
import Scrape_functions.twitterScrapeFULL as TwitScrape
import MASTERFILE.Sentimiento as Sentimiento
#import Scrape_functions.redditScrape as RedScrape
#import MASTERFILE.Sentimiento as SentimientoNLTK

# from classifier import *


''' ~~ FILL INFORMATION BELOW THIS LINE ~~ '''
brand = r"POLITICA" #Carpeta del proyecto
folder_name = brand
Producto = "Chertorivski"  #O empresa (cada marca y cada competidor)  (ej, BBVA, Santander)
busqueda = "Chertorivski"  #Busqueda sinonimo (Ejemplo: BBVA, Bancomer )

nuevo = True
#Twitter = pd.read_csv(r"Data\%s\TwitterConSentimientoyPolaridad.csv"%brand).iloc[:, 1:] #ya incluye sentimiento y sexo y está limpia
#Twitter = LIMPIA.LimpiaTwitter(Twitter) 
#Twitter = Twitter.drop("aux_Loc", axis = 1)

''' ~~ FILL INFORMATION ABOVE THIS LINE ~~ '''


''' ~~ GENERA DIRECTORIOS DE IMAGENES DE DESCARGA ~~ '''
pathFiles=brand+"/"+ Producto
pathImagenes=pathFiles+'/Imagenes'
DataJson=r"%s/Data/Json"%pathFiles

directorios=[pathFiles, pathImagenes, DataJson]

for directory in directorios:
    if not os.path.exists(directory):
        os.makedirs(directory)



'''EXTRAE INFORMACIÓN o LEE INFO YA GENERADA'''
#Twitter_aux =  TwitScrape.Scrape_Iterativo(busqueda, brand, 201801010000, 201812310000, 12000000) #GENERO UN NUEVO CSV

if nuevo == True:
    Twitter = pd.DataFrame() #Si se quiere concatenar debe leerse un archivo
else:
    Twitter = pd.read_csv(r"%s/Data/Data_Raw_Twitter.csv"%pathFiles).iloc[:, 1:] #ya incluye sentimiento y sexo y está limpia


'''SCRAPE'''
start  = 202001020000
for i in range(5):
    batch  = 4000000 #month
    end    = start + 1990000
    Twitter_json=TwitScrape.request_json(busqueda,brand,start, end)
    if 'results' in Twitter_json.keys():
        Twitter_proc = TwitScrape.procesar_json(Twitter_json)
        Twitter = Twitter.append(Twitter_proc, ignore_index=True)
    start = end + 10000

Twitter.to_csv(r"%s/Data/Data_Raw_Twitter.csv"%pathFiles)





'''DESCARGO IMAGENES'''
Y_Img.fetch_images(Twitter, "Profile Picture", "Username", pathImagenes)





'''COMPLETA LA TABLA'''

############################################
###########DEMOGRAFICOS#####################
############################################



Twitter = COMPLETA.AgregaSexo_Img(Twitter, pathImagenes)
#Twitter = COMPLETA.AgregaSexo_Text(Twitter, "Text")
Twitter = COMPLETA.AgregaEdad_Text(Twitter, "Text")
Twitter = COMPLETA.AgregaRegion_Text(Twitter, "Text")
#Twitter = COMPLETA.AgregaLocalizacionArtificial(Twitter) 
Twitter = COMPLETA.AgregaIngreso(Twitter)


Twitter.to_csv(r"%s/Data/TwitterDemo.csv" % pathFiles)


############################################
###########SENTIMIENTO######################
############################################
Twitter = Sentimiento.traduce(Twitter, "Text")
Twitter.to_csv(r"%s/Data/TwitterTraduc.csv" % pathFiles)

Twitter = pd.read_csv(r"%s/Data/TwitterTraduc.csv"%pathFiles).iloc[:, 1:] #ya incluye sentimiento y sexo y está limpia
#Twitter = COMPLETA.AgregaSentimientoIndicoio(Twitter) #YA FUNCIONA
#indicoio.config.api_key = '391a46cc4a63b70742b6eab3d2ff868e'  #key smartia
#Twitter["Sentiment"] = Twitter.Text_clean.apply(indicoio.sentiment, axis=0)

#Twitter = COMPLETA.AgregaSentimientoIndicoio(Twitter)
#Twitter = COMPLETA.AgregaSentimientoNLTK(Twitter, "translated")

Twitter = COMPLETA.AgregaPolaridadIndicoio(Twitter, "translated")
Twitter = COMPLETA.MascaraSemaforo(Twitter) #YA FUNCIONA 
Twitter.to_csv(r"%s/Data/TwitterDemoSent.csv" % pathFiles)


'''LIMPIO INFORMACIÓN'''

Twitter = LIMPIA.LimpiaTwitter(Twitter) 
Twitter.to_csv(r"%s/Data/TwitterCompleta.csv" % pathFiles)

#Reddit = LIMPIA.LimpiaTwitter(Reddit) 
#Twitter[["Sexo", "Semaforo"]] = Twitter[["Sexo", "Semaforo"]].dropna()


















