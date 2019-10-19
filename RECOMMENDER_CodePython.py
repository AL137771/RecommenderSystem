import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

pd.set_option('display.max_columns', 100)
CU = pd.read_csv('C:/Users/G50/Desktop/RecommenderSystem/Inventario_English.spanish/inventario_english.csv', error_bad_lines=False, encoding="latin-1")
CU.head()

CU = CU[['Titulo','autores','materia']]


 #inicializando la columna
CU['palabras_clave'] = ""

for index, row in CU.iterrows():

    materia = row['materia']
    # instanciando rake, que utiliza las stopwords en el idioma ingles y descartando
    # puntuaciones
    r = Rake()

    # extrayendo a las palabras y pasandolas al texto 
    r.extract_keywords_from_text(materia)
    key_words_dict_scores = r.get_word_degrees()
    
    # asignando las palabras clave a la columna palabras_clave
    row['palabras_clave'] = list(key_words_dict_scores.keys())

# Eliminando la columna materia
CU.drop(columns = ['materia'], inplace = True)

CU.set_index('Titulo', inplace = True)


CU['palabras'] = ''
columns = CU.columns
for index, row in CU.iterrows():
    words = ''
    for col in columns:
        if col != 'autores':
            words = words + ' '.join(row[col])+ ''
        else:
            words = words + row[col]+ ' '
    row['palabras'] = words
    
CU.drop(columns = [col for col in CU.columns if col!= 'palabras'], inplace = True)



count = CountVectorizer()
count_matrix = count.fit_transform(CU['palabras'])

indices = pd.Series(CU.index)

indices = pd.Series(CU.index)

cosine_sim = cosine_similarity(count_matrix, count_matrix)

def recomendaciones(title, cosine_sim = cosine_sim):
    
    recomendaciones_peliculas = []
    
    # obteniendo el index que coincida con el titulo
    idx = indices[indices == title].index[0]
    # creando un listado con las puntuaciones de similitud en orden descendiente
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    # obteniendo los index de los libros mas similares
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    # ciclo for que muestra los l0 libros mas parecidos
    for i in top_10_indexes:
        recomendaciones_peliculas.append(list(CU.index)[i])
        
    return recomendaciones_peliculas
