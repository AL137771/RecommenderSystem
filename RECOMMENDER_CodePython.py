import pandas as pd
from multi_rake import Rake
import numpy as np

cu = pd.read_csv('inventario.csv', sep=';', error_bad_lines=False, encoding="latin-1")

# discarding the commas between the actors' full names and getting only the first three names
#cu['autores'] = cu['autores'].map(lambda x: x.split(',')[:3])


# merging together first and last name for each actor and director, so it's considered as one word 
# and there is no mix up between people sharing a first name
#for index, row in cu.iterrows():
 #   row['autores'] = [x.lower().replace(' ','') for x in row['autores']]


  # initializing the new column
cu['Key_words'] = ""

for index, row in cu.iterrows():
    plot = row['materia']
    
    # instantiating Rake, by default is uses english stopwords from NLTK
    # and discard all puntuation characters
    r = Rake()

    # extracting the words by passing the text
    r.extract_keywords_from_text(materia)

    # getting the dictionary whith key words and their scores
    key_words_dict_scores = r.get_word_degrees()
    
    # assigning the key words to the new column
    row['Key_words'] = list(key_words_dict_scores.keys())

# dropping the Plot column
cu.drop(columns = ['materia'], inplace = True)  

cu
