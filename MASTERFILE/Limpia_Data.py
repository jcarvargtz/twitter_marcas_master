import pandas as pd
import numpy as np
from nltk.corpus import stopwords



def Clean_text(df,texto_columna="Text",fecha_columna=False):
    df[str(texto_columna)+"_clean"] = df[str(texto_columna)].str.replace('[^a-zA-ZñÑáéíóúÁÉÍÓÚ]|http\S+|www.\S+'," ").str.lower()
    if fecha_columna:
         df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

def LimpiaTwitterText(df):
     df = Clean_text(df,"Text",True)
     return(df)

def LimpiaTwitter(df):
     df = Clean_text(df,"Text",True)
     #df = Clean_text(df,"CompiledText",True)
     return(df)

def LimpiaReddit(df):
     df = Clean_text(df, "Text")
     return(df)

def SeparaFechaTwitter(df): 
     #df.dropna(inplace = True) 
     new = df["Date"].astype(str).str.split(" ", n = 2, expand = True)
     #new = df["Date"].str.split(" ",expand=True) 
     df["Date"]= new[0]
     try:
          df["Hour"]= new[1]
     except:
        print("Fecha Separada")
     return(df)

def SeparaFechaKeepa(df): 
     #df.dropna(inplace = True) 
     new = df["Date"].astype(str).str.split("T", n = 2, expand = True)
     #new = df["Date"].str.split(" ",expand=True) 
     df["Date"]= new[0]
     try:
          df["Hour"]= new[1]
     except:
        print("Fecha Separada")
     return(df)