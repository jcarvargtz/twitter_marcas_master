'''Funciones que se utilizan para generar los reportes'''
import MASTERFILE.CountFunctions as CF
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


def ConteoSocioDemograficos(df):
    variables=["Sexo","GrupoEdad","Region"]#,"Ingreso"]
    reporte=df[variables].apply(pd.Series.value_counts)
    reporte=reporte.reset_index(level=0) #.wide_to_long()
    reporte=reporte.melt(id_vars="index",var_name="Variable",value_name="Freq").dropna()
    reporte=reporte[["Variable","index","Freq"]]
    return(reporte)


def ConteoVariable(df,variable):
    reporte=df[variable].value_counts()
    reporte=reporte.reset_index(level=0) #.wide_to_long()
    reporte.columns=[variable, "Freq"]
    #reporte=reporte.melt(id_vars="Freq",value_name="Sexo").dropna()
    reporte=reporte[[variable, "Freq"]]
    aux=reporte["Freq"].sum()
    reporte["Freq_Rel"]=reporte["Freq"]/aux
    reporte = reporte.set_index(variable)
    return(reporte)


def ReporteTrend(df, n_grams=range(3), top_n=3):
    '''
    n_grams: vector type, default es range(3) 
    top_n : default 3
    '''
    # Sets of Stopwords
    sw = stopwords.words(["spanish","english"])
    sw.extend(["si","rt"])
    reporte = pd.DataFrame()
    
    n_list = [*n_grams]
    n_grams_aux = [x - 1 for x in n_grams]
    n_grams1 = list(filter(lambda x: x != [0], n_grams_aux))


    for i in (n_grams1):
        cv = CF.CountVectorizer(max_features=top_n,stop_words=sw,ngram_range=((i+1),(i+1)))
        #hace fit a la data
        try:
            cv_transformed = cv.fit_transform(df["Text_clean"].values.astype('U'))
            #Tabla de conteos (dict[2_gram])
            cv_df = pd.DataFrame(cv_transformed.toarray(),columns=cv.get_feature_names()).set_index(df["Date"])
            #if (i==2):
            #    print(cv_df)
            freq_ngram_ordenado=cv_df.sum().sort_values(ascending=False)
            freq_ngram_ordenado=pd.DataFrame(freq_ngram_ordenado)
            freq_ngram_ordenado=freq_ngram_ordenado.reset_index()
            freq_ngram_ordenado.columns=["ngram","freq"]
            freq_ngram_ordenado["n"]=i+1
            #freq_ngram_ordenado=freq_ngram_ordenado[-1:]+freq_ngram_ordenado[:-1]
            reporte=reporte.append(freq_ngram_ordenado)
        except:
            #reporte=[None]*(len(n_grams)*top_n)
            print("No registros en categoria %s"%i)
    return(reporte)



def ReporteTrendSegmentado(df, segmentacion, n_grams=range(4), top_n=5):
    reporte=pd.DataFrame()
    dat = df.groupby(segmentacion)
    n_tot=len(n_grams)*top_n
    for categoria, data in dat:
        A=pd.DataFrame(np.repeat(str(categoria),  n_tot   )).reset_index(drop=True)
        B=ReporteTrend(data,n_grams,top_n).reset_index(drop=True)
        reporteCat=pd.concat([A,  B  ], axis=1)
        
        reporte=reporte.append(reporteCat)   
        
    reporte.columns = [str(segmentacion), "ngram", "freq", "n"]
    reporte = reporte[[str(segmentacion), "n", "ngram", "freq"]]
    reporte= reporte.dropna()
        
    return(reporte)



