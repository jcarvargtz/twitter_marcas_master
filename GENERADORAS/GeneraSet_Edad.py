import pandas as pd 
import  Scrape_functions.userScrape as userScrape
import os
from itertools import product
'''
estados=["Aguascalientes", "Baja California", "Baja California Sur", "Chiapas","Campeche",
"Chihuahua","Coahuila","Colima","Durango","Guanajuato",
"Guerrero","Hidalgo","Jalisco","Estado de México","Michoacán",
"Morelos","Nayarit","Nuevo León","Oaxaca","Puebla",
"Querétaro","Quintana Roo","San Luis Potosí","Sinaloa","Sonora",
"Tabasco","Tamaulipas","Tlaxcala","Veracruz","Yucatán",
"Zacatecas","Ciudad de Mexico"]
'''
cumple_frase=["cumplo","micumple","años"]

edades=range(15,60)
cumples=pd.DataFrame(list(product(cumple_frase, edades)), columns=['cumple', 'edades'])
cumples["busqueda"]=cumples["cumple"]+ cumples["edades"].apply(str)
busca_cumple=cumples["busqueda"]
busca_cumple.str[-2:]

'''~~~FILL INFO BELOW THIS LINE~~~~'''
busqueda=(busca_cumple)###
#complemento=range(20,30)
output_path="ENTRENAMIENTO\BASES"
filename="Edades.csv"

base=pd.DataFrame()# O LEER SI SE VA A CONTINUAR
base=pd.read_csv(os.path.join(output_path,filename))#PARA LEER

'''~~~FILL INFO ABOVE THIS LINE~~~~'''
busqueda[0][-2:]

for i in busqueda:
    base0=userScrape.ScrapeTW(i, output_path, nUsers=10, nTweetsxUs=15, guardar=False)
    if base0.shape!=(0,0):
        base0["Edad"]= i[-2:]
    base=base.append(base0)
    base.shape


if (os.path.exists(output_path)==False):
    os.mkdir(output_path)

base.to_csv( os.path.join(output_path,filename), index=False  )




