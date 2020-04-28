#called after web scraping module to summarize

from word_freq_imporved import word_freq_improved_summarize

def get_summarized_article(text):
    tr_sum = word_freq_improved_summarize(text)
    return tr_sum
