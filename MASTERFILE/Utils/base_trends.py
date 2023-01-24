"""
TODO: falta agregar opcion para salvar la info
"""
import pandas as pd
import numpy as np
from pytrends.request import TrendReq
from datetime import datetime
import json

class trends:
    def __init__(self,brand,start,end,agg_locs,loc_dict):
        self.brand=brand
        # self.trends = TrendReq(hl="MX", tz=360,timeout=(10,25),retries=10, backoff_factor=0.1)
        self.start=start
        self.end=end
        # self.data=pd.DataFrame()
        self.agg_locs=agg_locs
        self.data = {}
        self.dict = loc_dict

    def save(self,output_path):
        with open(str(output_path),"w") as fp:
            json.dump(self.data,fp,indent=4)
    
    def search(self):
        if type(self.agg_locs) != list:
            self.agg_locs=[self.agg_locs]
        for loc in self.agg_locs:
            print(loc)
            print(self.get_geo_code(self.dict,str(loc)))
            trends = TrendReq(hl="es-MX", tz=360,timeout=(10,25),retries=10, backoff_factor=0.1)
            trends.build_payload(kw_list=[self.brand],
                                        cat=0,
                                        timeframe="{} {}".format(self.start,self.end),
                                        geo=str(self.get_geo_code(self.dict,str(loc))))
            print(loc)
            self.data[str(loc)] = json.loads(trends.interest_over_time().drop(labels=['isPartial'],axis='columns').to_json(indent=4, orient="index"))

    def get_geo_code(self, dict,loc):
        return dict[str(loc)]
        
    def get_data(self):
        return self.data

import yaml
with open("MASTERFILE/config.yml") as f:
    config = yaml.safe_load(f)



trends_tiempo = trends("BBVA")

class pytrendReg_tiempo:
    def __init__(self,brand_):
            self.brand = brand_
            # self.trends = TrendReq(hl="MX", tz=360,timeout=(10,25),retries=10, backoff_factor=0.1)
            # self.data=pd.DataFrame()
            self.data = []
            self.data_reg = []
            
    
    def search(self,start,end):
        trends = TrendReq(hl="es-MX", tz=360,timeout=(10,25),retries=10, backoff_factor=0.1)
        trends.build_payload(kw_list=[self.brand],cat=0,
                                        timeframe="{} {}".format(start,end),
                                        geo=str('MX'))
        df_edo = trends.interest_by_region()
        df_edo = df_edo.rename(columns={self.brand:"Vol_Trends"})
        #self.datajson = df_edo.to_json(orient="index", force_ascii=False)
        self.data = df_edo
    
    def save(self,output_path):
        with open(str(output_path),"w") as fp:
            json.dump(self.data,fp,indent=4)

    def regionalize(self):
        data_region = self.MascaraRegion(self.data)
        self.data_reg = data_region.groupby(["Region"]).agg(['mean'])

    def MascaraRegion(self,df):
        df = df.reset_index().rename(columns={"geoName":"Estado"})
        noroeste = ["Baja California", "Baja California Sur", "Chihuahua", "Sinaloa" ,"Sonora"]
        sureste = [ "Campeche", "Chiapas", "Guerrero","Oaxaca", "Quintana Roo","Tabasco", "Veracruz", "Yucatán"]
        occidente = ["Aguascalientes", "Colima", "Guanajuato", "Jalisco", "Michoacán", "Nayarit", "Querétaro", "Zacatecas"]
        noreste = ["Coahuila de Zaragoza", "Durango", "Nuevo León", "San Luis Potosí", "Tamaulipas"]
        #centro =["Tlaxcala", "Ciudad de México", "Estado de México", "Morelos", "Puebla", "Hidalgo"]
        df["Region"] = ["Noroeste" if i in noroeste else "SurEste" if i in sureste else "Occidente" if i in occidente else "Noreste" if i in noreste else "Centro" for i in df["Estado"] ]
        return (df)


    
        
        
ejemplo = pytrendReg_tiempo("BBVA")
ejemplo.search("2020-01-01","2020-05-01")
ejemplo.regionalize()
ejemplo.data_reg
ejemplo.save()



sum=0
regiones = config['variables']['vars']['agg_locs']['region']
for region in regiones.keys():
    for estado in regiones[region]:
        ej_data =  json.loads(ejemplo.data)
        sum = sum + ej_data[estado]["Vol_Trends"]
    promedio = sum/len(regiones[region])
    data_region[region] = {"Vol_Trend_avg": promedio}








trends_tiempo = trends("BBVA","2020-01-01","2020-05-01",config["variables"]["vars"]["agg_locs"]["estado"],config["variables"]["vars"]["dict_estado_codigo"])
trends_tiempo.search()
trends_tiempo.data
trends_tiempo.save("BBVAHackathon/Data/trends_tiempo.json")

a.get_geo_code(config["variables"]["vars"]["dict_estado_codigo"],"Aguascalientes")[3:]
config["variables"]["vars"]["agg_locs"].keys()
config["variables"]["vars"]["dict_estado_codigo"]
from pytrends.request import TrendReq
TrendReq()
end = "2020-05-01"
dt=datetime.strptime(end,"%Y-%m-%d")
dt.date()