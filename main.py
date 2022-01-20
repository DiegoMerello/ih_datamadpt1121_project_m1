import pandas as pd
import numpy as np
import requests as rq
from shapely.geometry import Point
import geopandas as gpd
import re
import os
import geopandas as gpd
import sys
import argparse

parser = argparse.ArgumentParser() #al igual que ls y mkdir, 
parser.add_argument(
    "--value",
    dest = "value",
    default = "Closest",
    help = "Execution parameter. Possibilites: Closest , AllTotems"
)
args = parser.parse_args(sys.argv[1:])

def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between to latitude/longitude pair point in degrees (i.e.: 40.392436 / -3.6994487)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish)
def distance_meters(mercator_start,mercator_finish):
    return mercator_start.distance(mercator_finish)

def sports_centres():
    instalaciones_dep_data=rq.get('https://datos.madrid.es/egob/catalogo/200215-0-instalaciones-deportivas.json')
    instalaciones_dep_data=instalaciones_dep_data.json()
    instalaciones_dep_data = pd.json_normalize(instalaciones_dep_data['@graph'])
    instalaciones_dep_data=instalaciones_dep_data.drop(['@id', '@type','id', 'relation', 'address.district.@id', 'address.area.@id', 'address.locality', 'address.postal-code', 'organization.organization-desc', 'organization.accesibility', 'organization.schedule', 'organization.services','organization.organization-name'], axis='columns')
    instalaciones_dep_data['address.street-address']=instalaciones_dep_data['address.street-address'].str.title()
    instalaciones_dep_data.dropna(subset=['location.latitude','location.longitude'], inplace=True)
    instalaciones_dep_data1=instalaciones_dep_data.rename(columns={'location.latitude':'lat_start','location.longitude':'long_start'})
    instalaciones_dep_data1["Punto Inicio"] = instalaciones_dep_data1.apply(lambda x: to_mercator(x["lat_start"],x["long_start"]), axis = 1)
    return instalaciones_dep_data1

def bicimad_stations():
    bicimad= pd.read_json("data/Estaciones.json")
    bicimad=bicimad.drop(['light', 'number', 'activate', 'no_available', 'total_bases', 'dock_bikes', 'free_bases','reservations_count','geometry_type'], axis='columns')
    bicimad['long_finish']=bicimad['geometry_coordinates'].map(lambda x:x.split(',')[0].replace('[','')).astype(float)
    bicimad['lat_finish']=bicimad['geometry_coordinates'].map(lambda x:x.split(',')[1].replace(']','')).astype(float)
    bicimad=bicimad.drop(['id','geometry_coordinates'],axis='columns')
    bicimad["Punto Final"] = bicimad.apply(lambda x: to_mercator(x["lat_finish"],x["long_finish"]), axis = 1)
    return bicimad

def clean_data():
    df_final = pd.merge(sports_centres(), bicimad_stations(), how='cross')
    df_final['Distancia']=df_final.apply(lambda x: distance_meters(x['Punto Inicio'], x['Punto Final']), axis=1)
    df_final1= df_final.drop(['lat_start','long_start','Punto Inicio', 'Punto Final', 'long_finish', 'lat_finish' ], axis='columns')
    df_final1=df_final1.rename(columns={'title':'Place of interest', 'address.street-address':'Place address','name':'BiciMAD station','address':'Station location'})
    df_final1.insert(1, 'Type of place', 'Instalación deportiva')
    return df_final1

def distancia_minima():
    x=str(input('Introduce una Instalación Deportiva: '))
    y = clean_data()[clean_data()['Place of interest']==x]
    return y.sort_values(by = "Distancia", ascending = True).groupby('Place of interest')['Place of interest','Type of place','Place address', 'Distancia','BiciMAD station', 'Station location'].nth(0).drop(["Distancia"], axis = "columns")

def bicimad_todas():
    return (clean_data().sort_values(by = "Distancia", ascending = True).groupby('Place of interest')['Type of place','Place address', 'Distancia','BiciMAD station', 'Station location'].nth(0).drop(["Distancia"], axis = "columns"))

if args.value == "Closest":
    min_distance = distancia_minima()
    # print(ubicacion_mas_cercana)
    min_distance.to_csv("data/min_distance.csv", sep= ";")
    print("Closest Totem saved in data file")
elif args.value == "AllTotems":
    all_totems = bicimad_todas()
    # print(distancias_ubicacion)
    all_totems.to_csv("data/all_totems.csv", sep= ";")
    print("All totems saved in data file")
else:
    print("Error, only: Closest or AllTotem")