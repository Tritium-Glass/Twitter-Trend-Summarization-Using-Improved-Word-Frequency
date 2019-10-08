import web_scraping_prototype as WSP
import auto_summarization as autosum
# import tf_idf
import word_freq
import summary_evaluation as sumeval

def main():
    articles = WSP.aljazeera_search('huawei')
    print(articles)
    for article in articles:
        ref_sum = autosum.get_summary(article)
        sys_sum = word_freq.word_freq_summarize(article)
        matching_bigrams, precision, recall, f_measure = sumeval.rouge(ref_sum, sys_sum)
        # print('Ref Sum:',ref_sum,'\nSys Sum:',sys_sum)
        print('\nB:',matching_bigrams,'\tP:',precision,'\tR',recall,'\tF',f_measure)

if __name__ == "__main__":
    main()
