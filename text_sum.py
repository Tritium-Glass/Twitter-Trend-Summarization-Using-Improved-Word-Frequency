from nltk.tokenize import RegexpTokenizer
token = RegexpTokenizer(r'\w+')
from nltk.corpus import stopwords

def main():
	with open('harmonyos.txt', 'r') as myfile:
		text = myfile.read()

		make_summary(text)

def make_summary(text):
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
	##print(text)
	##print(sen)
	##print(small)
	##print(punc_free)
	##print(words)
	##print(wgt)
	##print(order)
	##print(sorted_sen)
	first = max(sorted_sen, key=lambda x:sorted_sen[x])
	print(first)
	del sorted_sen[first]
	second = max(sorted_sen, key=lambda x:sorted_sen[x])
	print(second)

if __name__ == '__main__':
	main()