import csv
import numpy as np
import pandas as pd
pd.set_option("display.max_colwidth", 200)

def compare_trends(topics_1,topics_2):

	topics_1 = set(topics_1)
	topics_2 = set(topics_2)

	union = topics_1.intersection(topics_2)

	if len(union)>5:
		return 1
	else:
		return 0

def get_topics(documents):

	# with open('doc_sum.csv') as csv_file:
	#     csv_reader = csv.reader(csv_file, delimiter=',')
	#     i = 0
	#     for row in csv_reader[]:
	#         i+=1
	#         if i<0:
	#             continue
	#         if i>=4:
	#             break
	#         print(i)
	#         documents.append(row[0])

	news_df = pd.DataFrame({'document':documents})

	# removing everything except alphabets`
	news_df['clean_doc'] = news_df['document'].str.replace("[^a-zA-Z#]", " ")

	# removing short words
	news_df['clean_doc'] = news_df['clean_doc'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))

	# make all text lowercase
	news_df['clean_doc'] = news_df['clean_doc'].apply(lambda x: x.lower())

	#Remove stopwords

	from nltk.corpus import stopwords
	stop_words = stopwords.words('english')

	# tokenization
	tokenized_doc = news_df['clean_doc'].apply(lambda x: x.split())

	# remove stop-words
	tokenized_doc = tokenized_doc.apply(lambda x: [item for item in x if item not in stop_words])

	# de-tokenization
	detokenized_doc = []
	for i in range(len(news_df)):
		t = ' '.join(tokenized_doc[i])
		detokenized_doc.append(t)

	news_df['clean_doc'] = detokenized_doc

	#create tf-idf matrix using sklearn

	from sklearn.feature_extraction.text import TfidfVectorizer

	vectorizer = TfidfVectorizer(stop_words='english',
	max_features= 100, # keep top 1000 terms
	max_df = 0.5,
	smooth_idf=True)

	'''max_df = float in range [0.0, 1.0] or int (default=1.0)
	When building the vocabulary ignore terms that have a document
	frequency strictly higher than the given threshold (corpus-specific stop words).
	If float, the parameter represents a proportion of documents, integer absolute counts.
	This parameter is ignored if vocabulary is not None.
	'''

	X = vectorizer.fit_transform(news_df['clean_doc'])

	X.shape # check shape of the document-term matrix

	x = pd.DataFrame(X)
	x.tail()

	# get the first vector out (for the first document)
	first_vector_tfidfvectorizer=X[0]

	# place tf-idf values in a pandas data frame
	df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=vectorizer.get_feature_names(), columns=["tfidf"])
	df.sort_values(by=["tfidf"],ascending=False)


	from sklearn.decomposition import TruncatedSVD

	# SVD represent documents and terms in vectors
	svd_model = TruncatedSVD(n_components=1, algorithm='randomized', n_iter=100, random_state=122)

	svd_model.fit(X)

	len(svd_model.components_)

	terms = vectorizer.get_feature_names()

	result = []

	for i, comp in enumerate(svd_model.components_):
		terms_comp = zip(terms, comp)
		sorted_terms = sorted(terms_comp, key= lambda x:x[1], reverse=True)[:10]
		# print("\nTopic "+str(i)+": ")
		for t in sorted_terms:
			result.append(t[0])
			# print(t[0],end="")
			# print(", ", end="")

	return result

def main():
	documents = []
	with open('doc_sum.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		i = 0
		for row in csv_reader:
			i+=1
			if i<7:
				continue
			if i>=11:
				break
			# print(i)
			documents.append(row[0])
	print(get_topics(documents))

if __name__ == '__main__':
	main()
