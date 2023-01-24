'''
Funciones necesarias para el Trend Analysis
        Funciones incluidas:
                Frecuencias de 1-n grams
                Generar Word-Cloud
                Generar Frecuencia de grams por Tiempo
                Genera Analisis por Segmentación (influencer, género, etc)
                Función que Genera archivos csv 
'''

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from PIL import Image
import wordcloud as wc 
pd.set_option('display.max_columns', None)
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})



# Sets of Stopwords
sw = stopwords.words(["spanish","english"])
sw.extend(["si","rt"])
'''
# # # Create Functions 
# Clean Text'''
def Clean_text(df,texto_columna="Text",fecha_columna=False):
    df[str(texto_columna)+"_clean"] = df[str(texto_columna)].str.replace('[^a-zA-ZñÑáéíóúÁÉÍÓÚ]|http\S+|www.\S+'," ").str.lower()
    if fecha_columna:
         df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


def trending(data, windox=5, samp_freq="D"):
        def zscore(x, windoy=windox):
                r = x.rolling(window=windoy)
                m = r.mean().shift(1)
                s = r.std(ddof=0).shift(1)
                z = (x-m)/s
                return z
        x = data.copy()
        y = x.resample(samp_freq).sum()
        scores= y.apply(zscore,axis=1).add_prefix("Z_")
        return scores

# Creates the graphs function global por día #necesaria para el csv
def plotcv(data, name, save=False, title_name="Total", freq="D", include_title=True):
    dat = data.copy()
    z=dat.resample(freq).sum()
    x=z.plot()
    x.legend(loc="best",ncol=4, fontsize="xx-small")
    if include_title:
        plt.title(str(title_name))
    plt.ylabel("Count")
    if save:
        plt.savefig(str(name) + ".pdf", format="pdf",bbox_inches="tight")
        plt.show()
    else:
        plt.show()

# Creates the frequency graphs function  global total
def freq_plotcv(data, name,path_, save=False, title_name="Total", include_title=True):
    dat = data.copy()
    dat.mean().plot("barh")
    if include_title:
        plt.title(str(title_name))
    if save:
        plt.savefig(path_+ str(name) + "_freq" + ".pdf", format="pdf",bbox_inches="tight")
        plt.show()
    else:
        plt.show()

# Create CVect Function >> Genera y Analiza la tabla de token global
def CVect(data, d_name,path_, n_feat=10, n_grams=4, d_plot=False, save_d_plot=False,
          d_title=False, d_plot_freq="D", f_plot=False,plot_title=True, window_=5,freq_="D"):
        dic= {}
        for n in range(1,n_grams+1):
                cv = CountVectorizer(max_features=n_feat,stop_words=sw,ngram_range=(n,n))
                cv_transformed = cv.fit_transform(data["Text_clean"])
                cv_df = pd.DataFrame(cv_transformed.toarray(),
                        columns=cv.get_feature_names()).set_index(data["Date"])
                dic[str(n)+"_gram"] = cv_df
                trend = trending(cv_df, windox=window_, samp_freq=freq_)
                dic[str(n)+"_trend"] = trend
                print("Most frequent sets of " +str(n) +" words: ")
                print(cv_df.sum().sort_values(ascending=False))
                print(" ")
                if d_plot:
                        fname_= str(d_name) + "_" + str(n) + "_gram"
                        title= str(d_name) + ": " + str(n) + " gram"
                        plotcv(cv_df, name=fname_ ,save=save_d_plot,title_name= title,
                               freq=d_plot_freq, include_title=plot_title)
                if f_plot:
                        fname_= str(d_name) + "_" + str(n) + "_gram"
                        title= str(d_name) + ": " + str(n) + " gram"
                        freq_plotcv(cv_df, name=fname_, path_=path_,
                                    save=save_d_plot, title_name= title,
                                    include_title=plot_title)
        return dic

# Create GroupCVect  >> Genera y Analiza la tabla de token Segmentada
def GroupCVect(data,group_col,path,n_feat=10, n_grams=4,plot_=False,save_plot_=False):
        d={}
        dat = data.groupby(group_col)
        for name, cat in dat:
                print("For the " + str(name) + " category:")
                x = CVect(data=cat,d_name=name,path_=path ,n_feat=n_feat,n_grams=n_grams,d_plot=plot_,save_d_plot=save_plot_)
                # x = x.add_prefix(str(name) +"_") #Quita el # Para agregar prefijo a las variables
                d[str(name)]= x
                print(" ")
        return d


