import web_scraping_prototype as WSP
import auto_summarization as autosum
from tf_idf import tf_idf_summarise
from word_freq import word_freq_summarize
from gensim.summarization.summarizer import summarize
import summary_evaluation as sumeval
import csv

article_count = 1

def main():
    with open("keywords.txt") as file:
        keywords = file.read().split('\n')
    print(len(keywords))
    keywords = set(keywords)
    print(len(keywords))
    for keyword in keywords:
        articles = WSP.aljazeera_search(keyword)
        print(len(articles))
        for i in range(min(len(articles,article_count))):
            try:
                ref_sum = autosum.get_summary(articles[i])
                sys_sum = word_freq_summarize(articles[i])
            except:
                continue
            # sys_sum = word_freq_summarize(article)
            # sys_sum = tf_idf_summarise(article)
            matching_bigrams, precision, recall, f_measure = sumeval.rouge(ref_sum, sys_sum)
            #print('Ref Sum:',ref_sum,'\nSys Sum:',sys_sum)
            with open('scores.csv', mode='a', encoding='utf-8', newline='') as scores_file:
                scores_writer = csv.writer(scores_file, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_ALL)
                scores_writer.writerow(['WF', keyword, article, ref_sum, sys_sum, precision, recall, f_measure])
            # print('\nB:',matching_bigrams,'\tP:',precision,'\tR',recall,'\tF',f_measure)

if __name__ == "__main__":
    main()
