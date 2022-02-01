from textblob import TextBlob
import pandas as pd
import csv
import re
import time
import string


from time import sleep
from textblob.exceptions import NotTranslated
from textblob.exceptions import TranslatorError
from deep_translator import GoogleTranslator


# Cargamos el archivo csv y visualizamos el head
# Dicho csv fue obtenido con el metodo cursor del archivo 'CollectingDataWithTweepy.csv'
df = pd.read_csv("Domingo3001_EVCG.csv")
df.head()

# Limpiando el texto


# Retirando hashtags, Rts, Https, guiones, barras y asteriscos

def clean_text(Text):
    Text = re.sub(r'^RT[\s]+', ' ', Text)
    Text = re.sub(r'https?:\/\/.*[\r\n]*', ' ', Text)
    Text = re.sub(r'#', ' ', Text)
    Text = re.sub(r'@[A-Za-z0-9]+', ' ', Text)
    Text = re.sub(r'_[A-Za-z0-9]+', ' ', Text)
    Text = re.sub(r'\. ', ' ', Text)
    Text = re.sub(r'\_ ', ' ', Text)
    Text = re.sub(r'\\ ', ' ', Text)
    Text = re.sub(r'\*', ' ', Text)
    return Text


df['cleaning_text'] = df['Text'].apply(clean_text)


# Retirando espacios duplicados en la cadena y otros caracteres

l = []
list(map(lambda x: l.append(x), df['cleaning_text']))

l2 = []
for s in l:  # MODIFICAR PARA RESTRINGIR TEXTOS MAYORES A 5000
    l2.append(re.sub(r"^\s+|\s+$", "", s))
l3 = []
for s in l:
    " ".join(s.split())
    l3.append(" ".join(s.split()))


df["cleaned"] = l3

nombre_persona = "Héctor"
nombrep_completo = "Héctor Flores"
nombrep_completo2 = "Héctor flores"

l4 = list(map(lambda x: "" if len(x) < len(nombre_persona) else x, l3))
l4 = list(map(lambda x: "" if x == nombrep_completo or x ==
          nombrep_completo2 else x, l4))

df["cleaned"] = l4

# RETIRANDO DUPLICADOS DEL DATAFRAME POR SUBSET CON DROP_DUPLICATES
print('anteriormente se tenian', len(df), 'filas')
df = df.drop_duplicates(subset="cleaning_text", keep="first")
print('actualmente, posterior a retirar duplicados, se tienen', len(df), 'filas')


#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_polaritiesTB(text):
    if len(text) > 1:
        try:
            translated = GoogleTranslator(
                source='auto', target='english').translate(text)
            analysis = TextBlob(translated)
            result = analysis.sentiment.polarity
            return result

        except:
            return str(0.0000001)


def get_polaritiesVS(text):
    try:
        if len(text) < 5000:
            translated = GoogleTranslator(
                source='auto', target='english').translate(text)
            vaderAnalyzer = SentimentIntensityAnalyzer().polarity_scores(translated)
            result = vaderAnalyzer
            return result['compound']

    except:
        return float(0.0000001)
        # se retorna cero porque es un texto mayor a 5000 chrt y Deeptl no es capaz de traducirlo


# Separamos el df en 10 dataframes para evitar que se atasque la traduccion
largo = len(df)
decima = int(len(df) * 0.1)

df1 = df.iloc[: decima, :]
df2 = df.iloc[decima: ((decima) * 2), :]
df3 = df.iloc[((decima) * 2): ((decima) * 3), :]
df4 = df.iloc[((decima) * 3): ((decima) * 4), :]
df5 = df.iloc[((decima) * 4): ((decima) * 5), :]
df6 = df.iloc[((decima) * 5): ((decima) * 6), :]
df7 = df.iloc[((decima) * 6): ((decima) * 7), :]
df8 = df.iloc[((decima) * 7): ((decima) * 8), :]
df9 = df.iloc[((decima) * 8): ((decima) * 9), :]
df10 = df.iloc[((decima) * 9):, :]


# Aplicamos los metodos de polaridad a cada texto de cada columna de cada dataframe

df1['polarityTB'] = df1['cleaned'].apply(get_polaritiesTB)
df1['polarityVS'] = df1['cleaned'].apply(get_polaritiesVS)

df2['polarityTB'] = df2['cleaned'].apply(get_polaritiesTB)
df2['polarityVS'] = df2['cleaned'].apply(get_polaritiesVS)

df3['polarityTB'] = df3['cleaned'].apply(get_polaritiesTB)
df3['polarityVS'] = df3['cleaned'].apply(get_polaritiesVS)

df4['polarityTB'] = df4['cleaned'].apply(get_polaritiesTB)
df4['polarityVS'] = df4['cleaned'].apply(get_polaritiesVS)

df5['polarityTB'] = df5['cleaned'].apply(get_polaritiesTB)
df5['polarityVS'] = df5['cleaned'].apply(get_polaritiesVS)

df6['polarityTB'] = df6['cleaned'].apply(get_polaritiesTB)
df6['polarityVS'] = df6['cleaned'].apply(get_polaritiesVS)

df7['polarityTB'] = df7['cleaned'].apply(get_polaritiesTB)
df7['polarityVS'] = df7['cleaned'].apply(get_polaritiesVS)

df8['polarityTB'] = df8['cleaned'].apply(get_polaritiesTB)
df8['polarityVS'] = df8['cleaned'].apply(get_polaritiesVS)

df9['polarityTB'] = df9['cleaned'].apply(get_polaritiesTB)
df9['polarityVS'] = df9['cleaned'].apply(get_polaritiesVS)

df10['polarityTB'] = df10['cleaned'].apply(get_polaritiesTB)
df10['polarityVS'] = df10['cleaned'].apply(get_polaritiesVS)


# Reunimos todos los dataframes en uno ya con polaridades

DF = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9])


# Finalmente guardamos en un archivo csv para seguir con el proceso

DF.to_csv("RES_EVCG_D3001.csv")
