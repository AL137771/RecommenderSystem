#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install multi-rake


# In[68]:


import pandas as pd
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import tkinter as tk


# In[69]:


pd.set_option('display.max_columns', 100)
ES = pd.read_csv('C:/Users/G50/Desktop/SRBCC/SRBCC/Inventario_English.spanish/inventario_spanish.csv', error_bad_lines=False, encoding="latin-1")
ES.head()


# In[70]:


ES = ES[['Titulo', 'autores', 'materia']]


# In[71]:


ES['materia'] =  ES['materia'].astype(str)


# In[72]:



#inicializando la columna
ES['palabras_clave'] = ""


for index, row in ES.iterrows():

    materia = row['materia']
    # instanciando rake, que utiliza las stopwords en el idioma ingles y descartando
    # puntuaciones
    r = Rake(language="spanish")
    
    
    # extrayendo a las palabras y pasandolas al texto 
    r.extract_keywords_from_text(materia)
    key_words_dict_scores = r.get_word_degrees()
    
    # asignando las palabras clave a la columna palabras_clave
    row['palabras_clave'] = list(key_words_dict_scores.keys())


# In[73]:


ES


# In[74]:


ES.drop(columns = ['materia'], inplace = True)


# In[75]:


ES.set_index('Titulo', inplace = True)


# In[76]:


ES['palabras'] = ''
columns = ES.columns


# In[77]:


for index, row in ES.iterrows():
    words = ''
    for col in columns:
        if col != 'autores':
            words = words + ' '.join(row[col])+ ''
        else:
            words = words + row[col]+ ' '
    row['palabras'] = words
    
ES.drop(columns = [col for col in ES.columns if col!= 'palabras'], inplace = True)


# In[78]:


count = CountVectorizer()
count_matrix = count.fit_transform(ES['palabras'])


# In[79]:


indices = pd.Series(ES.index)


cosine_sim = cosine_similarity(count_matrix, count_matrix)


# In[80]:


def recomendaciones(title, cosine_sim = cosine_sim):
    
    recomendaciones_peliculas = []
    
    # obteniendo el index que coincida con el titulo
    idx = indices[indices == title].index[0]
    # creando un listado con las puntuaciones de similitud en orden descendiente
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    # obteniendo los index de los libros mas similares
    top_5_indexes = list(score_series.iloc[1:11].index)
    
    # ciclo for que muestra los 5 libros mas parecidos
    for i in top_5_indexes:
        recomendaciones_peliculas.append(list(ES.index)[i])
        
    return recomendaciones_peliculas


# In[81]:


recomendaciones("mirada en dos tiempos")


# In[61]:


recomendaciones('pequeños contribuyentes fiscal 1')


# In[62]:


recomendaciones("capitan alatriste")


# In[63]:


recomendaciones("politico y el cientifico")


# In[ ]:




