doc = [
    "An intern at OpenGenus",
    "Developer at OpenGenus",
    "A ML intern",
    "A ML developer"
]

from sklearn.feature_extraction.text import CountVectorizer

# Converting each document into an vector
vectorizer = CountVectorizer()
bag_of_words = vectorizer.fit_transform(doc)

#look at the vectors
print(bag_of_words.todense())

#Singular value decomposition
from sklearn.decomposition import TruncatedSVD
#This process encodes our original data into topic encoded data
svd = TruncatedSVD(n_components = 2)
lsa = svd.fit_transform(bag_of_words)

#Using pandas to look at the output of lsa
import pandas as pd

topic_encoded_df = pd.DataFrame(lsa, columns=["topic1", "topic2"])
topic_encoded_df["doc"]= doc
print(topic_encoded_df[["doc","topic1","topic2"]])

#A look at dictionary
dictionary = vectorizer.get_feature_names()
print(dictionary)

encoding_matrix=pd.DataFrame(svd.components_,index = ["topic1","topic2"],columns=dictionary).T
print(encoding_matrix)
#numerical values can be thought of as an expression of that word in respective topic

#Considering the words affecting variance in data
import numpy as np
encoding_matrix['abs_topic1']=np.abs(encoding_matrix["topic1"])
encoding_matrix['abs_topic2']=np.abs(encoding_matrix["topic2"])
encoding_matrix.sort_values('abs_topic1',ascending=False)

#We need the matrix with absolute values only to determine the strength of each part of sentence effectively
final_matrix=encoding_matrix.sort_values('abs_topic1',ascending=False)
print(final_matrix[["abs_topic1","abs_topic2"]])

#Extracting out final sentence from topic 1
sentence1= final_matrix[final_matrix["abs_topic1"]>=0.4]
print(sentence1[['abs_topic1']])
#Extracting out final sentence from topic 2
sentence2=final_matrix[final_matrix["abs_topic2"]>=0.4]
print(sentence2[['abs_topic2']])
