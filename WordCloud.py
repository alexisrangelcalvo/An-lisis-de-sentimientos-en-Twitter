# STOPWORDS se importa para trabajar textos en ingles, esta limita la participacion de articulos definidos, nexos, etc...
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import re
import numpy as np


DF = pd.read_csv('26_01_EVCG.csv')
# LIMPIANDO POR ENCIMA LA COLUMNA 'CLEANED' PARA RETIRAR NOMBRES DE PERSONAS


def clean_text_names(Text):
    Text = re.sub(r'^RT[\s]+', ' ', Text)
    Text = re.sub(r'https?:\/\/.*[\r\n]*', ' ', Text)
    Text = re.sub(r'#', ' ', Text)
    Text = re.sub(r'@[A-Za-z0-9]+', ' ', Text)
    Text = re.sub(r'_[A-Za-z0-9]+', ' ', Text)
    Text = re.sub(r'\. ', '', Text)
    Text = re.sub(r'\@', '', Text)

    return Text


DF['cleaned'] = DF['cleaned'].fillna('').apply(str)
DF['cloud'] = DF['cleaned'].apply(clean_text_names)

text = ''.join(DF.cloud)


# Aqui definimos las palabras (ya que trabajaremos con texto en espanol) como articulos definidos y nexos que queremos no sean tomados en la frecuencia para imprimir la nube de terminos
empty_words = ["PAN", "pan", "Pan", "PRI", "Pri", "Villarreal", "pri", "con", "está", "las", "ni", "Esta", "será", "los", "más", "pero", "el", "la", "por",
               "del", "que", "y", "una", "un", "es", "de", "no", "si", "ah", "para", "en", "a", "se", "su", "lo", "le", "como", "al", "DESDE", "EnVivo", "Mi", "o"]

# Introducimos la forma deseada de la nube (requiere ser una imagen con fondo blanco y la figura un color notablemente diferente a blanco, si no es asi no saltara un error)
custom_mask = np.array(Image.open('shutterstock_1279963171.jpg'))
wc = WordCloud(background_color='white',
               stopwords=empty_words,
               mask=custom_mask)

wc.generate(text)
image_colors = ImageColorGenerator(custom_mask)
wc.recolor(color_func=image_colors)

# Plotting
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()  # para mostrar por pantalla, por ejemplo en jupyter notebook

# para descargar imagen en el ambiente del documento
wc.to_file('EV_SE_wordcloud.png')
