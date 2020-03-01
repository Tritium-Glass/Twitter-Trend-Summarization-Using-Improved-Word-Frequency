#called after web scraping module to summarize

from word_freq import word_freq_summarize
from timeit import default_timer as timer

def get_summarized_article(text):
    summarization_start = timer()
    summary = word_freq_summarize(text)
    summarization_end = timer()
    summarization_time = summarization_end - summarization_start
    return summary, summarization_time
