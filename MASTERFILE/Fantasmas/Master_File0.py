'''
ESTE ARCHIVO TOMA UN ARCHIVO YA CON SEXO, SENTIMIENTO Y EDAD
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
import Scrape_functions.twitterScrape as TS
import Scrape_functions.redditScrape as RS
import Scrape_functions.userScrape as TSuser
import pandas as pd
import os
import MASTERFILE.CountFunctions as CF
import Limpia_Data as LIMPIA
import MASTERFILE.Analisis as Reporte
import MASTERFILE.Completa_Tabla as COMPLETA



''' ~~ FILL INFORMATION BELOW THIS LINE ~~ '''
#brand="ejemplo"
#pathEjemplo=os.path.join(os.getcwd(),"Ejemplo")
''' ~~ FILL INFORMATION ABOVE THIS LINE ~~ '''



'''EXTRAE INFORMACIÓN o LEE INFO YA GENERADA'''

#Twitter= TS.TwitterScrape( brand,pathEjemplo )
#Twitter=TSuser.TwitterUserScrape(brand,pathEjemplo,nUsers=5, nTweets=50)
#Reddit=RS.RedditScrape( brand, pathEjemplo)


#SIN COMPILADO, ASUMIMOS QUE YA SE GENERO COMPLETAR TABLA
#PAra el analisis final debe tomarse el compilado
data = pd.read_excel("EjemploSamsungData.xlsx")
clases = pd.read_csv("EjemploSamsungDemograf.csv",index_col=0)
Twitter = data.merge(clases,how="right", on="Username",right_index=True)



'''LIMPIO INFORMACIÓN'''
#Twitter = LIMPIA.LimpiaTwitterCompiled(Twitter)
Twitter = LIMPIA.LimpiaTwitterText(Twitter)
#Reddit = LIMPIA.LimpiaReddit(Reddit)


'''COMPLETA LA TABLA'''
Twitter=COMPLETA.MascaraEdad(Twitter)
Twitter=COMPLETA.MascaraSemaforo(Twitter)




'''ANALISIS'''
Reporte.ReporteEstaticoSegmentado(Twitter,"Target") #Target=Sexo
Reporte.ReporteEstaticoSegmentado(Twitter,"GrupoEdad") #Mascara de Edad
Reporte.ReporteEstaticoSegmentado(Twitter,"Semaforo") #Mascara de Sentiment


