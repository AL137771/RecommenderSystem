import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

books = pd.read_csv('books.csv', sep=';', error_bad_lines=False, encoding="latin-1")

books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher'
                    , 'imageUrlS', 'imageUrlM', 'imageUrlL']


#print books.shape

books.drop(['imageUrlS', 'imageUrlM', 'imageUrlL'], axis=1, inplace=True)

#books.head()
#books.dtypes


books.loc[books.ISBN == '0789466953','yearOfPublication'] = 2000
books.loc[books.ISBN == '0789466953','bookAuthor'] = "James Buckley"
books.loc[books.ISBN == '0789466953', 'publisher'] = "DK Publishing Inc"
books.loc[books.ISBN == '0789466953', 'bookTitle' ] = "Dk Readers: Creating the X-Men, How comic books came to life(level 4, Proficient Readers)"


books.loc[books.ISBN == '078946697X','yearOfPublication'] = 2000
books.loc[books.ISBN == '078946697X','bookAuthor'] = "Michael Teitelbaum"
books.loc[books.ISBN == '078946697X', 'publisher'] = "DK Publishing Inc"
books.loc[books.ISBN == '078946697X', 'bookTitle' ] = "Dk Readers: Creating the X-Men, How it all began(level 4, Proficient Readers)"

books.loc[books.ISBN == '2070426769','yearOfPublication'] = 2003
books.loc[books.ISBN == '2070426769','bookAuthor'] = "Jean Marie Gustave Le"
books.loc[books.ISBN == '2070426769', 'publisher'] = "Gallimard"
books.loc[books.ISBN == '2070426769', 'bookTitle' ] = "Peuple de ciel, sulvi de 'Les Bergers'"



books.yearOfPublication=pd.to_numeric(books.yearOfPublication, errors='coerce')

# sorted(books['yearOfPublication'].unique())


books.loc[(books.yearOfPublication > 2006)|(books.yearOfPublication == 0), 'yearOfPublication'] = np.NAN
books.yearOfPublication.fillna(round(books.yearOfPublication.mean()), inplace=True)

books.yearOfPublication = books.yearOfPublication.astype(np.int32)

books.loc[(books.ISBN == '193169656X'), 'publisher'] = 'other'
books.loc[(books.ISBN == '1931696993'), 'publisher'] = 'other'




# RATINGS

users = pd.read_csv('users.csv', sep=';', error_bad_lines=False, encoding="latin-1")

users.columnos = ['userID', 'Location', 'Age']

users.loc[(users.Age > 90)|(users.Age < 5), 'Age'] = np.nan
users.Age = users.Age.fillna(users.Age.mean())
users.Age = users.Age.astype(np.int32)

#RATINGS

ratings = pd.read_csv('ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
ratings.columns = ['userID', 'ISBN', 'bookRating']

n_users = users.shape[0]
n_books = books.shape[0]

ratings_new = ratings[ratings.ISBN.isin(books.ISBN)]
ratings_new = ratings_new[ratings_new.userID.isin(users.userID)]

sns.countplot(data=ratings_explicit, x='bookRating')
#print ratings.shape
#print ratings_new.shape

sparsity=1.0-len(ratings_new)/float(n_users*n_books)

ratings_explicit = ratings_new[ratings_new.bookRating != 0]
ratings_explicit = ratings_new[ratings_new.bookRating == 0]

users_exp_ratings = users[users.userID.isin(ratings_explicit.userID)]
users_imp_ratings = users[users.userID.isin(ratings_implicit.userID)]
