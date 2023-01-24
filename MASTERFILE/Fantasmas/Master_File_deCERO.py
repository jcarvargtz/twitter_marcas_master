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
import Scrape_functions.twitterScrape as TS
import Scrape_functions.redditScrape as RS
import Scrape_functions.userScrape as TSuser
import pandas as pd
import os
from shutil import rmtree
import MASTERFILE.CountFunctions as CF
import Limpia_Data as LIMPIA
import MASTERFILE.Analisis as Reporte
import MASTERFILE.Completa_Tabla as COMPLETA
import numpy as np




''' ~~ FILL INFORMATION BELOW THIS LINE ~~ '''
brand = r"Bla"


pathEjemplo=os.path.join(os.getcwd(),"Ejemplo")
pathImagenes=os.path.join(os.path.join(pathEjemplo,"Imagenes"),brand)
pathResultados=os.path.join(os.path.join(pathEjemplo,"Resultados"),brand)
pathInfoGeneral=os.path.join(pathResultados,"General")
pathInfoSentimiento=os.path.join(pathResultados,"Sentimiento")
pathInfoTrend=os.path.join(pathResultados,"Trend")
''' ~~ FILL INFORMATION ABOVE THIS LINE ~~ '''


'''EXTRAE INFORMACIÓN o LEE INFO YA GENERADA'''

#Twitter=TSuser.ScrapeTW(brand,pathEjemplo,nUsers=100, nTweetsxUs=50) ##GENERO UN NUEVO CSV
#Twitter=pd.read_csv(r"Ejemplo\NokiaTwitterUsers.csv" )
#Twitter=pd.read_csv(r"Ejemplo\Ikea1.csv" ).iloc[:, 2:] #ya incluye sentimiento y sexo y está limpia
Twitter = pd.read_csv(r"Ejemplo\Loly\ConSentimiento.csv").iloc[:, 1:] #ya incluye sentimiento y sexo y está limpia

# Reddit = RS.RedditScrape( brand, pathEjemplo)



'''LIMPIO INFORMACIÓN'''

Twitter = LIMPIA.LimpiaTwitter(Twitter) #YA FUNCIONA
#Twitter = LIMPIA.SeparaFechaTwitter(Twitter)   #FALTA MODIFICAR
#Reddit = LIMPIA.LimpiaReddit(Reddit) 


'''DESCARGO IMAGENES'''
#Y_Img.fetch_images(Twitter,"Profile Picture", "Username",pathImagenes) #YA FUNCIONA


'''COMPLETA LA TABLA'''


Twitter = COMPLETA.AgregaSentimientoIndicoio(Twitter) #YA FUNCIONA
Twitter = COMPLETA.MascaraSemaforo(Twitter) #YA FUNCIONA 
Twitter = COMPLETA.AgregaSexo_Img(Twitter, pathImagenes)

Twitter.to_csv(r"Ejemplo\Loly\ConSentimiento.csv")


Twitter=Twitter[['Profile Picture', 'Username', 'Location', 'Text',
    'Date', 'User Followers', 'Text_clean', 'Sexo']]


#Twitter=Twitter[['Profile Picture', 'Username', 'Name', 'Location', 'Query', 'Text',
#    'Date', 'Followers', 'CompiledText', 'Text_clean', 'CompiledText_clean',
#    'Sentiment', 'anger', 'fear', 'joy', 'sadness', 'surprise', 'Semaforo', "Sexo"]]





#Twitter = 
Twitter = COMPLETA.AgregaEdad_Text(Twitter, "Text")
Twitter = COMPLETA.AgregaRegion_Text(Twitter, "Text") 
Twitter = COMPLETA.AgregaIngreso(Twitter)


#Twitter.to_csv(r"Ejemplo\Nokia1.csv")


'''ANALISIS'''
Twitter = Twitter.dropna()
Twitter.columns
Twitter[["Sexo", "Semaforo"]] = Twitter[["Sexo", "Semaforo"]].dropna()

segmentaciones=["Sex","GrupoEdad","Region","Ingreso","Semaforo"] #Cambiar Edad por GrupoEdad
CF.NFWrdCld(Twitter,"WCLoly",r"Ejemplo\Resultados\Loly",save=True)

Reporte.ReporteSentimiento(Twitter).to_csv(r"Ejemplo\Resultados\Loly\Sentimiento\SentimientoPromedio.csv")
Reporte.ReporteSentimientoSegmentado(Twitter,"Date").to_csv(r"Ejemplo\Resultados\Loly\Sentimiento\SentimientoPromedioDiario.csv")

Reporte.ConteoSocioDemograficos(Twitter).to_csv(r"Ejemplo\Resultados\Loly\General\ConteoSociodemografico.csv")

Reporte.ReporteTrend(Twitter).to_csv(r"Ejemplo\Resultados\Loly\Trend\TrendGeneral.csv")
Reporte.ReporteTrendSegmentado(Twitter,"Sexo").to_csv(r"Ejemplo\Resultados\Loly\Trend\TrendSexo.csv")
Reporte.ReporteTrendSegmentado(Twitter,"Semaforo").to_csv(r"Ejemplo\Resultados\Loly\Trend\TrendSemaforo.csv")
Reporte.ReporteTrendSegmentado(Twitter,"GrupoEdad").to_csv(r"Ejemplo\Resultados\Loly\Trend\TrendEdad.csv")
Reporte.ReporteTrendSegmentado(Twitter,"Region").to_csv(r"Ejemplo\Resultados\Loly\Trend\TrendLocalizacion.csv")
Reporte.ReporteTrendSegmentado(Twitter,"Ingreso").to_csv(r"Ejemplo\Resultados\Loly\Trend\TrendIngreso.csv")

Twitter.columns
Reporte.ReporteSentimientoSegmentado(Twitter,"Date").to_csv(r"Ejemplo\Resultados\Loly\Sentimiento\SentimientoPromedioDiario.csv")
Reporte.ReporteSentimientoSegmentado(Twitter,"Sexo").to_csv(r"Ejemplo\Resultados\Loly\Sentimiento\SentimientoPromedioSexo.csv")
Reporte.ReporteSentimientoSegmentado(Twitter,"Semaforo").to_csv(r"Ejemplo\Resultados\Loly\Sentimiento\SentimientoPromedioSemaforo.csv")
Reporte.ReporteSentimientoSegmentado(Twitter,"GrupoEdad").to_csv(r"Ejemplo\Resultados\Loly\Sentimiento\SentimientoPromedioGrupoEdad.csv")
Reporte.ReporteSentimientoSegmentado(Twitter,"Region").to_csv(r"Ejemplo\Resultados\Loly\Sentimiento\SentimientoPromedioLocalizacion.csv")
Reporte.ReporteSentimientoSegmentado(Twitter,"Ingreso").to_csv(r"Ejemplo\Resultados\Loly\Sentimiento\SentimientoPromedioIngreso.csv")
