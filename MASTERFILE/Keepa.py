import numpy as np
import requests
import keepa
import json
import pandas as pd
import os
import MASTERFILE.Limpia_Data as LIMPIA
import MASTERFILE.Analisis as Reporte
import MASTERFILE.CountFunctions as CF


try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle



''' ~~ FILL INFORMATION BELOW THIS LINE ~~ '''
brand = r"Competencia_Nutricion"
folder_name = brand
nuevo = True
Twitter = pd.read_csv(r"Data\%s\TwitterConDemoSentyPol.csv" % folder_name).iloc[:, 1:] 
ASIN ="B07QN4Y17N" #mascarilla facial 2
''' ~~ FILL INFORMATION ABOVE THIS LINE ~~ '''



def RequestKeepa(ASIN , accesskey='_______________________'): 
    '''
    ASIN = solamente 1 asin
    '''
    api = keepa.Keepa(accesskey)
    # Single ASIN query
    products = api.query(ASIN, domain= "MX" , to_datetime=False) # returns list of product data
    return(products)

def guardaKeepa(products, folder, ASIN):

    with open(r'Data\%s\Keepa_scrape_%s.p' %(folder,ASIN), 'wb') as fp:
        pickle.dump(products, fp, protocol=pickle.HIGHEST_PROTOCOL)
    return(True)

def procesaKeepa(products):
    price_df = pd.DataFrame()
    price_df["Date"] = products[0]["data"]["NEW_time"]
    price_df["Price_new"] = products[0]["data"]["NEW"]
    """ LIMPIA FECHA """
    new = price_df["Date"].astype(str).str.split("T", n = 1, expand = True)
    new.columns=["aux"]
    new1 = new.aux.str.split(expand=True,)

    price_df["Date"]= new1[0]
    return price_df

def Scrape_Procesa_Keepa(ASIN , folder_name , accesskey='_______________________'):
    products = RequestKeepa(ASIN , accesskey)
    guardaKeepa(products, folder_name, ASIN)
    df = procesaKeepa(products)
    return df


'''
GENERA UN NUEVO ARCHIVO O TOMA UN SCRAPE EXISTENTE
'''
##GENERA UNO NUEVO

if (nuevo):
    producto_precios = Scrape_Procesa_Keepa(ASIN, folder_name) 

else: ###LEE UN PICKLE EXISTENTE y PROCESALO
    with open(r'Data\%s\Keepa_scrape_%s.p' %(folder_name,ASIN), 'rb') as f:
        producto = pickle.load(f)
    producto_precios = procesaKeepa(producto).dropna().reset_index(drop=True)



'''
PROCESA DUPLICADOS
'''

precios_unique = producto_precios.sort_index().drop_duplicates(subset='Date', keep='last').set_index('Date')


'''
GUARDA EL DOCUMENTO EN CSV
'''
#keepa_df = keepa_df.set_index("Date")
try:
    precios_unique.to_json(r"RESULTADOS/%s/JSON/Keepa.json"% folder_name, orient = "index")
except:
    os.makedirs(r"RESULTADOS/%s/JSON/" % folder_name)
    precios_unique.to_json(r"RESULTADOS/%s/JSON/Keepa.json"% folder_name, orient = "index")





#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++ MEZCLA DE TWITTER + KEEPA +++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



'''
REPORTES DE SENTIMIENTO Y CONTEO VS PRECIOS
'''

Twitter = LIMPIA.LimpiaTwitter(Twitter)
Twitter = LIMPIA.SeparaFechaTwitter(Twitter)
RepDiarioSent=Reporte.ReporteSentimientoSegmentado(Twitter, "Date")

df1 = RepDiarioSent[["Sentiment", "Conteo"]]
#keepa1 = keepa_df.set_index("Date")
keepa1=precios_unique
Twitter_Precios = pd.merge(df1,keepa1,how="outer", right_index=True, left_index= True)
Twitter_Precios = Twitter_Precios.sort_index().reset_index().drop_duplicates(subset='Date', keep='last').set_index('Date')
Twitter_Precios.to_json(r"RESULTADOS\%s\JSON\Precios_Stats.json" %folder_name, orient = "index" )

Twitter_Precios["Price_new"]=Twitter_Precios["Price_new"].fillna(method='bfill')
'''
ELASTICIDADES
'''
ObsCompletas=Twitter_Precios.dropna().reset_index()
Q0=ObsCompletas["Conteo"].iat[0]
Q1=ObsCompletas["Conteo"].iat[-1]
P0=ObsCompletas["Price_new"].iat[0]
P1=ObsCompletas["Price_new"].iat[-1]
T0=ObsCompletas["Date"].iat[0]
T1=ObsCompletas["Date"].iat[-1]
Elast = {"Elasticidad" : (Q1-Q0)/(P1-P0)*P1/Q1, "Actual": {"Precio": P1,"Cantidad":Q1 ,"Fecha":T1}, "Historico": {"Precio": P0,"Cantidad":Q0, "Fecha":T0}}
with open(r"RESULTADOS\%s\JSON\Elasticidad.json" %folder_name, 'w') as fp:
    json.dump(Elast, fp)


'''
JSON SUBSECCIONES
'''

base=Twitter
total_comentarios = base.shape[0]
sentimiento_promedio = Twitter["Sentiment"].mean()
precio_promedio = precios_unique["Price_new"].mean()
precio_desviacion = precios_unique["Price_new"].std()

Subsecciones = {"Total_Comentarios": total_comentarios, "Sentimiento_Promedio": sentimiento_promedio, "Precio_promedio": precio_promedio, "Precio_desviacion": precio_desviacion}
with open(r"RESULTADOS\%s\JSON\Subsecciones.json" %folder_name, 'w') as fp:
    json.dump(Subsecciones, fp)
