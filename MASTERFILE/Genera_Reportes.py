import pandas as pd
import os
import json 
import MASTERFILE.Limpia_Data as LIMPIA
import MASTERFILE.Analisis as Reporte
import MASTERFILE.CountFunctions as CountFunctions

''' ~~ FILL INFORMATION BELOW THIS LINE ~~ '''
brand = r"7enequilibrio" #Correr antes el Genera Base Twitter
folder_name = brand
Twitter = pd.read_csv(r"Data\%s\TwitterConSentimientoyPolaridad.csv" % brand).iloc[:, 1:] 

''' ~~ FILL INFORMATION ABOVE THIS LINE ~~ '''



''' ~~ GENERA DIRECTORIOS DE RESULTADOS ~~ '''
pathResultados=os.path.join(os.getcwd(),"RESULTADOS")
pathResMarca=os.path.join(pathResultados,brand)
#pathMarcaCSV=os.path.join(pathResMarca,"CSV")
pathMarcaJSON=os.path.join(pathResMarca,"JSON")

directorios=[pathResultados, pathResMarca, pathMarcaJSON]

for directory in directorios:
    if not os.path.exists(directory):
        os.makedirs(directory)

'''
CONTEOS
'''
Reporte.ConteoSocioDemograficos(Twitter).to_json(r"RESULTADOS\%s\JSON\ConteoSociodemografico.json" % folder_name, orient='records', force_ascii=False)

(Twitter[["neg","neu","pos"]].sum()/Twitter.shape[0]).to_json(r"RESULTADOS\%s\JSON\ProporcionEmociones.json" % folder_name)

segmentos=["Sexo","GrupoEdad","Region","Rango_Ingreso" ]# , "Fuente"]
for i in segmentos:
    rep = Reporte.CompletaReporteSegmentado(Reporte.ConteoVariable(Twitter,i),i).reset_index()
    rep.to_json(r"RESULTADOS\%s\JSON\Conteo_%s.json" % (folder_name, i), orient='records', force_ascii=False)

'''
SENTIMIENTO
'''
#DIARIO
Twitter = LIMPIA.LimpiaTwitter(Twitter) 
Twitter = LIMPIA.SeparaFechaTwitter(Twitter)
RepDiarioSent=Reporte.ReporteSentimientoSegmentado(Twitter, "Date")
RepDiarioSent["CutOffMax"]=[.33]*RepDiarioSent.shape[0]
RepDiarioSent["CutOffMin"]=[.33]*RepDiarioSent.shape[0]
RepDiarioSent.reset_index().to_json(r"RESULTADOS\%s\JSON\SentimientoPromedioDiario.json" % folder_name, orient='records', force_ascii=False)



#Twitter = LIMPIA.SeparaFechaTwitter(Twitter)
RepDiario=Reporte.ReporteEmocionesSegmentado(Twitter, "Date")
RepDiario["CutOffMax"]=[.33]*RepDiario.shape[0]
RepDiario["CutOffMin"]=[.33]*RepDiario.shape[0]
RepDiario.to_json(r"RESULTADOS\%s\JSON\EmocionesPromedioDiario.json" % folder_name, orient='index', force_ascii=False)




#SENTIMIENTO PROMEDIO POR SEGMENTO

segmentos=["Semaforo","Sexo","GrupoEdad","Region","Rango_Ingreso"]
for i in segmentos:
    rep = Reporte.CompletaReporteSegmentado(Reporte.ReporteSentimientoSegmentado(Twitter,i), i)
    rep.to_json(r"RESULTADOS\%s\JSON\SentimientoProm_%s.json" % (folder_name, i), orient='index', force_ascii=False)

#EMOCIONES PROMEDIO POR SEGMENTO
for i in segmentos:
    rep = Reporte.CompletaReporteSegmentado(Reporte.ReporteEmocionesSegmentado(Twitter,i), i)
    rep.to_json(r"RESULTADOS\%s\JSON\EmocionesProm_%s.json" % (folder_name, i), orient='index', force_ascii=False)


