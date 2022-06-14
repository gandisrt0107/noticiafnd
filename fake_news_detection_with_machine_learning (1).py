# -*- coding: utf-8 -*-
"""Salinan Fake News Detection with Machine Learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1snUKyT-iJHTCkDBPMNwv-ixRGtbibddK

# **Kelompok 4**

---

1. M. Yusuf
2. Gandis Ratna Cendani Karmana
3. Ganjar Arih Nurul Inas
4. Raden Roro Fara Diba
5. Rhena Yuni Junita
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import re
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop = stopwords.words('indonesian')
from nltk import tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from wordcloud import WordCloud, STOPWORDS

"""## *Load Dataset*"""

fake = pd.read_csv("/content/Fake - Fake.csv")
true = pd.read_csv("/content/True - True.csv")

fake.shape, true.shape

"""## *Preprocessing*"""

# Membuat tanda untuk melacak fake dan real news
fake['target'] = 0
true['target'] = 1

# Menggabungkan data frame
data = pd.concat([fake, true], ignore_index=True, sort=False)
data.head()

# Mengacak data untuk mencegah bias
data = shuffle(data)
data = data.reset_index(drop=True)
data.head()

# Menghapus judul, subjek dan tanggal karena tidak dibutuhkan
data.drop(["title", "subject", "date"],axis=1,inplace=True)
data.head()

# Mengubah ke huruf kecil
data['text'] = data['text'].apply(lambda x: x.lower())
data.head()

# Menghapus tanda baca
def punctuation_removal(text):
    all_list = [char for char in text if char not in string.punctuation]
    clean_str = ''.join(all_list)
    return clean_str

data['text'] = data['text'].apply(punctuation_removal)
data.head()

# Menghapus Stopwords
data['text'] = data['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
data.head()

"""## *Visualisasi*"""

# Menampilkan fake dan real dari artikel

print(data.groupby(['target'])['text'].count())
fig, ax = plt.subplots(1,2, figsize=(10, 5))
g = sns.countplot(data.target,ax=ax[0],palette="gist_gray");
g.set_title("Jumlah Fake dan Real Data", fontsize=15)
g.set_ylabel("Jumlah")
g.set_xlabel("Target")
plt.title('Persentase Target', fontsize=20)
data.groupby(['target'])['text'].count().plot(kind='pie', labels=['Fake', 'True', 'Unverified'], wedgeprops=dict(width=.2), autopct='%1.0f%%', startangle= -20,  textprops={'fontsize': 15})
fig.show()

# Fungsi kata yang paling sering muncul

token_space = tokenize.WhitespaceTokenizer()

def counter(text, column_text, quantity):
    all_words = ' '.join([text for text in text[column_text]])
    token_phrase = token_space.tokenize(all_words)
    frequency = nltk.FreqDist(token_phrase)
    df_frequency = pd.DataFrame({"Kata": list(frequency.keys()),
                                   "Frequency": list(frequency.values())})
    df_frequency = df_frequency.nlargest(columns = "Frequency", n = quantity)
    plt.figure(figsize=(12,8))
    ax = sns.barplot(data = df_frequency, x = "Kata", y = "Frequency", color = 'blue')
    ax.set(ylabel = "Jumlah")
    plt.xticks(rotation='vertical')
    plt.show()

# Kata-kata yang paling sering muncul dalam Fake News
counter(data[data["target"] == 0], "text", 20)

# Kata-kata yang paling sering muncul dalam Real News
counter(data[data["target"] == 1], "text", 20)

# Membuat World Cloud untuk Fake News

plt.figure(figsize = (15,15))
wc = WordCloud(max_words = 500 , width = 1000 , height = 500 , stopwords = STOPWORDS).generate(" ".join(data[data.target == 0].text))
plt.imshow(wc , interpolation = 'bilinear')
plt.axis("off")
plt.show()

# Membuat World Cloud untuk Real News

plt.figure(figsize = (15,15))
wc = WordCloud(max_words = 500 , width = 1000 , height = 500 , stopwords = STOPWORDS).generate(" ".join(data[data.target == 1].text))
plt.imshow(wc , interpolation = 'bilinear')
plt.axis("off")
plt.show()

"""## *N-Gram Analisis*"""

texts = ' '.join(data['text'])

string = texts.split(" ")

def draw_n_gram(string,i):
    n_gram = (pd.Series(nltk.ngrams(string, i)).value_counts())[:15]
    n_gram_df=pd.DataFrame(n_gram)
    n_gram_df = n_gram_df.reset_index()
    n_gram_df = n_gram_df.rename(columns={"index": "Kata", 0: "Jumlah"})
    print(n_gram_df.head())
    plt.figure(figsize = (16,9))
    return sns.barplot(x='Jumlah',y='Kata', data=n_gram_df)

"""### Unigram Analisis"""

draw_n_gram(string,1)
plt.show()

"""### Bigram Analisis"""

draw_n_gram(string,2)
plt.show()

"""### Trigram Analisis"""

draw_n_gram(string,3)
plt.show()

"""## *Pembagian Dataset*

### Membuat fungsi text
"""

def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) 
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)    
    return text