# # # Functions that don't plot, only Generate data #########
def plotcvdta(data, name, save=False, freq="D"):
        dat = data.copy()
        z=dat.resample(freq).sum()
        if save:
                z.to_csv(str(name)+"_"+str(freq)+".csv")
        return z


def CVectDta(data, d_name,path_, n_feat=10, n_grams=4, date_data =False, save_d_plot=False,
        d_freq="D", window_=5,freq_="D"):
        dic= {}
        for n in range(1,n_grams+1):
                cv = CountVectorizer(max_features=n_feat,stop_words=sw,ngram_range=(n,n))
                cv_transformed = cv.fit_transform(data["Text_clean"])
                cv_df = pd.DataFrame(cv_transformed.toarray(),
                        columns=cv.get_feature_names()).set_index(data["Date"])
                dic[str(n)+"_gram"] = cv_df
                trend = trending(cv_df, windox=window_, samp_freq=freq_)
                trend.to_csv(str(path_)+str(d_name) + "_" + str(n) + "_gram_trend.csv")
                dic[str(n)+"_trend"] = trend
                cv_df.sum().sort_values(ascending=False).to_csv(str(path_)+str(d_name)+"_"+str(n)+"_gram.csv")
                if date_data:
                        fname_= str(path_)+str(d_name) + "_" + str(n) + "_gram_freq"
                        plotcvdta(cv_df, fname_, save=save_d_plot,freq=d_freq)
        return dic

def GCCectDta(data,group_col,path__,n_feat_=10, n_grams_=4,date_data_=False, save_d_plot_=False,
        d_freq_="D", window__=5,freq__="D"):
        d={}
        dat = data.groupby(group_col)
        for name, cat in dat:
                print("For the " + str(name) + " category:")
                x = CVectDta(data=cat,d_name=name, path_=path__ ,
                                n_feat=n_feat_,n_grams=n_grams_,
                                date_data=date_data_,save_d_plot=save_d_plot_,
                                d_freq=d_freq_,window_=window__,freq_=freq__)
                # x = x.add_prefix(str(name) +"_") #Quita el # Para agregar prefijo a las variables
                d[str(name)]= x
                print(" ")
        return d


def WrdCldDta(data, name,path, save=False, max_words=1000):
        text = " ".join(tx for tx in data["Text_clean"])
        word_c = wc.WordCloud(stopwords=sw, max_words=max_words,
                              background_color="black",
                              mode="RGBA").generate(text)
        x=word_c.words_
        y=pd.DataFrame.from_dict(data=x,orient="index")
        y.to_csv(str(path)+name+"_wrd_cloud.csv")
        return y

#Notformat WordCloud
def NFWrdCld(data, name,path_, save=False):
        text = " ".join(tx for tx in data["Text_clean"])
        word_c = wc.WordCloud(stopwords=sw,
                              background_color="white",
                              colormap="winter").generate(text)
        plt.imshow(word_c, interpolation="bilinear") 
        plt.axis("off")
        if save:
                plt.savefig(path_+ name + ".png", format="png",bbox_inches="tight")
        else:
                plt.show() 




def Twitter_Count(data,group_cols,path,n_feats=10,n_grams=4,file_name=False):
        df= pd.DataFrame()
        dat=data.groupby(group_cols)
        for gram in range(1,n_grams+1):
                cv = CountVectorizer(max_features=n_feats,stop_words=sw,ngram_range=(gram,gram),lowercase=False)
                cv_transformed = cv.fit_transform(dat["Text_clean"])
                cv_array = cv_transformed.toarray()
                cv_df = pd.DataFrame(cv_array,
                        columns=cv.get_feature_names()).sum()
                df=pd.concat([df,cv_df])
        if file_name!= False:
                df.to_csv(str(path)+"/"+str(file_name))
        return df

def GlobCVectDta(data, d_name,path_, n_feat=10, n_grams=4, save=False):
        dic= {}
        df = pd.DataFrame()
        for n in range(1,n_grams+1):
                cv = CountVectorizer(max_features=n_feat,stop_words=sw,ngram_range=(n,n))
                cv_transformed = cv.fit_transform(data["Text_clean"])
                cv_df = pd.DataFrame(cv_transformed.toarray(),
                        columns=cv.get_feature_names())
                dic[str(n)+"_gram"] = cv_df
                df = pd.merge([df,cv_df.sum()])
        if save:
                df.to_csv(path_+"/"+d_name+".csv")
        return df