#SENTIMIENTO PROMEDIO POR DOBLE SEGMENTACION
Twitter = Twitter.loc[:, Twitter.columns != "Ingreso"]
Twitter = Twitter.rename({"Rango_Ingreso": "Ingreso", "GrupoEdad": "Edad"}, axis='columns')
variables =["Sexo", "Edad", "Region", "Ingreso"]
for i in variables:
    for j in variables:
        if variables.index(i) < variables.index(j) :
            Reporte.ReporteSentimientoSegmentado(Twitter,[i,j]).reset_index().to_json(r"RESULTADOS\%s\JSON\SentimientoProm_%s%s.json" % (folder_name, i, j),orient='records', force_ascii=False)
Twitter = Twitter.rename({"Ingreso": "Rango_Ingreso", "Edad": "GrupoEdad"}, axis='columns')


'''
TENDENCIAS
'''
def guardaJson(df,path):
    with open(path, 'w', encoding='utf-8') as f:
        df.to_json(f,orient='records', force_ascii=False)

#TREND GENERAL
guardaJson(Reporte.ReporteTrend(Twitter, n_grams=[1,2,3,4,5], top_n= 25),r"RESULTADOS\%s\JSON\TrendGeneral.json"% folder_name)

#TREND SEMAFORO
guardaJson(Reporte.ReporteTrendSegmentado(Twitter, "Semaforo", n_grams=(1,2,4), top_n=3),r"RESULTADOS\%s\JSON\TrendSemaforo.json" % folder_name)

#TREND SEGMENTADO 
segmentos=["Sexo","GrupoEdad", "Region","Rango_Ingreso"]
for i in segmentos:
    guardaJson(Reporte.ReporteTrendSegmentado(Twitter, i, n_grams=(1,2,4), top_n=1),r"RESULTADOS\%s\JSON\Trend_%s.json" % (folder_name, i))


#TREND SEGMENTACION DOBLE

Twitter = Twitter.rename({"Rango_Ingreso": "Ingreso", "GrupoEdad": "Edad"}, axis='columns')
variables =["Sexo", "Edad", "Region", "Ingreso"]
for i in variables:
    for j in variables:
        if variables.index(i) < variables.index(j) :
            guardaJson(Reporte.ReporteTrendSegmentado_doble(Twitter, [i,j], top_n=1, n_grams=[1,2,4]),r"RESULTADOS\%s\JSON\Trend_%s%s.json" % (folder_name,i,j))
Twitter = Twitter.rename({"Ingreso": "Rango_Ingreso", "Edad": "GrupoEdad"}, axis='columns')




#####################################################
#####################################################
###############  COMPETENCIA Y DENUE  ###############
#####################################################




Competencia = Reporte.CompletaReporteSentimientoSegmentado(Reporte.ReporteSentimientoSegmentado(Twitter,"Region"), "Region").drop(["Conteo"], axis=1)


Competencia["Oportunidad"]=[1.2, 7.8, 2.3, 3.2, 4.1]    #INCORPORA LOS 3
Competencia["Competencia"]=[7.4, 4.5, 3.7, 3.7, 1.1]  #INDICE FABRICADO
Competencia["Crecimiento"]=[1.2, 1.3, 2.7, 3.3, 1.1]   #CRECIMENTO PROMEDIO DEL PIB



Competencia.to_json(r"RESULTADOS\%s\JSON\MapaCompetencia.json" % (folder_name), orient='index', force_ascii=False)



















'''
Twitter.columns

#WORD_CLOUD
wordcloud_data = CF.WrdCldDta(Twitter, "WC%s" % brand, pathResMarca + folder_name, save=True)

wordcloud_data=wordcloud_data.reset_index()
wordcloud_data.columns=[["ngram", "freq"]]
wordcloud_data.head().to_dict("series")



wordcloud_data.head().to_json(orient="records" ,force_ascii=False)

import wordcloud as wc
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

sw = stopwords.words(["spanish","english"])
sw.extend(["si","rt"])

def NFWrdCld(data, name,path_, save=False):
    text = " ".join(tx for tx in Twitter["Text_clean"])
    word_c = wc.WordCloud(stopwords=sw, background_color="white",
                                colormap="winter").generate(text)
    plt.imshow(word_c, interpolation="bilinear") 
    plt.axis("off")
    if save:
            plt.savefig(pathResMarca+  "WC%s" % brand + ".png", format="png",bbox_inches="tight")
    else:
            plt.show() 

'''
