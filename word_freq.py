from nltk.tokenize import RegexpTokenizer
token = RegexpTokenizer(r'\w+')
from nltk.corpus import stopwords

with open('johannes.txt','r+',encoding="utf-8") as file:
    text = file.read()
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
for s in sen:
    sum = 0
    wrd = s.split()
    for w in wrd:
        current = (str(token.tokenize(w))[2:-2]).lower()
        if current in wgt:
            sum += wgt[current]
    order[s] = sum
sorted_sen = dict(sorted(order.items(), key = lambda x:x[1], reverse=True))
print('\n1.Text\n',text)
print('\n2.List of Sentences\n',sen)
print('\n3.List of sentences in small case\n',small)
print('\n4.Removing punctuation\n',punc_free)
print('\n5.Removing stop words\n',words)
print('\n6.Word frequency\n',wgt)
print('\n7.Sentences with sum of frequency of their words\n',order)
print('\n8.Sorted sentences\n',sorted_sen)
print('\n9.Final Summary:')
final_summary = ""
for i in range(4):
    summ = max(sorted_sen, key=lambda x:sorted_sen[x])
    final_summary += summ
    print(summ)
    del sorted_sen[summ]
