import pandas as pd


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
