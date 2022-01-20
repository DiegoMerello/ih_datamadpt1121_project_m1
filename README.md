<p align="left"><img src="https://cdn-images-1.medium.com/max/184/1*2GDcaeYIx_bQAZLxWM4PsQ@2x.png"></p>

# __ih_datamadpt1121_project_m1__Diego Merello

## **Data:**

There are 2 main datasources:

- **Azure SQL Database.** The database contains information from the BiciMAD stations including their location (i.e.: latitude / longitude). In order to access the database you may need the following credentials:
```
Server name:   sqlironhack
Database:      BiciMAD
```
>The obtained data reveal all BiciMad stations (coordinates locations, availability) from Madrid (Spain)

- **API REST.** We will use the API REST from the [Portal de datos abiertos del Ayuntamiento de Madrid](https://datos.madrid.es/nuevoMadrid/swagger-ui-master-2.2.10/dist/index.html?url=/egobfiles/api.datos.madrid.es.json#/), 

> Sport centre table and location from Madrid city free data


---

## **Main Challenge:**

Firstly, data of sports centres is cleaned. Useless columns are dropped. 
Secondly, values from address.street-address are transformed into string, then every word is capitalized
Since I had NaN values at certain columns I've dropped them to have no probs
I renamed columns since they are going to be my start point just to make them prettier and applied function to covert 2D points into mercator projection

Data from BiciMAD is cleand dropping useless columns, lamba function is applied to split up values from one column, additionally, integres are converted into float numbers since it was needed.
Following same reasony as above, I converted 2D coordinates into mercator coordinates

Both datasets are merged into one, so every location is crossed with every BiciMAD Station.
Columns are renamed to specific output. And a new column is inserted with the type of place.

## **Output**

There are two option:

1. With one specific Place of Interest, the closest BiciMAD station is found
2. The closest BiciMAD station to every Place of Interest 
3. At Visual Studio Code, a pipeline is created and with the argparse function. By default is ask the closest station to a specific Place of Interest.

 
## **Project Main Stack**

- [Azure SQL Database](https://portal.azure.com/)

- [SQL Alchemy](https://docs.sqlalchemy.org/en/13/intro.html) (alternatively you can use _Azure Data Studio_)

- [Requests](https://requests.readthedocs.io/)

- [Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/index.html)

- Module `geo_calculations.py`

- [Argparse](https://docs.python.org/3.7/library/argparse.html)












 


 

