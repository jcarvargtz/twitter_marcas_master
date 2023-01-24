import pandas as pd 
import  Scrape_functions.twitterUserGEOFULL as userGeoScrape
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


Aguascalientes = "Aguascalientes"
Baja_California = "Mexicali"
Baja_California_Sur = "La Paz"
Campeche = "Campeche"
Coahuila = "Saltillo"
Colima = "Colima"
Chiapas = "Tuxtla Gutiérrez"
Chihuahua = "Chihuahua"
Distrito_Federal = "Ciudad de México"
Durango = "Durango"
Guanajuato = "Guanajuato"
Guerrero = "Chilpancingo"
Hidalgo = "Pachuca"
Jalisco = "Guadalajara" 
Estado_de_Mexico = "Toluca"
Michoacan = "Morelia"
Morelos = "Cuernavaca"
Nayarit = "Tepic"
Nuevo_Leon = "Monterrey"
Oaxaca = "Oaxaca"
Puebla = "Puebla"
Queretaro = "Querétaro"
Quintana_Roo = "Chetumal"
San_Luis_Potosi = "San Luis Potosí" 
Sinaloa = "Culiacán"
Sonora = "Hermosillo"
Tabasco = "Villahermosa"
Tamaulipas = "Ciudad Victoria"
Tlaxcala = "Tlaxcala"
Veracruz = "Xalapa" 
Yucatan = "Mérida"
Zacatecas = "Zacatecas"


#definir busquedas

'''~~~FILL INFO BELOW THIS LINE~~~~'''
#noroeste = [Baja_California, Baja_California_Sur, Chihuahua, Sinaloa, Sonora]
#sureste = [Campeche, Chiapas, Guerrero, Oaxaca, Quintana_Roo, Tabasco, Veracruz, Yucatan]
#occidente = [Aguascalientes, Colima, Guanajuato, Jalisco, Michoacan, Nayarit, Queretaro, Zacatecas]
#noreste = [Coahuila, Durango, Nuevo_Leon, San_Luis_Potosi, Tamaulipas]
#centro =[Tlaxcala, Distrito_Federal, Estado_de_Mexico, Morelos, Puebla, Hidalgo]
noroeste = [Chihuahua, Sinaloa, Sonora] #Baja_California_Sur
sureste = [Oaxaca, Veracruz, Yucatan]# Guerrero
occidente = [Jalisco, Michoacan, Zacatecas]#Guanajuato]#
noreste = [Durango, Nuevo_Leon, Tamaulipas] #Coahuila
centro =[Estado_de_Mexico, Morelos, Puebla] #Distrito_Federal]

lugares = [noroeste, sureste, occidente, noreste, centro ]


output_path="ENTRENAMIENTO\BASES"
filename="Lugares.csv"

base=pd.DataFrame()# O LEER SI SE VA A CONTINUAR
base=pd.read_csv(os.path.join(output_path,filename))#PARA LEER

'''~~~FILL INFO ABOVE THIS LINE~~~~'''

for i in noroeste:
    base0=userGeoScrape.scrape_geo_full("a",201901010000, 201912010000,i)
    if base0.shape!=(0,0):
        base0["Region"]= ["Noroeste"]*base0.shape[0]
    base=base.append(base0)
    base.shape

if (os.path.exists(output_path)==False):
    os.mkdir(output_path)

base.to_csv( os.path.join(output_path,filename), index=False  )



import pandas as pd
base = pd.read_csv(r"ENTRENAMIENTO\BASES\Lugares.csv")
base.columns