#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests as rq
from shapely.geometry import Point
import geopandas as gpd
import re
import os 


# In[2]:


import geopandas as gpd


# In[3]:


def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c


# In[4]:


instalaciones_dep_data=rq.get('https://datos.madrid.es/egob/catalogo/200215-0-instalaciones-deportivas.json')
instalaciones_dep_data=instalaciones_dep_data.json()
instalaciones_dep_data


# In[5]:


instalaciones_dep_data = pd.json_normalize(instalaciones_dep_data['@graph'])
instalaciones_dep_data.head()


# In[6]:


#Hay que llamar a la API, y normalizar los valores de longitud y latitud

#instalaciones_dep_data= pd.read_csv("../ih_datamadpt1121_project_m1/200215-0-instalaciones-deportivas.csv", sep=';')
#instalaciones_dep_data


# In[7]:


instalaciones_dep_data=instalaciones_dep_data.drop(['@id', '@type','id', 'relation', 'address.district.@id', 'address.area.@id', 'address.locality', 'address.postal-code', 'organization.organization-desc', 'organization.accesibility', 'organization.schedule', 'organization.services','organization.organization-name'], axis='columns')
instalaciones_dep_data


# In[8]:


instalaciones_dep_data['address.street-address']=instalaciones_dep_data['address.street-address'].str.title()
#instalaciones_dep_data['NUM'] = instalaciones_dep_data['NUM'].replace(np.nan, 'S/N')
instalaciones_dep_data.dropna(subset=['location.latitude','location.longitude'], inplace=True)
#instalaciones_dep_data['Type of Place'] = "Instalación Deportiva"
instalaciones_dep_data


# In[9]:


instalaciones_dep_data.info()


# In[10]:


instalaciones_dep_data1=instalaciones_dep_data.rename(columns={'location.latitude':'lat_start','location.longitude':'long_start'})


# In[11]:


instalaciones_dep_data1["Punto Inicio"] = instalaciones_dep_data1.apply(lambda x: to_mercator(x["lat_start"],x["long_start"]), axis = 1)
instalaciones_dep_data1


# In[12]:


bicimad= pd.read_json("../ih_datamadpt1121_project_m1/Estaciones.json")

bicimad


# In[13]:


bicimad=bicimad.drop(['light', 'number', 'activate', 'no_available', 'total_bases', 'dock_bikes', 'free_bases','reservations_count','geometry_type'], axis='columns')
bicimad


# In[14]:


bicimad['LONGITUD']=bicimad['geometry_coordinates'].map(lambda x:x.split(',')[0].replace('[','')).astype(float)
bicimad['LATITUD']=bicimad['geometry_coordinates'].map(lambda x:x.split(',')[1].replace(']','')).astype(float)
bicimad=bicimad.drop(['id','geometry_coordinates'],axis='columns')
bicimad


# In[15]:


bicimad1=bicimad.rename(columns={'LATITUD':'lat_finish','LONGITUD':'long_finish'})


# In[16]:


bicimad1["Punto Final"] = bicimad1.apply(lambda x: to_mercator(x["lat_finish"],x["long_finish"]), axis = 1)
bicimad1


# In[17]:


def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between to latitude/longitude pair point in degrees (i.e.: 40.392436 / -3.6994487)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish)
def distance_meters(mercator_start,mercator_finish):
    return mercator_start.distance(mercator_finish)


# In[24]:


bicimad1


# In[25]:


instalaciones_dep_data1


# In[27]:


df_final = pd.merge(instalaciones_dep_data1, bicimad1, how='cross')
df_final


# In[32]:


#tabla_combinada = instalaciones_dep_data1().merge(bicimad1(),  how='cross') 
df_final['Distancia']=df_final.apply(lambda x: distance_meters(x['Punto Inicio'], x['Punto Final']), axis=1)
df_final
df_final= df_final.drop(['lat_start','long_start','Punto Inicio', 'Punto Final', 'long_finish', 'lat_finish' ], axis='columns')


# In[33]:


df_final


# In[ ]:


#dt=pd.merge(instalaciones_dep_data1,bicimad1, how='cross')
#dt


# In[ ]:


x=str(input('Introduce una Instalación Deportiva: '))
y= df_final()[df_final()]['title'==x]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




