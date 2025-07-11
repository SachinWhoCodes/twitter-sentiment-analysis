# -*- coding: utf-8 -*-
"""Twitter-sentimental-analysis-using-ml.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eOPWZVY7pjiQQWVGURO55OJTA67JHyM3
"""

#installing kaggle (for dataset)
! pip install kaggle

"""Uploading Kaggle Json File"""

!mkdir -p ~/.kaggle
!cp /content/kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

"""Importing Semtimental Dataset"""

#API to fetch dataset
import kagglehub

# Download latest version
path = kagglehub.dataset_download("kazanova/sentiment140")

print("Path to dataset files:", path)

#required dependencies
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

#Printing stopwords in english
print(stopwords.words('english'))

"""Data Processing"""

#loading the data from csv to pandas dataframe
twitter_data = pd.read_csv('/kaggle/input/sentiment140/training.1600000.processed.noemoticon.csv', encoding='ISO-8859-1')

#checking the number of rows and cols
twitter_data.shape

#print head rows
twitter_data.head()

#naming the cols

column_names = ['target', 'id', 'date', 'flag', 'user', 'text']
twitter_data = pd.read_csv('/kaggle/input/sentiment140/training.1600000.processed.noemoticon.csv', names=column_names, encoding='ISO-8859-1')
# twitter_data.shape
twitter_data.head()

#counting the missing values in the dataset
twitter_data.isnull().sum()

#checking the distribution of target col
twitter_data['target'].value_counts()

"""Convert the target "4" to "1"
"""

twitter_data.replace({'target':{4:1}}, inplace=True)

#checking again the distribution of target col
twitter_data['target'].value_counts()

"""0 --> Negative Tweet
1 --> Positive Tweet

**Stemming**
"""

port_stem = PorterStemmer()

def stemming(content):

  stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
  stemmed_content = stemmed_content.lower()
  stemmed_content = stemmed_content.split()
  stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
  stemmed_content = ' '.join(stemmed_content)

  return stemmed_content

twitter_data['stemmed_content'] = twitter_data['text'].apply(stemming)

twitter_data.head()

#separating the target and stemmed content

Y = twitter_data['target'].values
X = twitter_data['stemmed_content'].values

print(X)

print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

print(X.shape, X_train.shape, X_test.shape)

#converting the text data to textual data
vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print(X_train)

"""Training the Model --> Logistic Regression"""

model = LogisticRegression(max_iter=1000)

model.fit(X_train, Y_train)

"""Model Evaluation --> Accuracy Score"""

X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(Y_train, X_train_prediction)

print(training_data_accuracy)

#Now testing on test data
X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(Y_test, X_test_prediction)

print(test_data_accuracy)

"""Accuracy Score --> 0.77668125

**Saving the trained model**
"""

import pickle

filename = 'twitter_sentimental_analysis_trained_model.sav'
pickle.dump(model, open(filename, 'wb'))

