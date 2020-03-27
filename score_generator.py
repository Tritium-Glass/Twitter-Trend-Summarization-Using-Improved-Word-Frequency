import csv
from tf_idf import tf_idf_summarise
from word_freq import word_freq_summarize
from word_freq_improved import word_freq_improved_summarize
from gensim.summarization.summarizer import summarize
from lsa_textsum import lsa_summarise
import summary_evaluation as sumeval
from timeit import default_timer as timer

def score_generator(human_summary, text):

    ref_sum = human_summary

    try:
        #word frequency
        wf_start = timer()
        wf_sum = word_freq_summarize(text)
        wf_end = timer()
        wf_time = wf_end - wf_start
        matching_bigrams, wf_precision, wf_recall, wf_f_measure = sumeval.rouge(ref_sum, wf_sum)
        print("Word Frequency: Time:",wf_time,"precision: ",wf_precision,"recall:"\
        ,wf_recall,"f_measure:",wf_f_measure)

        #tf-idf
        tf_start = timer()
        tf_sum = tf_idf_summarise(text)
        tf_end = timer()
        tf_time = tf_end - tf_start
        matching_bigrams, tf_precision, tf_recall, tf_f_measure = sumeval.rouge(ref_sum, tf_sum)
        print("TF-IDF: Time:",tf_time,"precision: ",tf_precision,"recall:"\
        ,tf_recall,"f_measure:",tf_f_measure)

        #textrank
        tr_start = timer()
        tr_sum = summarize(text,word_count=280)
        tr_end = timer()
        tr_time = tr_end - tr_start
        matching_bigrams, tr_precision, tr_recall, tr_f_measure = sumeval.rouge(ref_sum, tr_sum)
        print("TextRank: Time:",tr_time,"precision: ",tr_precision,"recall:"\
        ,tr_recall,"f_measure:",tr_f_measure)

        #lsa
        lsa_start = timer()
        lsa_sum = lsa_summarise(text)
        lsa_end = timer()
        lsa_time = lsa_end - lsa_start
        matching_bigrams, lsa_precision, lsa_recall, lsa_f_measure = sumeval.rouge(ref_sum, lsa_sum)
        print("LSA: Time:",lsa_time,"precision: ",lsa_precision,"recall:"\
        ,lsa_recall,"f_measure:",lsa_f_measure)

        #improved wf
        wfi_start = timer()
        wfi_sum = word_freq_improved_summarize(text)
        wfi_end = timer()
        wfi_time = wfi_end - wfi_start
        matching_bigrams, wfi_precision, wfi_recall, wfi_f_measure = sumeval.rouge(ref_sum, wfi_sum)
        print("Word Frequency Improved: Time:",wfi_time,"precision: ",wfi_precision,"recall:"\
        ,wfi_recall,"f_measure:",wfi_f_measure)
    except Exception as e:
        print(e)
        return

    with open('results_blackbook.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([str(wf_time),str(tf_time),str(tr_time),str(wfi_time),str(lsa_time),str(wf_f_measure),str(tf_f_measure),str(tr_f_measure),str(wfi_f_measure),str(lsa_f_measure)])

def main():
    with open('doc_sum_2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            print(i)
            i+=1
            score_generator(row[1].lower(), row[0].lower())

if __name__ == '__main__':
    main()