def ReporteTrendSegmentado_doble(df, segmentacion, n_grams=range(4), top_n=5):
    reporte=pd.DataFrame()
    dat = df.groupby(segmentacion)
    n_tot=len(n_grams)*top_n
    for categoria, data in dat:
        A0=pd.DataFrame(np.repeat(categoria[0],  n_tot   )).reset_index(drop=True)
        A1=pd.DataFrame(np.repeat(categoria[1],  n_tot   )).reset_index(drop=True)
        B=ReporteTrend(data,n_grams,top_n).reset_index(drop=True)
        reporteCat=pd.concat([A0,A1,B], axis=1)
        reporte=reporte.append(reporteCat)   
    
    reporte.columns = [segmentacion[0], segmentacion[1], "ngram", "freq", "n"]
    reporte = reporte[[segmentacion[0], segmentacion[1], "n", "ngram", "freq"]]
    reporte= reporte.dropna()
    return(reporte)






def ReporteSentimiento(df):
    #sentimientos=["anger","fear","joy","sadness","surprise","Sentiment"]
    sentimientos=["Sentiment"]
    reporte=df[sentimientos].mean()
    reporte["Conteo"]=df["Sentiment"].count()
    return(reporte)

def ReporteSentimientoSegmentado(df,segmentacion):
    #sentimientos=["anger","fear","joy","sadness","surprise","Sentiment"]
    sentimientos=["Sentiment"]
    reporte=df.groupby((segmentacion)) [sentimientos].mean()
    reporte["Conteo"]=df.groupby(segmentacion)["Sentiment"].count()
    #reporte = reporte.set_index(segmentacion)
    #print(reporte)
    #reporte =  CompletaReporteSentimientoSegmentado(reporte, segmentacion)
    return(reporte)


def ReporteEmociones(df):
    sentimientos=["neg","pos","neu"]
    #sentimientos=["Sentiment"]
    reporte=df[sentimientos].mean()
    reporte["Conteo"]=df["Sentiment"].count()
    return(reporte)

def ReporteEmocionesSegmentado(df,segmentacion):
    sentimientos=["neg","pos","neu"]
    #sentimientos=["Sentiment"]
    reporte=df.groupby((segmentacion)) [sentimientos].mean()
    reporte["Conteo"]=df.groupby(segmentacion)["Sentiment"].count()
    #print(reporte)
    #reporte =  CompletaReporteSentimientoSegmentado(reporte, segmentacion)
    return(reporte)









def CompletaReporteSentimientoSegmentado(df, segmentacion):
    if segmentacion == "Sexo":
        variables = ["F" , "M"]
    elif segmentacion == "GrupoEdad":
        variables = ["Menor", "Joven", "Adulto", "Mayor"]
    elif segmentacion == "Region":
        variables =["Noroeste", "SurEste", "Occidente", "Noreste", "Centro"]
    elif segmentacion == "Semaforo":
        variables = ["Verde", "Amarillo", "Rojo"]
    elif segmentacion == "Rango_Ingreso":
        variables = ["A", "B ", "C", "D"]
    else:
        print("SEGMENTACION ERROREA")
     
    for i in variables:
        if i not in df.index:
            df.loc[i] = [0, 0]
            
    return df
    
def CompletaReporteEmocionesSegmentado(df, segmentacion):
    if segmentacion == "Sexo":
        variables = ["F" , "M"]
    elif segmentacion == "GrupoEdad":
        variables = ["Menor", "Joven", "Adulto", "Mayor"]
    elif segmentacion == "Region":
        variables =["Noroeste", "SurEste", "Occidente", "Noreste", "Centro"]
    elif segmentacion == "Semaforo":
        variables = ["Verde", "Amarillo", "Rojo"]
    elif segmentacion == "Rango_Ingreso":
        variables = ["A", "B ", "C", "D"]
    else:
        print("SEGMENTACION ERROREA")
     
    for i in variables:
        if i not in df.index:
            df.loc[i] = [0, 0, 0, 0]
            
    return df

def CompletaReporteSegmentado(df, segmentacion):
    if segmentacion == "Sexo":
        variables = ["F" , "M"]
    elif segmentacion == "GrupoEdad":
        variables = ["Menor", "Joven", "Adulto", "Mayor"]
    elif segmentacion == "Region":
        variables =["Noroeste", "SurEste", "Occidente", "Noreste", "Centro"]
    elif segmentacion == "Semaforo":
        variables = ["Verde", "Amarillo", "Rojo"]
    elif segmentacion == "Rango_Ingreso":
        variables = ["A", "B", "C", "D"]
    else:
        print("SEGMENTACION ERROREA")
     
    for i in variables:
        if i not in df.index:
            df.loc[i] = [0] * df.shape[1]
            
    return df






