
from collections import Counter
import math

from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk
from string import punctuation

stop_words = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')
#separate sentences and consider each as separate document

def main(articles):

    tf = []

    article_words = []
    for article in articles:
        #print(article)
        tokenized_article = tokenizer.tokenize(article)
        filtered_text = [w for w in tokenized_article if not w in stop_words]
        article_words.append(filtered_text)
        #print(filtered_text)
        tf.append(dict(Counter(filtered_text)))

    idf = {}

    for item in tf:
        for key in item.keys():
            count = 0
            for article in article_words:
                if key in article:
                    count+=1
            idf[key]=math.log(len(article_words)/count)

    important_words = []

    for key,value in idf.items():
        if value == 0:
            important_words.append(key)
    print(important_words)

if __name__ == '__main__':
    text = ""
    text2 = ""
    with open('harmonyos.txt','r+',encoding="utf-8") as file:
        text = file.read()

    with open('harmonyos2.txt','r+',encoding="utf-8") as file:
        text2 = file.read()
    main([text,text2])
