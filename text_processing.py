# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:47:23 2022

@author: AS00340968
"""

import pandas as pd
import numpy as np

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

import TensorFlow



def text_preprocess(series, stemmer, stopwords):
    df = series.str.replace("\n\t",  " ")
    df = df.str.replace(r"[^a-zA-Z ]+", "")
    df = df.str.lower()
    df = df.apply(lambda x: ' '.join([stemmer.stem(item) for item in x.split() if item not in stopwords])) 
    return df
    
# Download first from Kaggle    
data = pd.read_csv('email_set.csv')

# Get stopwords and create stemmer using Sastrawi
stopwords = StopWordRemoverFactory().get_stop_words()
stemmer = StemmerFactory().create_stemmer()

# Preprocess the sentences
data['processed_text'] = text_preprocess(data['subject'], stemmer, stopwords)

# Build word embedding model and create one more with dim=3 for experimentation
model = fasttext.train_unsupervised('twitter.txt', model='skipgram', dim=100)

# Apply the word embedding model to the sentences
data['vec'] = data['processed_text'].apply(lambda x: model.get_sentence_vector(x))
