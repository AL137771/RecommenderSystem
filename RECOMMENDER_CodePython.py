import pandas as pd
from multi_rake import Rake
import numpy as np

CU = pd.read_csv('INVENTARIO.csv', sep=';', error_bad_lines=False, encoding="latin-1")


CU['Key_words'] = ""

for index, row in CU.iterrows():
    materia = row['materia']


    r = Rake()

    r.extract_keywords_from_text(materia)

    key_words_dict_scores = r.get_word_degrees()

    row['Key_words'] =list(key_words_dict_scores.keys())

CU.drop(columns = ['materia'], inplace = True)

CU.set_index('Titulo', inplace = True)



df['bag_of_words'] = ''
columns = CU.columns
for index, row in df.iterrows():
    words = ''
    for col in columns:
        if col != 'autorPrincipal':
            words = words + ' '.join(row[col])+ ' '
        else:
            words = words + row[col]+ ' '
    row['bag_of_words'] = words
    
CU.drop(columns = [col for col in CU.columns if col!= 'bag_of_words'], inplace = True)
