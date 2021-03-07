from lyricsgenius import Genius

import pandas as pd
import string
import json

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords


def search_library(artist, name,token):

    """
    query = artist
    n = number of songs
    token = access token for genius api
    """

    api = Genius(token)



    list_lyrics = []
    list_title = []
    list_artist = []
    list_album = []
    list_year = []

    album = api.search_album(artist, name)
    fileNameWithExtension = "Lyrics_" + artist + ".json"
    fileName = artist + ".json"
    album.save_lyrics(filename=artist, extension="json")

    # lyrics outputed to json file
    # json to csv




    data = json.load(open(fileName))

    tracks = data["tracks"]

    df = pd.DataFrame(tracks)


    title = [sub['song']['title']for sub in tracks]

    lyrics = [sub['song']['lyrics'] for sub in tracks]

    albumName = data['name']


    df.insert(2,'album', albumName)
    df.insert(0, 'title', title)
    df.insert(1,'lyrics', lyrics)





    return df

def clean_lyrics(df,column):
    """
    This function cleans the words without importance and fix the format of the  dataframe's column lyrics 
    parameters:
    df = dataframe
    column = name of the column to clean
    """
    df = df
    df[column] = df[column].str.lower()
    df[column] = df[column].str.replace(r"verse |[1|2|3]|chorus|bridge|outro|intro","").str.replace("[","").str.replace("]","")
    df[column] = df[column].str.lower().str.replace(r"instrumental|intro|guitar|solo","")
    df[column] = df[column].str.replace("\n"," ").str.replace(r"[^\w\d'\s]+","").str.replace("efil ym fo flah","")
    df[column] = df[column].str.strip()

    return df

def lyrics_to_words(document):
    """
    This function splits the text of lyrics to  single words, removing stopwords and doing the lemmatization to each word
    parameters:
    document: text to split to single words
    """
    stop_words = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stopwordremoval = " ".join([i for i in document.lower().split() if i not in stop_words])
    punctuationremoval = ''.join(ch for ch in stopwordremoval if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punctuationremoval.split())
    return normalized
