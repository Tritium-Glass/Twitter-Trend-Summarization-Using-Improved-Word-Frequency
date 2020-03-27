from nltk.tokenize import RegexpTokenizer
token = RegexpTokenizer(r'\w+')
from nltk.corpus import stopwords

# with open('microsoft.txt','r+',encoding="utf-8") as file:
#     text = file.read()
# text = '''
# Huawei Technologies founder and CEO Ren Zhengfei said on Thursday the Chinese company is willing to license its Ren told reporters he was not afraid of creating a rival by making Huawei's technology available to competitors, and the offer could also include chip design know-how.Huawei, the world's largest telecoms gear maker, has been on a US trade blacklist since May over concerns that its equipment could be used by Beijing to spy. Huawei has repeatedly denied such allegations.The sanctions cut off Huawei's access to essential US technologies. The latest version of its Mate 30 flagship phone, unveiled last week in Europe, will not come with Google Mobile Services.Ren's remarks come after he said this month that he is open to selling the firm's 5G technology - including patents, code, blueprints and production know-how - to Western firms for a one-off fee.The offer to license out 5G technology marks the latest attempt by Huawei, also the world's No.2 smartphone vendor, to minimise the impact of the US trade ban. It expects a drop of some $10bn in revenue from its phone business this year.
# '''

def word_freq_improved_summarize(text):
    sen = text.split('.')
    #normalise
    small = [s.lower() for s in sen]
    #remove punctuation
    punc_free = []
    for p in small: punc_free.extend(token.tokenize(p))
    #remove stopwords
    stop_words = set(stopwords.words('english'))
    words = []
    for x in punc_free:
        if x not in stop_words: words.append(x)
    #weighted frequency
    wgt = {}
    for x in words: wgt[x] = words.count(x)
    max_freq = max(wgt.values())
    for x in wgt.keys(): wgt[x] = wgt[x]/max_freq
    #replace with weighted_frequency
    order = {}
    avg = len(sen)/2
    for i in range(len(sen)):
        sum = 0
        wrd = sen[i].split()
        for w in wrd:
            current = (str(token.tokenize(w))[2:-2]).lower()
            if current in wgt:
                sum += wgt[current]
        order[sen[i]] = sum*(1+0.1*abs(avg-i)/avg)
    sorted_sen = dict(sorted(order.items(), key = lambda x:x[1], reverse=True))
    # print('\n1.Text\n',text)
    # print('\n2.List of Sentences\n',sen)
    # print('\n3.List of sentences in small case\n',small)
    # print('\n4.Removing punctuation\n',punc_free)
    # print('\n5.Removing stop words\n',words)
    # print('\n6.Word frequency\n',wgt)
    # print('\n7.Sentences with sum of frequency of their words\n',order)
    # print('\n8.Sorted sentences\n',sorted_sen)
    # print('\n9.Final Summary:')
    final_summary = ""
    while True and len(sorted_sen)>0:
        summ = max(sorted_sen, key=lambda x:sorted_sen[x])
        if (len(final_summary)+len(summ))<240:
            final_summary += summ
            del sorted_sen[summ]
        else:
            if len(final_summary)<1:
                del sorted_sen[summ]
                continue
            else:
                break

    return final_summary

if __name__ == "__main__":
    with open('./passages/harmonyos.txt','r+',encoding="utf-8") as file:
        text = file.read()
        word_freq_improved_summarize(text)
