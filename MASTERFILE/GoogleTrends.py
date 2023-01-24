from pytrends.request import TrendReq
import pandas as pd
import time
startTime = time.time()



def GTrend_interesTime(brand_, date_from_, date_to_, lang_="es", geo_="MX", cat_=0):
     '''
     dates format: string-> yyyy-mm-dd
     cat : https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
     '''
     pytrend = TrendReq(hl='%s-%s'%(lang_,geo_), tz=360)
     brand = [brand_]
     pytrend.build_payload(kw_list=brand,
     cat=cat_,
     timeframe='%s %s'%(date_from_,date_to_),
     geo=geo_)
     data = pytrend.interest_over_time()
     if not data.empty:
          data = data.drop(labels=['isPartial'],axis='columns')

     return(data)
     
data = GTrend_interesTime("BBVA", "2020-01-01","2020-05-01")
data.columns=["Freq"]
data1 = data.reset_index()
data1.to_json(orient="index")
brand = ["BBVA"]
data[brand]