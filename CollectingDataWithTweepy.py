# Tweepy
# Llamando a las librerias y recursos necesarios
# General:
import tweepy           # Twitter's API
import pandas as pd     # Para manejar DataFrames
import numpy as np

# Para ploteo y visualizacion:
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# Autenticando la api y credenciales de Twitter
# "Client_Tw.csv" es el nombre del archivo csv separado por columnas con el nombre de la llave, y en primer fila la llave
log = pd.read_csv("Client_Tw.csv")
log.head()

bearerToken = log["BearerToken"][0]
consumerKey = log['ConsumerKey'][0]
consumerSecret = log['ConsumerSecret'][0]
accessToken = log['AccesToken'][0]
accessTokenSecret = log['AccesTokenSecret'][0]

# Llamando al metodo API's:


def getAPI():

    # Autenticacion y acceso a llaves:
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    # Return API with authentication:
    # para mantener la conexion cuando se llegue al limite de la solicitud
    API = tweepy.API(auth, wait_on_rate_limit=True)
    return API


# Empleamos el método cursor en el siguiente simple algoritmo
# Un método de busqueda de tweets por contenido y locación para realizar análisis de sentimientos, por ejemplo

def searchTweets_cu(query, geocode='24.01362,-104.67530,400km', nitems=1000, to_csv=False, csv_name="archivo.csv", nhead=30):
    API = getAPI()

    # query es la palabra u oracion a buscar
    # geocode = '24.01362,-104.67530,400km'
    # aquí introducimos longitud y latitud de la zona a estudiar, seguido del diametro a cubrir
    # nitems = 1000 # aqui escribimos la cantidad de tweets a solicitar, aunque no siempre se recolecta la totalidad
    # to_csv, valor booleano si se desea descargar la solicitud
    # csv_name, el nombre para guardar el archivo en el formato deseado (usualmente csv)

    simple_list = []
    for tweet in tweepy.Cursor(API.search_tweets, q=query, geocode='24.01362,-104.67530,300km').items(nitems):
        simple_list.append([tweet.text, tweet.created_at, tweet.favorite_count, tweet.retweet_count,
                           tweet.user.location, [h['text'] for h in tweet.entities['hashtags']]])
    simple_list = pd.DataFrame(simple_list, columns=[
                               "Text", "Created at", "Likes", "Retweets", "Ubicación", "Hashtags"])

    try:
        if to_csv:
            simple_list.to_csv(csv_name)
    except:
        print(
            f"No se han producido archivos csv con el método ordenado, dado to_csv{to_csv}")

    return simple_list.head(50)


# Finalmente, aqui especificamos los parametros para realizar la busqueda
searchTweets_cu(query="@EVillegasV", to_csv=True, csv_name="@EVCG_D30.csv")