data["text"] = data["text"].apply(wordopt)

"""### Split Data"""

X_train,X_test,y_train,y_test = train_test_split(data['text'], data['target'], test_size=0.2, random_state=0)

print('Data Train : {shape}'.format(shape=X_train.shape))
print('Data Test : {shape}'.format(shape=X_test.shape))
print('Data Train (target) : {shape}'.format(shape=y_train.shape))
print('Data Test (target) : {shape}'.format(shape=y_test.shape))

"""## *Modeling dan Evaluasi*

### **Model dan Evaluasi Machine Learning**
"""

vectorization = TfidfVectorizer()
Xv_train = vectorization.fit_transform(X_train)
Xv_test = vectorization.transform(X_test)

"""#### Logistic Regression"""

from sklearn.linear_model import LogisticRegression

LR = LogisticRegression()
LR.fit(Xv_train,y_train)
pred_lr=LR.predict(Xv_test)
LR.score(Xv_test, y_test)

print(classification_report(y_test, pred_lr))

cm_LR_text = confusion_matrix(pred_lr,y_test)
sns.heatmap(cm_LR_text, annot=True, fmt='d',cmap='magma')
plt.title('Logistic Regression Confusion Matrix');

"""#### Decision Tree Classification"""

from sklearn.tree import DecisionTreeClassifier

DT = DecisionTreeClassifier()
DT.fit(Xv_train, y_train)
pred_dt = DT.predict(Xv_test)
DT.score(Xv_test, y_test)

print(classification_report(y_test, pred_dt))

cm_DT_text = confusion_matrix(pred_dt,y_test)
sns.heatmap(cm_DT_text, annot=True, fmt='d',cmap='magma')
plt.title('Decision Tree Confusion Matrix');

"""#### Random Forest Classifier"""

from sklearn.ensemble import RandomForestClassifier

RFC = RandomForestClassifier(random_state=0)
RFC.fit(Xv_train, y_train)
pred_rfc = RFC.predict(Xv_test)
RFC.score(Xv_test, y_test)

print(classification_report(y_test, pred_rfc))

cm_RFC_text = confusion_matrix(pred_rfc,y_test)
sns.heatmap(cm_RFC_text, annot=True, fmt='d',cmap='magma')
plt.title('Random Forest Confusion Matrix');

"""#### Gradient Boosting Classifier"""

from sklearn.ensemble import GradientBoostingClassifier

GBC = GradientBoostingClassifier(random_state=0)
GBC.fit(Xv_train, y_train)
pred_gbc = GBC.predict(Xv_test)
GBC.score(Xv_test, y_test)

print(classification_report(y_test, pred_gbc))

cm_GBC_text = confusion_matrix(pred_gbc,y_test)
sns.heatmap(cm_GBC_text, annot=True, fmt='d',cmap='magma')
plt.title('Gradient Boosting Confusion Matrix');

"""#### *Testing Model*"""

def output_lable(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Bukan Fake News"
    
def manual_testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt) 
    new_X_test = new_def_test["text"]
    new_Xv_test = vectorization.transform(new_X_test)
    pred_LR = LR.predict(new_Xv_test)
    pred_DT = DT.predict(new_Xv_test)
    pred_GBC = GBC.predict(new_Xv_test)
    pred_RFC = RFC.predict(new_Xv_test)

    return print("\n\nLR Prediction: {} \nDT Prediction: {} \nGBC Prediction: {} \nRFC Prediction: {}".format(output_lable(pred_LR[0]),                                                                                                       output_lable(pred_DT[0]), 
                                                                                                              output_lable(pred_GBC[0]), 
                                                                                                              output_lable(pred_RFC[0])))

news = str(input())
manual_testing(news)

"""## *Save Klasifikasi*"""

import pickle

f = open('Model LogisticRegression', 'wb')
pickle.dump(classification_report(y_test, pred_lr), f)
f.close()

f = open('Model LogisticRegression', 'rb')
MLR = pickle.load(f)
f.close()
print(MLR)