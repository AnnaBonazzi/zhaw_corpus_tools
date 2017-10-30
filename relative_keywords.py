#coding=utf8
'''
Anna Bonazzi, 06/10/2017

Script to extract keywords from a corpus by comparing it to another larger corpus and picking the words with a larger relative frequency

Keywords: words whose relative frequency is bigger in the main corpus. Keywords are sorted by the difference in rel freq between corpus 1 and corpus 2: words with a rel freq that is hugely superior in corpus 1 come first.

'''
# VARIABLES FOR USER TO CHANGE

corpus1 = '/path/to/main_corpus.vrt' # Interesting corpus
corpus2 = '/path/to/comparison_corpus.vrt' # Big comparison corpus
output_folder = '/path/to/keywords_folder/'
min_freq = 2 # Minimum frequency of keyword candidates
lang = 'fr'
unit = 'lemma' # Options: 'wordform', 'lemma', 'pos'
#--------------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import re
from nltk.corpus import stopwords
#--------------------------
langs = {'fr' : 'french', 'de' : 'german', 'it' : 'italian', 'en' : 'english'}
stop = set(stopwords.words(langs[lang]) + ['avoir', 'e', 'aucun'])
# Counts word frequencies
def corpus_stats(corpus):
	print ('Searching '+corpus+'... patience.')
	word_tot = 0; word_dic = {}
	text_counter = 0
	chunk = []
	with open (corpus, 'r') as f:	
		for line in f:
			if '</text>' not in line: # Works text by text
				if '<' not in line:
					units = {'wordform' : 0, 'lemma':2, 'pos':1}
					word = line.split("\t")[units[unit]].decode('utf-8')
					# Lemmas [2], wordforms [0], pos [1]
					chunk.append(word)						
				elif '<text' in line:
					chunk.append(line.decode('utf-8'))
			else: # Meets text end, works on temporary text chunk
				text_counter += 1
				chunk.append(line.decode('utf-8'))
			  	# Searches for chosen lang/class combination
				regex = re.search('language="'+lang+'".*?subclass=".*?".*?', ''.join(chunk))
				if regex:
					for word in chunk:
						if '<text' not in word.split(' '):
							# Counts word frequency
							word_tot += 1
							if word in word_dic:
								word_dic[word] += 1
							else:
								word_dic[word] = 1
				chunk = []
				if '00000' in str(text_counter):
					print (str(text_counter))
		return (word_tot, word_dic)

word_tot1, word_dic1 = corpus_stats(corpus1)
word_tot2, word_dic2 = corpus_stats(corpus2)

def rel_freq(word_tot, word_dic):
	rel_freq = {}
	for word in word_dic:
		rel = float('{:.5f}'.format(word_dic[word] * 100 / word_tot))
		rel_freq[word] = rel
	return rel_freq

rel_freq1 = rel_freq(word_tot1, word_dic1)
rel_freq2 = rel_freq(word_tot2, word_dic2)

keywords = {}

for word in rel_freq1:
	if rel_freq1[word] >= min_freq:
		if word not in rel_freq2:
			rel_freq2[word] = 1
		# Compares relative frequencies of word in the 2 corpora
		if rel_freq1[word] > rel_freq2[word]:
			keywords[word] = rel_freq1[word] - rel_freq2[word]

sorted_tuples = sorted(keywords.items(), key=lambda pair: pair[1], reverse=True)
with open (output_folder+lang+'_geothermie_relative.txt', 'a') as out:
	for tup in sorted_tuples:
		print (str(tup[0].encode('utf-8')) + "\t" + str(tup[1]).encode('utf-8') + "\n")
		out.write(str(tup[0].encode('utf-8')) + "\t" + str(tup[1]).encode('utf-8') + "\n")

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
