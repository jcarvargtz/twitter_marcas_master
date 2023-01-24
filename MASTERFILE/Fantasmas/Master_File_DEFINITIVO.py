'''
ESTE ARCHIVO DEBE TOMAR UNA MARCA, COMPLETAR LA TABLA Y HACER ANALISIS

**COMPLETO**

PROYECTO COMPUESTO POR LAS SIGUIENTES ETAPAS
    EXTRAE INFO
        Twitter
        Reddit
        Google News
        Unir Tablas
    LIMPIA DATA
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
import os
import json 
import MASTERFILE.Limpia_Data as LIMPIA
import MASTERFILE.Make_predicts_Img as Y_Img
import MASTERFILE.CountFunctions as CF
import MASTERFILE.Analisis as Reporte
import MASTERFILE.Completa_Tabla as COMPLETA
import Scrape_functions.twitterScrapeFULL as TwitScrape
import Scrape_functions.redditScrape as RedScrape

# from classifier import *

''' ~~ FILL INFORMATION BELOW THIS LINE ~~ '''
brand = r"Samsung S10"
folder_name = r"Samsung S10"
filename = "Samsung_S10.csv"
path = "Data/Samsung S10" 

''' ~~ FILL INFORMATION ABOVE THIS LINE ~~ '''


''' ~~ GENERA DIRECTORIOS ~~ '''
pathEjemplo=os.path.join(os.getcwd(),"Ejemplo")
pathImagenes=os.path.join(os.path.join(pathEjemplo,"Imagenes"),brand)
#pathResultados=os.path.join(os.path.join(pathEjemplo,"Resultados"),brand)
#pathInfoGeneral=os.path.join(pathResultados,"General")
#pathInfoSentimiento=os.path.join(pathResultados,"Sentimiento")
#pathInfoTrend=os.path.join(pathResultados,"Trend")
#pathJsonRes=os.path.join(pathResultados,"Json_res")

directorios=[pathEjemplo, pathImagenes]#, pathResultados, pathInfoGeneral, pathInfoSentimiento, pathInfoTrend, pathJsonRes]

for directory in directorios:
    if not os.path.exists(directory):
        os.makedirs(directory)




'''EXTRAE INFORMACIÓN o LEE INFO YA GENERADA'''


# Twitter=TSuser.ScrapeTW(brand,pathEjemplo,nUsers=100, nTweetsxUs=50) ##GENERO UN NUEVO CSV
Twitter = pd.read_csv(r"Data\Tecate Light\TwitterConDemoySent.csv").iloc[:, 1:] #ya incluye sentimiento y sexo y está limpia
Twitter = Twitter.drop("aux_Loc", axis = 1)

#Twitter = TwitScrape.Scrape_Iterativo(brand, 201901010000, 201912010000, 6000000)
#Reddit = RedScrape.RedditScrape(brand, path, since_month='month',  subreddit1='all')
#Reddit.columns


'''   
with open("Loly in the sky201812010000to201812010000.json") as json_file:
    r_json = json.load(json_file)
r_json.keys()
print(r_json)

'''

'''DESCARGO IMAGENES'''
Y_Img.fetch_images(Twitter, "Profile Picture", "Username", pathImagenes)




'''COMPLETA LA TABLA'''
#Twitter = COMPLETA.AgregaSentimientoIndicoio(Twitter) #YA FUNCIONA
indicoio.config.api_key = '391a46cc4a63b70742b6eab3d2ff868e'  #key smartia
#Twitter["Sentiment"] = Twitter.Text_clean.apply(indicoio.sentiment, axis=0)

Twitter["Sentiment"]=[None]*Twitter.shape[0]
for i in range(0,Twitter.shape[0]):
    try:
        Twitter["Sentiment"][i] = indicoio.sentiment(Twitter["Text"][i])
    except:
        Twitter["Sentiment"][i] = indicoio.sentiment(Twitter["Text"][i])



'''  
#Twitter["Emotions"] = Twitter.Text_clean.apply(indicoio.emotion, axis=0)
Twitter["Emotions"]=[None]*Twitter.shape[0]
for i in range(0,Twitter.shape[0]):
    try:
        Twitter["Emotions"][i] = indicoio.emotion(Twitter["Text"][i])
    except:
        Twitter["Emotions"][i] = indicoio.emotion(Twitter["Text"][i])
Twitter = pd.concat([Twitter.drop("Emotions", axis=1), pd.DataFrame(Twitter["Emotions"].tolist())] , axis=1 )  


Reddit["Sentiment"]=[None]*Reddit.shape[0]
for i in range(0,Reddit.shape[0]):
    try:
        Reddit["Sentiment"][i] = indicoio.sentiment(Reddit["Text"][i])
    except:
        Reddit["Sentiment"][i] = indicoio.sentiment(Reddit["Text"][i])
        print(i)

Reddit["Emotions"]=[None]*Reddit.shape[0]
for i in range(82,Reddit.shape[0]):
    try:
        Reddit["Emotions"][i] = indicoio.emotion(Reddit["Text"][i])
    except:
        Reddit["Emotions"][i] = indicoio.emotion(Reddit["Text"][i])
        print(i)
'''    
#TWITTER


Twitter = COMPLETA.MascaraSemaforo(Twitter) #YA FUNCIONA 
Twitter.to_csv(r"Data\%s\TwitterConSentimiento.csv" % folder_name)
'''
#REDDIT
Reddit = pd.concat([Reddit.drop("Emotions", axis=1), pd.DataFrame(Reddit["Emotions"].tolist())] , axis=1 )  
Reddit = COMPLETA.MascaraSemaforo(Reddit) #YA FUNCIONA 
Reddit.to_csv(r"Ejemplo\%s\ReddirConSentimiento.csv" % folder_name)
'''

Twitter = COMPLETA.AgregaSexo_Img(Twitter, pathImagenes)
Twitter = COMPLETA.AgregaSexo_Text(Twitter, "Text")
Twitter = COMPLETA.AgregaEdad_Text(Twitter, "Text")
#Twitter = COMPLETA.AgregaRegion_Text(Twitter, "Text")
Twitter = COMPLETA.AgregaLocalizacionArtificial(Twitter) 
Twitter = COMPLETA.AgregaIngreso(Twitter)
'''
Reddit = COMPLETA.AgregaSexoArtificial (Reddit)
Reddit = COMPLETA.AgregaEdad_Text(Reddit, "Text")
Reddit = COMPLETA.AgregaRegion_Text(Reddit, "Text") 
Reddit = COMPLETA.AgregaIngreso(Reddit)
'''
Twitter.to_csv(r"Data\%s\TwitterConDemoySent.csv" % folder_name)
'''
Reddit.to_csv(r"Data\%s\RedditConPredicciones.csv" % folder_name)
'''


'''LIMPIO INFORMACIÓN'''

Twitter = LIMPIA.LimpiaTwitter(Twitter) 
#Reddit = LIMPIA.LimpiaTwitter(Reddit) 

Twitter[["Sexo", "Semaforo"]] = Twitter[["Sexo", "Semaforo"]].dropna()


