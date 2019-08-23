import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv('https://query.data.world/s/uikepcpffyo2nhig52xxeevdialfl7')
df.head()

#df.shape()

df = df[['Title','Genre','Director','Actors','Plot']]

#df.shape()

# se descargan las comas entre los actores, y se obtienen solo los primeros 3 nombres
df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])

# coloca los generos en una lista de palabras
df['Genre'] = df['Genre'].map(lambda x: x.lower().split(','))

df['Director'] = df['Director'].map(lambda x: x.split(' '))


for index, row in df.iterrows():
    row['Actors'] = [x.lower().replace(' ','') for x in row['Actors']]
    row['Director'] = ''.join(row['Director']).lower()


# creando la nueva columa donde iran las keywords
df['Key_words'] = ""

for index, row in df.iterrows():
    plot = row['Plot']
    
    
    r = Rake()

    # extrayendo las palabras y colocandolas en el texto
    r.extract_keywords_from_text(plot)

    # getting the dictionary whith key words and their scores
    key_words_dict_scores = r.get_word_degrees()
    
    # assigning the key words to the new column
    row['Key_words'] = list(key_words_dict_scores.keys())

# dropping the Plot column
df.drop(columns = ['Plot'], inplace = True)

df.set_index('Title', inplace = True)



df['bag_of_words'] = ''
columns = df.columns
for index, row in df.iterrows():
    words = ''
    for col in columns:
        if col != 'Director':
            words = words + ' '.join(row[col])+ ' '
        else:
            words = words + row[col]+ ' '
    row['bag_of_words'] = words
    
df.drop(columns = [col for col in df.columns if col!= 'bag_of_words'], inplace = True)



# instanciando y generando la matriz de conteo
count = CountVectorizer()
count_matrix = count.fit_transform(df['bag_of_words'])

# crea una serie para los titulos de las peliculas asi se pueden asociar a un orden numero
indices = pd.Series(df.index)
indices[:5]


# generando la matriz de similitud de coseno
cosine_sim = cosine_similarity(count_matrix, count_matrix)
cosine_sim

# funcion que toma el titulo de la pelicula como entrada y regrea las top 10 peliculas recomendadas
def recommendations(title, cosine_sim = cosine_sim):
    
    recommended_movies = []
    # obtiene el index de la pelicula que coincida con el titulo
    idx = indices[indices == title].index[0]

    # crea la serie con los resultados de similitud en orden descendiente
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    # obtiene los index de las 10 peliculas mas similares
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    for i in top_10_indexes:
        recommended_movies.append(list(df.index)[i])
        
    return recommended_movies
