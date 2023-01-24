"""
Falta
mesa1:  
    g1:listo
    g2:listo
    g3:listo
    g4:listo
mesa2:
    t1:listo
    t2:listo
    g1:listo 
    g2:Todo
    g3:listo
    g4:listo
mesa3:
    g1:todo
mesa4:
    g4:todo
"""

import pandas as pd
import yaml
import json
import numpy as np
import nltk
# import wordcloud as wc

class gen_report:
    def __init__(self,data_twitter,data_trends_tiempo,data_trends_estado,config, output_path):
        if type(data_twitter) == str:
            self.data_twitter = self.load_pandas(data_twitter)
        else:
            self.data_twitter = data_twitter
        if type(data_trends_estado) == str:
            self.data_trends_estado = self.load_pandas(data_trends_estado)
        else:
            self.data_trends_estado = data_trends_estado
        if type(data_trends_tiempo) == str:
            self.data_trends_tiempo = self.load_pandas(data_trends_tiempo)
        else:
            self.data_trends_tiempo = data_trends_tiempo
        if type(config) == str:
            self.config = self.load_config(config)
        else:
            self.config = config
        self.output_path = output_path

    def load_json(self,path):
        with open(path,"r") as fp:
            jai = json.load(fp)
        return

    def load_pandas(self,x):
        df = pd.read_csv(x)
        return df

    def load_config(self,x):
        with open(x) as f:
            y = yaml.safe_load(f)
        return y

    def mesa_1(self):
        mesa = {
            "g1":self.m1g1(),
            "g2":self.m1g2(),
            "g3":self.m1g3(),    
            "g4":self.m1g4()
        }
        return mesa

    def mesa_2(self):
        mesa={
            "t1":self.m2t1(),
            "t2":self.m2t2(),
            "g1":self.m2g1(),
            "g2":self.m2g2(),
            "g3":self.m2g3(),
            "g4":self.m2g4()
        }
        return mesa
    
    def mesa_3(self):
        mesa = {
            "g1":self.m3g1()
        }
        return mesa

    def mesa_4(self):
        mesa = {
            "g1":self.m4g1()
        }
        return mesa

    def mega_json(self):
        file = {
            "Mesa_1":self.mesa_1(),
            "Mesa_2":self.mesa_2(),
            "Mesa_3":self.mesa_3(),
            "Mesa_4":self.mesa_4()
        }
        with open(self.output_path,"w") as fp:
            json.dump(file,fp, indent=4)

    def m1g1(self):
        d = {}
        for h in config["variables"]["vars"]["Groupings"]["Region"]:
            try:
                d["Region_{}".format(h)] ={}
                h_=h
                if h == "Todo":
                    h_ = slice(None)
                try:
                    d["Region_{}".format(h)]["Sentiment"] = np.mean(temp.loc[(slice(None),slice(None),h_)]["Sentiment"])
                except:
                    d["Region_{}".format(h)]["Sentiment"] = 0
                ####################################################################################################  Definir X de acuerdo a  trends 
                try:
                    tm=self.data_trends_estado.set_index("Region")
                    d["Region_{}".format(h)]["Volumen"] = self.tm.loc[h_]["Volumen"]
                ####################################################################################################    
                except:
                    d["Region_{}".format(h)]["Volumen"] = 0
            except:
                d["Region_{}".format(h)]["Sentiment"] = 0
                d["Region_{}".format(h)]["Volumen"] = 0
        return d

    def m1g2(self):
        d={}
        d["Advertencia"]={}
        d["Palomita"]={}
        temp = self.data_twitter.groupby("Region")["Sentiment"].apply(np.mean).sort_values(ascending=False)
        d["Advertencia"]["Sentimiento"] = temp.tail(1)
        d["Palomita"]["Sentimiento"] = temp.head(1)
        ############################################################################### Corregir el nombre de las variables de acuerdo a la base de trends
        try:
            d["Advertencia"]["Popularidad"] = self.data_trends_estado.sort_values(on="Volumen").tail(1)
            d["Palomita"]["Popularidad"] = self.data_trends_estado.sort_values(on="Volumen").tail(1)
        except:
            pass
        ##################################################################################################################################################    
        return d

    def m1g3(self):
        stopwords = set(nltk.corpus.stopwords.words("spanish"))
        a = self.data_twitter['Text_clean'].str.lower().str.cat(sep=' ')
        b = nltk.tokenize.word_tokenize(a)
        c = nltk.FreqDist(w.lower() for w in b if w not in stopwords)    
        d = dict(c.most_common(50))
        return d
        
    def m1g4(self):
        da={}
        temp = self.data_twitter.copy()
        temp["dt"] = temp.Date + " " + temp.Hour
        temp["dt"] = temp.dt.apply(pd.to_datetime)
        temp["Sentiment"] = temp["Sentiment"].apply(lambda x: 50*x +50)
        temp = self.data_twitter.set_index(["Sexo","GrupoEdad","Region"])
        d = json.loads(temp.resample('D',on="dt")["Sentiment"].mean().to_json(orient="index",indent=4))
        da["Sentiment"] =d
        td = json.loads(self.data_trends_tiempo.groupby("Fecha").mean().to_json(orient="index",indent=4))
        da["Volumen"]=td
        return d


    def m2t1(self):
        temp = self.data_twitter.set_index(["Sexo","GrupoEdad","Region"])
        d = {}
        for i in config["variables"]["vars"]["Groupings"]["sexo"]:
            d["Sexo_{}".format(i)]={}
            for j in config["variables"]["vars"]["Groupings"]["GrupoEdad"]:
                d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]={}
                for h in config["variables"]["vars"]["Groupings"]["Region"]:
                    try:
                        d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] ={}
                        i_=i
                        j_=j
                        h_=h
                        if i == "Todo":
                            i_ = slice(None)
                        if j == "Todo":
                            j_ = slice(None)
                        if h == "Todo":
                            h_ = slice(None)
                        d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)]["Sentiment"] = np.mean(temp.loc[(i_,j_,h_)]["Sentiment"])
                    except:
                        d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)]["Sentiment"] = 0
        return d

    def m2t2(self):
        d={}
        temp= self.data_trends_estado.set_index("Region")
        for h in config["variables"]["vars"]["Groupings"]["Region"]:
            h_=h
            if h=="Todo":
                h_=slice(None)
            try:
                d["Region_{}".format(h)]=temp.iloc[h_]["Volumen"]
            except:
                d["Region_{}".format(h)]=0
        return d

    def m2g1(self):
        temp = self.data_twitter.set_index(["Sexo","GrupoEdad","Region"])
        d = {}
        for i in config["variables"]["vars"]["Groupings"]["sexo"]:
            d["Sexo_{}".format(i)]={}
            for j in config["variables"]["vars"]["Groupings"]["GrupoEdad"]:
                d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]={}
                for h in config["variables"]["vars"]["Groupings"]["Region"]:
                    try:
                        d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] ={}
                        i_=i
                        j_=j
                        h_=h
                        if i == "Todo":
                            i_ = slice(None)
                        if j == "Todo":
                            j_ = slice(None)
                        if h == "Todo":
                            h_ = slice(None)
                        stopwords = set(nltk.corpus.stopwords.words("spanish"))
                        a = temp.loc[(i_,j_,h_)]['Text_clean'].str.lower().str.cat(sep=' ')
                        b = nltk.tokenize.word_tokenize(a)
                        c = nltk.FreqDist(w.lower() for w in b if w not in stopwords)    
                        d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] = dict(c.most_common(10))
                    except:
                        d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] = {}
        return d

    def m2g2(self):
        pass
    #    temp = self.data_twitter.set_index(["Sexo","GrupoEdad","Region"])
    #    d = {}
    #    for i in config["variables"]["vars"]["Groupings"]["sexo"]:
    #        d["Sexo_{}".format(i)]={}
    #        for j in config["variables"]["vars"]["Groupings"]["GrupoEdad"]:
    #            d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]={}
    #            for h in config["variables"]["vars"]["Groupings"]["Region"]:
    #                try:
    #                    d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] ={}
    #                    i_=i
    #                    j_=j
    #                    h_=h
    #                    if i == "Todo":
    #                        i_ = slice(None)
    #                    if j == "Todo":
    #                        j_ = slice(None)
    #                    if h == "Todo":
    #                        h_ = slice(None)
    #                    stopwords = set(nltk.corpus.stopwords.words("spanish"))
    #                    a = temp.loc[(i_,j_,h_)]['Text_clean'].str.lower().str.cat(sep=' ')
    #                    b = nltk.tokenize.word_tokenize(a)
    #                    c = nltk.FreqDist(w.lower() for w in b if w not in stopwords)    
    #                    ngrams = dict(c.most_common(3))
    #                    mask = []
    #                    # for n in temp.loc[(i_,j_,h_)]:
    #                    #     for key in ngrams.keys():
    #                    #         # if str(key)
    #                    #         pass
    #    return 0

        
    def m2g3(self):
        temp = self.data_twitter.set_index(["Sexo","GrupoEdad","Region"])
        tm= self.data_trends_estado.set_index("Region")
        d = {}
        for i in config["variables"]["vars"]["Groupings"]["sexo"]:
            d["Sexo_{}".format(i)]={}
            for j in config["variables"]["vars"]["Groupings"]["GrupoEdad"]:
                d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]={}
                for h in config["variables"]["vars"]["Groupings"]["Region"]:
                    try:
                        d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] ={}
                        i_=i
                        j_=j
                        h_=h
                        if i == "Todo":
                            i_ = slice(None)
                        if j == "Todo":
                            j_ = slice(None)
                        if h == "Todo":
                            h_ = slice(None)
                        try:  
                            d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)]["Sentiment"] = np.mean(temp.loc[(i_,j_,h_)]["Sentiment"])
                        except:
                            d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)]["Sentiment"] = 0
                        try:  
                            ######################################################################################################### definit x a partir de base trends
                            d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)]["Volumen"] = tm.loc[h_]["Volumen"]
                            #########################################################################################################
                        except:
                            d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)]["Volumen"] = 0
                    except:
                        d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] ={}
        return d
        
    def m2g4(self):
        d = {}
        temp = self.data_twitter.copy()
        tm = self.data_trends_tiempo.copy()
        temp["dt"] = temp.Date + " " + temp.Hour
        temp["dt"] = temp.dt.apply(pd.to_datetime)
        tm["dt"] = tm.dt.apply(pd.to_datetime)
        temp = self.data_twitter.set_index(["Sexo","GrupoEdad","Region"])
        temp["Sentiment"] = temp["Sentiment"].apply(lambda x: 50*x +50)
        twit =temp.groupby(["Sexo","Region","GrupoEdad"]).resample('D',on="dt")["Sentiment"].mean()
        d["sentiment"] = json.loads(twit.to_json(orient="index",indent=4))
        try:
            trends = tm.groupby("Region").resample('D',on="dt")["Volumen"].mean()
            d["volumen"] = json.loads(trends.to_json(orient="index",indent=4))
        except:
            pass
        # d["Sentiment"] = json.loads(temp.groupby(["Sexo","Region","GrupoEdad"]).resample('D',on="dt")["Sentiment"].mean().to_json(orient="index",indent=4))
        return d  

    def m3g1(self):
        pass
    def m4g1(self):
        pass



