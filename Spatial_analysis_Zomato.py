#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


data = pd.read_csv(r'/Users/gowthammarrapu/Documents/untitled folder 2/zomato.csv')


# In[ ]:


type(data)


# In[ ]:


data.columns,data.shape


# In[ ]:


data.duplicated().sum(),data.isnull().sum()


# In[ ]:


data.dropna(subset=['location'] , inplace = True)


# In[ ]:


data.isnull().sum()


# In[ ]:


df = data.copy()


# In[ ]:


df.head()


# In[ ]:


df['location'] = df['location'] + ' , Bangalore , Karnataka , India'


# In[ ]:


df['location']


# In[ ]:


df.dtypes


# In[ ]:


df.columns


# In[ ]:


rest_loc = pd.DataFrame()
rest_loc['Name'] = df['location'].unique()
rest_loc


# In[ ]:


from geopy.geocoders import Nominatim


# In[ ]:


geolocator = Nominatim(user_agent="app" , timeout=None )


# In[ ]:


lat = [] ## define lat list to store all the latitudes
lon = [] ## define lon list to store all the longitudes


for name in rest_loc['Name']:
    location = geolocator.geocode(name)
    
    if location is None:
        lat.append(np.nan)
        lon.append(np.nan)
        
    else:
        lat.append(location.latitude)
        lon.append(location.longitude)
print(lat)


# In[ ]:


rest_loc['lat'] = lat
rest_loc['lon'] = lon
rest_loc


# In[ ]:


rest_loc.isnull().sum() 


# In[ ]:


rest_loc['lat'].isnull()


# In[ ]:


rest_loc[rest_loc['lat'].isnull()]


# In[ ]:


import warnings
from warnings import filterwarnings
filterwarnings('ignore')


# In[ ]:


### for Rammurthy Nagar , Bangalore
### 13.0163° N, 77.6785° E


# In[ ]:


rest_loc['lat'][79] = 13.0163
rest_loc['lon'][79] = 77.6785


# In[ ]:


### for Sadashiv Nagar ,
### 13.0068 (Lat) & 77.5813(Lon)


# In[ ]:


rest_loc['lat'][85] = 13.0068
rest_loc['lon'][85] = 77.5813


# In[ ]:


rest_loc.isnull().sum()


# In[ ]:


geolocator = Nominatim(user_agent="app" , timeout=None )


# In[ ]:


df['address'][0]


# In[ ]:


loc = geolocator.geocode(df['address'][0])


# In[ ]:


hasattr(loc , 'latitude')

## hasattr(loc,'latitude')  Return whether the loc has an attribute of latitude or not..

### it means address doesn't have any property as latitude , ie it is unable to find any geo-graphical for address feature..


# In[ ]:


'''now how to find geo-graphical co-ordinates of address feature..For this u have to use structured query ...
For a structured query, provide a dictionary whose keys
    are like: `street`, `city`, `county`, `state`, `country`, or
    `postalcode`'''


# In[ ]:


address = {'street':'21st Main Road' , 'city':'Bangalore' , 'country':'India' , 'state':'Karnataka'}


# In[ ]:


address_geocode = geolocator.geocode(address)


# In[ ]:


hasattr(address_geocode , 'latitude')


# In[ ]:


hasattr(address_geocode , 'longitude')


# In[ ]:


address_geocode.latitude


# In[ ]:


address_geocode.longitude


# In[ ]:


### where are most number of restaurants located in Bengalore


# In[ ]:


df['location'].value_counts()


# In[ ]:


type(df['location'].value_counts())


# In[ ]:


Rest_locations = df['location'].value_counts().reset_index()


# In[ ]:



Rest_locations.rename(columns={'index': 'Name'}, inplace=True)


# In[ ]:


### Now we can say that These are my locations where most of my restaurants are located..


# In[ ]:


'''
lets create Heatmap of this results so that it becomes more user-friendly..
now In order to perform Spatial Anlysis(Geographical Analysis) , we need latitudes & longitudes of every location..
'''


# In[ ]:


rest_loc


# In[ ]:


Beng_rest_locations = Rest_locations.merge(rest_loc , on="Name")


# In[ ]:


type(Beng_rest_locations)


# In[ ]:


Beng_rest_locations.head(5)


# In[ ]:


Beng_rest_locations.rename(columns={'location': 'count'}, inplace=True)


# In[ ]:


import folium


# In[ ]:


def Generate_basemap():
    basemap = folium.Map(location=[12.97 , 77.59])
    return basemap


# In[ ]:


basemap = Generate_basemap()


# In[ ]:


basemap


# In[ ]:


from folium.plugins import HeatMap


# In[ ]:


Beng_rest_locations.columns


# In[ ]:


Beng_rest_locations[['lat', 'lon' , 'count']]


# In[ ]:


HeatMap(Beng_rest_locations[['lat', 'lon' , 'count']]).add_to(basemap)


# In[ ]:


basemap


# In[ ]:




