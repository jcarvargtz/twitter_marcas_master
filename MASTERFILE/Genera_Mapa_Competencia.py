import pandas as pd
import os
import json 
#import MASTERFILE.Limpia_Data as LIMPIA
#import MASTERFILE.Analisis as Reporte
#import MASTERFILE.CountFunctions as CountFunctions

''' ~~ FILL INFORMATION BELOW THIS LINE ~~ '''
brands = ["ChefPremier", "Mooch App", "7enequilibrio"] #Correr antes el Genera Base Twitter
for brand in brands:
    folder_name = brand

    with open(r"Data/%s/Competencia.json"%brand) as f:
        competencia = json.load(f)


    with open(r"Data/%s/crecimiento_estatal.json"%brand) as f:
        crecimiento = json.load(f)

    with open(r"RESULTADOS/%s/JSON/SentimientoProm_Region.json"%brand) as f:
        sentimiento = json.load(f)


    Regiones = competencia.keys()
    Regiones
    mapa={}
    for region in Regiones:
        if region == "Sureste":
            mapa["SurEste"]={
            'Sentiment': sentimiento["SurEste"]["Sentiment"],
            'Competencia': competencia[region],
            'Crecimiento': crecimiento [region]
            }
        else:
            mapa[region]={
            'Sentiment': sentimiento[region]["Sentiment"],
            'Competencia': competencia[region],
            'Crecimiento': crecimiento [region]
        }

    with open (r"RESULTADOS\%s\JSON\MapaCompetencia.json"%brand, 'w') as file:
        json.dump( mapa ,file)