Twitter = pd.read_csv("BBVAHackathon/Data/TwitterCompleta.csv")
trends_estado = 

reportes =  gen_report(Twitter, trends_tiempo, trends_estado, config, "BBVAHackathon/Resultados")








# {mesa2:
#     {grafica1:
#         (sexo)todo:
#             {edad1:
#                 {region_norte:
#                     estado1:dato
#                     estado2:dato
#                     estado...
#                 }
#                 {region_sur:
#                 ...}
#             {edad2:
#                 ...
#             }
#             ...
#             }}

import yaml
with open("MASTERFILE/config.yml") as f:
    config = yaml.safe_load(f)

import numpy as np
data = pd.read_csv("Data/Competencia_ChefPremier/TwitterConDemoSentyPol.csv")
data.columns
temp = self.data_twitter.copy()
temp["dt"] = temp.Date + " " + temp.Hour
temp["dt"] = temp.dt.apply(pd.to_datetime)
temp = self.data_twitter.set_index(["Sexo","GrupoEdad","Region"])
temp.groupby(["Sexo","Region","GrupoEdad"]).resample('D',on="dt").mean()
temp=data.groupby("Region")["Sentiment"].apply(np.mean).sort_values()
temp
temp = data.set_index(["Sexo","GrupoEdad","Region"])
d ={}
for i in config["variables"]["vars"]["Groupings"]["sexo"]:
    d["Sexo_{}".format(i)]={}
    for j in config["variables"]["vars"]["Groupings"]["GrupoEdad"]:
        d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]={}
        for h in config["variables"]["vars"]["Groupings"]["Region"]:
            try:
                d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] ={}
                i_=i
                j_=j
                h_=h
                if i == "Todo":
                    i_ = slice(None)
                if j == "Todo":
                    j_ = slice(None)
                if h == "Todo":
                    h_ = slice(None)
                stopwords = set(nltk.corpus.stopwords.words("spanish"))
                a = temp.loc[(i_,j_,h_)]['Text_clean'].str.lower().str.cat(sep=' ')
                b = nltk.tokenize.word_tokenize(a)
                c = nltk.FreqDist(w.lower() for w in b if w not in stopwords)    
                d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] = dict(c.most_common(10))
            except:
                d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] = {}

