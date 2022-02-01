import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Jonh Smith")

# Cargando el df generado en TextBlob-Vader o CollectindDataWithTweepy para obtener coordenadas de los tweets emitidos
DF = pd.read_csv("ARCHIVO.csv")

# Probando Geopy para obtener la información geográfica de un lugar por nombre
location = geolocator.geocode('Lerdo, Durango')
print(location)

# Obtenindo latitudes y longitudes
print((location.latitude, location.longitude))


# Definiendo metodos para sacar las coordenadas en conjunto y por separado

def long_lat(loc):
    try:
        if type(loc) == type('string'):
            location = geolocator.geocode(loc)
            return (location.latitude, location.longitude)
    except:
        return ""


def lat_place(loc):
    try:
        if type(loc) == type('string'):
            location = geolocator.geocode(loc)
            return (location.latitude)
    except:
        return ""


def long_place(loc):
    try:
        if type(loc) == type('string'):
            location = geolocator.geocode(loc)
            return (location.longitude)
    except:
        return ""


# Aplicando los metodos para obtener coordenadas
l = DF['Ubicación']
coordenadas = list(map(lambda x: long_lat(x), l))
latitud = list(map(lambda x: lat_place(x), l))
longitud = list(map(lambda x: long_place(x), l))

DF.insert(loc=9, column='coords', value=coordenadas)
DF.insert(loc=10, column='Latitud', value=latitud)
DF.insert(loc=11, column='Longitud', value=longitud)


m = DF_light.coords.value_counts()
m = m.to_dict()


# sentiemiento como diccionario
sentimiento = []
for c in cordinates:
    filt = DF_light['coords'] == c
    daf = DF_light.loc[filt]
    x = daf.sentimiento.value_counts()
    x = x.to_dict()
    sentimiento.append(x)


# Obteniendo listas de coordenadas, locación y frecuencia para crear un DF mas ligero, que emplearemos en QGIS
cordinates = []
frequency = []

for key in m:
    cordinates.append(key)
    frequency.append(m[key])


freq_ID = pd.DataFrame(list(zip(cordinates, latitud, longitud, frequency)), columns=[
                       "Coordenadas", "Latitud", "Longitud", "Tweets recabados"])

# sentiemiento como diccionario
sentimiento = []
for c in cordinates:
    filt = DF_light['coords'] == c
    daf = DF_light.loc[filt]
    x = daf.sentimiento.value_counts()
    x = x.to_dict()
    sentimiento.append(x)


# PARA OBTENER LISTAS DE LOS SENTIMIENTOS Y APILARLAS AL DATAFRAME
# Para obtener listas (3) de los sentimientos (Neutro, Positivo, Negativo) e insertarlas al nuevo df freq_ID
def polaridad(sentimiento, dicc):
    valor = dicc.get(sentimiento)
    return valor


Neutral = []
for i in range(0, len(sentimiento)):
    try:
        opinion = 'Neutra'
        x = polaridad(opinion, sentimiento[i])
        Neutral.append(x)
    except:
        Neutral.append(0)

Positive = []
for i in range(0, len(sentimiento)):
    try:
        opinion = 'Positiva'
        x = polaridad(opinion, sentimiento[i])
        Positive.append(x)
    except:
        Positive.append(0)

Negative = []
for i in range(0, len(sentimiento)):
    try:
        opinion = 'Negativa'
        x = polaridad(opinion, sentimiento[i])
        Negative.append(x)
    except:
        Negative.append(0)


# Rellenando NaNs

freq_ID['Neutral'] = Neutral
freq_ID['Neutral'] = freq_ID['Neutral'].fillna(0)
Neutral = freq_ID['Neutral']

freq_ID['Positive'] = Positive
freq_ID['Positive'] = freq_ID['Positive'].fillna(0)
Positive = freq_ID['Positive']

freq_ID['Negative'] = Negative
freq_ID['Negative'] = freq_ID['Negative'].fillna(0)
Negative = freq_ID['Negative']

Total = list(map(lambda x, y, z: x + y + z, Neutral, Positive, Negative))

# Porcentaje de positivos

freq_ID['Total'] = Total
PositiveAsPercentage = list(map(lambda x, y: (100 * x) / y, Positive, Total))
freq_ID['PositiveAsPercentage'] = PositiveAsPercentage

# Porcentaje de negativos

NegativeAsPercentage = list(map(lambda x, y: (100 * x) / y, Negative, Total))
freq_ID['NegativeAsPercentage'] = NegativeAsPercentage

# Porcentaje de neutros

NeutralAsPercentage = list(map(lambda x, y: (100 * x) / y, Neutral, Total))
freq_ID['NeutralAsPercentage'] = NeutralAsPercentage


# Descargando finalmente el csv a utilizar en QGIS
freq_ID.to_csv('freq_ID.CSV')