#dat = Twitter.groupby(["GrupoEdad"])
#n_tot=len(n_grams)*top_n
#i=0
#for categoria, data in dat:
    #A=pd.DataFrame(np.repeat(str(categoria),  5   )).reset_index(drop=True)
#    print(i)
#    B=Reporte.ReporteTrend(data,range(4)).reset_index(drop=True)
#    i=i+1



# reporteCat=pd.concat([A,  B  ], axis=1)
#    print(reporteCat)
#    print("hola")
    
    #reporteCat=pd.concat([A,  B  ], axis=1)
    #reporte=reporte.append(reporteCat)





'''

def ReporteTrend(df, n_grams=range(3), top_n=3):

    n_grams: vector type, default es range(3) 
    top_n : default 3
    
    # Sets of Stopwords
sw = stopwords.words(["spanish","english"])
sw.extend(["si","rt"])
reporte=pd.DataFrame()
df=Twitter[Twitter["GrupoEdad"]=="Menor"]
n_grams=[4]
top_n=3
for i in n_grams:
i=4    
cv = CF.CountVectorizer(max_features=top_n,stop_words=sw,ngram_range=((i+1),(i+1)))
#hace fit a la data
cv_transformed = cv.fit_transform(df["Text_clean"].values.astype('U'))
#Tabla de conteos (dict[2_gram])
cv_df = pd.DataFrame(cv_transformed.toarray(),columns=cv.get_feature_names()).set_index(df["Date"])
freq_ngram_ordenado=cv_df.sum().sort_values(ascending=False)
freq_ngram_ordenado=pd.DataFrame(freq_ngram_ordenado)
freq_ngram_ordenado=freq_ngram_ordenado.reset_index()
freq_ngram_ordenado.columns=["ngram","freq"]
freq_ngram_ordenado["n"]=i+1
#freq_ngram_ordenado=freq_ngram_ordenado[-1:]+freq_ngram_ordenado[:-1]
reporte=reporte.append(freq_ngram_ordenado)
return(reporte)

'''

'''



def ReporteTrend(df, n_grams=range(3), top_n=3):
    
    #n_grams: vector type, default es range(3) 
    #top_n : default 3
    
    # Sets of Stopwords
    sw = stopwords.words(["spanish","english"])
    sw.extend(["si","rt"])
    reporte = pd.DataFrame()
    for i in n_grams:
        cv = CF.CountVectorizer(max_features=top_n,stop_words=sw,ngram_range=((i+1),(i+1)))
        #hace fit a la data
        try:
            cv_transformed = cv.fit_transform(df["Text_clean"].values.astype('U'))
            #Tabla de conteos (dict[2_gram])
            cv_df = pd.DataFrame(cv_transformed.toarray(),columns=cv.get_feature_names()).set_index(df["Date"])
            freq_ngram_ordenado=cv_df.sum().sort_values(ascending=False)
            freq_ngram_ordenado=pd.DataFrame(freq_ngram_ordenado)
            freq_ngram_ordenado=freq_ngram_ordenado.reset_index()
            freq_ngram_ordenado.columns=["ngram","freq"]
            freq_ngram_ordenado["n"]=i+1
            #freq_ngram_ordenado=freq_ngram_ordenado[-1:]+freq_ngram_ordenado[:-1]
            reporte=reporte.append(freq_ngram_ordenado)
        except:
            #reporte=[None]*(len(n_grams)*top_n)
            print("No registros en categoria %s"%i)
    return(reporte)

'''










#ReporteTrendSegmentado(Twitter, "Sexo").to_json("Reporte.json" ,orient="values", force_ascii=False) 