d={}
for h in config["variables"]["vars"]["Groupings"]["Region"]:
    try:
        d["Region_{}".format(h)] ={}
        h_=h
        if h == "Todo":
            h_ = slice(None)
        d["Region_{}".format(h)]["Sentiment"] = np.mean(temp.loc[(slice(None),slice(None),h_)]["Sentiment"])
        d["Region_{}".format(h)]["Volumen"] = np.mean(temp.loc[(slice(None),slice(None),h_)]["Volumen"])
    except:
        d["Region_{}".format(h)]["Sentiment"] = 0
        d["Region_{}".format(h)]["Volumen"] = 0

d


d = {}
for i in config["variables"]["vars"]["Groupings"]["sexo"]:
    d["Sexo_{}".format(i)]={}
    for j in config["variables"]["vars"]["Groupings"]["GrupoEdad"]:
        d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]={}
        for h in config["variables"]["vars"]["Groupings"]["Region"]:
            try:
                d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)] ={}
                i_=i
                j_=j
                h_=h
                if i == "Todo":
                    i_ = slice(None)
                if j == "Todo":
                    j_ = slice(None)
                if h == "Todo":
                    h_ = slice(None)
                d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)]["Sentiment"] = np.mean(temp.loc[(i_,j_,h_)]["Sentiment"])
            except:
                d["Sexo_{}".format(i)]["GrupoEdad_{}".format(j)]["Region_{}".format(h)]["Sentiment"] = 0
d
temp.reset_index(inplace=True)
temp["dt"] = data.Date + " " + data.Hour
temp["dt"] = data.dt.apply(pd.to_datetime)
temp = data.set_index(["Sexo","GrupoEdad","Region","dt"])
temp.groupby(["Sexo","Region","GrupoEdad"]).resample('D',on="dt")["Sentiment"].mean()

import matplotlib.pyplot as plt
temp[temp["Sexo"]=="M"]

with open("temp.json","w") as fp:
    json.dump(d,fp,indent=4)
