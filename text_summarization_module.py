#called after web scraping module to summarize

from gensim.summarization.summarizer import summarize

def get_summarized_article(text):
    tr_sum = summarize(text,word_count=280)
    return tr_sum
