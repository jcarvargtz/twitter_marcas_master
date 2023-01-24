from PIL import Image
import requests
import os
from textstat.textstat import textstat
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence, image
from keras.models import load_model
import numpy as np
import pandas as pd


def predict_sex_image(folder_path,model_path,dataframe,image_shape=(48,48)):
    img_width, img_height = image_shape
    model = load_model(model_path)
    #model.compile(loss='categorical_crossentropy',
    #            optimizer='rmsprop',
    #            metrics=['accuracy'])
    # load all images into a list
    images = []
    dic = {}
    for img in os.listdir(folder_path):
        index=str(img)
        img = os.path.join(folder_path, img)
        img = image.load_img(img, target_size=(img_width, img_height))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        images.append(img)
        dic[index] =img
    # stack up images list to pass for prediction
    images = np.vstack(images)
    classes = model.predict_classes(images, batch_size=10)
    aux= pd.DataFrame(classes,index=dic.keys(),columns=["Sex_encod"])
    aux=aux.reset_index()
    new= aux["index"].str.split(".", n = 1, expand = True) 
    aux["Username"]=new[0]
    dataframe=pd.merge(dataframe,aux,on="Username", how="left")
    dataframe["Sexo"]=["F" if i==1 else "M" if i==2 else "X" for i in dataframe["Sex_encod"] ]
    dataframe=dataframe.drop(["Sex_encod","index"], axis=1)
    return dataframe

def predict_text_image(X,model):  #Falta hacer preprocesamiento
    model = load_model(model)
    predictions = model.predict(X)
    return predictions

def fetch_images(data,links_colname,users_colname,save_path):
    if (os.path.exists(save_path )==False):
        os.mkdir(save_path)
        
    bad_users=[]
    j=0
    for i in range(data.shape[0]):
        url=data[str(links_colname)].iloc[i]
        user=data[str(users_colname)].iloc[i]
        try:
            im=Image.open(requests.get(url, stream=True).raw)
            im.save(str(save_path)+"/"+user+".png")
            j+=1
        except:
            bad_users.append(user)
            j+=1
    return bad_users



