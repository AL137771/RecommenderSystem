#!/usr/bin/env python
# coding: utf-8

# In[192]:


#pip install wx


# In[213]:


import pandas as pd
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import tkinter


# In[214]:


pd.set_option('display.max_columns', 100)
ES = pd.read_csv('C:/Users/G50/Desktop/SRBCC/SRBCC/Inventario_English.spanish/inventario_spanish.csv', error_bad_lines=False, encoding="latin-1")
ES.head()


# In[215]:


ES = ES[['Titulo', 'autores', 'materia']]


# In[216]:


ES['materia'] =  ES['materia'].astype(str)


# In[217]:


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


# In[218]:


ES = ES.drop("materia", axis=1)


# In[219]:


ES.set_index('Titulo', inplace = True)


# In[220]:


ES['palabras'] = ''
columns = ES.columns

for index, row in ES.iterrows():
    words = ''
    for col in columns:
        if col != 'autores':
            words = words + ' '.join(row[col])+ ''
        else:
            words = words + row[col]+ ' '
    row['palabras'] = words
    
ES.drop(columns = [col for col in ES.columns if col!= 'palabras'], inplace = True)


# In[221]:


count = CountVectorizer()
count_matrix = count.fit_transform(ES['palabras'])


# In[222]:


indices = pd.Series(ES.index)

cosine_sim = cosine_similarity(count_matrix, count_matrix)


# In[223]:


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


# In[224]:


recomendaciones("mirada en dos tiempos")


# In[225]:


recomendaciones('pequeños contribuyentes fiscal 1')


# In[314]:


recomendaciones("capitan alatriste")


# In[354]:


count = CountVectorizer()
count_matrix = count.fit_transform(ES['palabras'])    
        
indices = pd.Series(ES.index)
cosine_sim = cosine_similarity(count_matrix, count_matrix)

from tkinter import *


def hi():
    global dave
    dave = startEntry.get()

def recomendaciones(cosine_sim = cosine_sim):
    
    recomendaciones_peliculas = []
    
    # obteniendo el index que coincida con el titulo
    idx = indices[indices == dave].index[0]
    # creando un listado con las puntuaciones de similitud en orden descendiente
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    # obteniendo los index de los libros mas similares
    top_5_indexes = list(score_series.iloc[1:6].index)
    
    # ciclo for que muestra los 5 libros mas parecidos
    for i in top_5_indexes:
        recomendaciones_peliculas.append(list(ES.index)[i])
        
    
    label.config(text=recomendaciones_peliculas)


frame = Tk()
frame.title("Sistema de recomendacion")
frame.geometry("800x300")
frame.config(bg="#AEB6BF")
imagen=PhotoImage(file="book.png")
titulo = Label(frame, text="Sistema de recomendacion de la biblioteca de CU",  font=(20))
titulo.place(x=300, y=100)
titulo.pack()

startLabel =Label(frame,text="Ingresa un libro de tu preferencia: ")
startLabel.place(x=250, y=250)

labelR=Label(frame, text="Recomendaciones:", bg="white", fg='black')
labelR.place(x=25, y=150)
label=Label(frame,text='...',bg='black',fg='white')
label.place(x=25,y=180)

startEntry=Entry(frame)


startLabel.pack()
startEntry.pack()

plotButton= Button(frame,text="Guardar", command=hi)
plotButton.config(fg = "black", bg = "white")
plotButton2= Button(frame,text="Obtener recomendaciones", command=recomendaciones)
plotButton2.config(fg = "white", bg = "black")

plotButton.pack()
plotButton2.pack()

frame.mainloop()


# In[ ]:




