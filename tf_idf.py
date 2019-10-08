import math

from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
import nltk
import summary_evaluation as se
nltk.download('punkt')

# with open('microsoft.txt','r+',encoding="utf-8") as file:
#     text = file.read()
# text = '''
# Microsoft held talks in the past few weeks to acquire software developer platform GitHub, Business Insider reports. One person familiar with the discussions between the companies told CNBC that they had been considering a joint marketing partnership valued around $35 million, and that those discussions had progressed to a possible investment or outright acquisition. It is unclear whether talks are still ongoing, but this person said that GitHub's price for a full acquisition was more than Microsoft currently wanted to pay. GitHub was last valued at $2 billion in its last funding round 2015, but the price tag for an acquisition could be $5 billion or more, based on a price that was floated last year. GitHub's tools have become essential to software developers, who use it to store code, keep track of updates and discuss issues. The privately held company has more than 23 million individual users in more than 1.5 million organizations. It was on track to book more than $200 million in subscription revenue, including more than $110 million from companies using its enterprise product, GitHub told CNBC last fall.Microsoft has reportedly flirted with buying GitHub in the past, including in 2016, although GitHub denied those reports. A partnership would give Microsoft another connection point to the developers it needs to court to build applications on its various platforms, including the Azure cloud. Microsoft could also use data from GitHub to improve its artificial intelligence producs. The talks come amid GitHub's struggle to replace CEO and founder Chris Wanstrath, who stepped down 10 months ago. Business Insider reported that Microsoft exec Nat Friedman -- who previously ran Xamarin, a developer tools start-up that Microsoft acquired in 2016 -- may take that CEO role. Google's senior VP of ads and commerce, Sridhar Ramaswamy, has also been in discussions for the job, says the report. Microsoft declined to comment on the report. GitHub did not immediately return a request for comment.
# '''
#remove stop words, stem the words and then create frequency matrix of it
def _create_frequency_matrix(sentences):
    frequency_matrix = {}
    stopWords = set(stopwords.words("english"))
    ps = PorterStemmer()

    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            word = ps.stem(word)
            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:10]] = freq_table
    return frequency_matrix

'''
find total number of words in each sentence considering
it as a document and calculates term frequency for each
'''
def _create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix

#find out how many sentences(documents) contain a word
def _create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table

'''
IDF(t) = log_e(Total number of documents / Number of documents with term t in it)
'''
def _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix

#TF-IDF mixes 2 algorithms. Hence we multiply TF and IDF for each word
def _create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix

def _score_sentences(tf_idf_matrix):
    """
    score a sentence by its word's TF
    Basic algorithm: adding the TF frequency of every non-stop word
    in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score

        sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence

    return sentenceValue

#threshold value for selecting sentences is the average sentence score
def _find_average_score(sentenceValue) -> int:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original summary_text
    average = (sumValues / len(sentenceValue))
    return average

#sentence selected if the sentence score is more than threshold
def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        # print(sentence)
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary

def tf_idf_summarise(text):
    # 1 Separate sentences
    sentences = sent_tokenize(text) #NLTK function
    total_documents = len(sentences)
    # print('1. Tokenised sentences:\n',sentences)

    # 2 Create the Frequency matrix of the words in each sentence.
    freq_matrix = _create_frequency_matrix(sentences)
    # print('\n2. Frequency Matrix of stemmed words:\n',freq_matrix)

    '''
    Term frequency (TF) is how often a word appears in a document, divided by how many words are there in a document.
    '''
    # 3 Calculate TermFrequency and generate a matrix
    tf_matrix = _create_tf_matrix(freq_matrix)
    # print('\n3. Term Frequency Matrix:\n',tf_matrix)

    # 4 creating table for documents per words
    count_doc_per_words = _create_documents_per_words(freq_matrix)
    # print('\n5. How many documents contain the word:\n',count_doc_per_words)

    '''
    Inverse document frequency (IDF) is how unique or rare a word is.
    '''
    # 5 Calculate IDF and generate a matrix
    idf_matrix = _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents)
    # print('\n5. How unique a word is(IDF):\n',idf_matrix)

    # 6 Calculate TF-IDF and generate a matrix
    tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)
    # print('\n6. The TF-IDF matrix(TF*IDF):\n',tf_idf_matrix)

    # 7 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(tf_idf_matrix)
    # print('\n7. Sentence scores:\n',sentence_scores)

    # 8 Find the threshold
    threshold = _find_average_score(sentence_scores)
    # print('\n8. Threshold value(average sentence score):\n',threshold)

    # 9 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1 * threshold)
    # print('\n**SUMMARY**:\n',summary)

    return summary
