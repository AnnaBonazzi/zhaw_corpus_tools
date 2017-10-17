#coding=utf8
'''
Anna Bonazzi, 06/09/2017

Script to find collocates of specific words from a corpus.

What the script does:
	1) Picks corpus texts with chosen language, puts them together
	2) Finds collocations (basis-collocate pairs) in window of given size
	3) Selects collocations containing the desired searchword / searchword variants (through regex)
	4) Sorts the searchword's collocates by pmi or log-likelihood value

! Requires all the encode/decode pieces in python2.7. Comment it out for python 3.
'''
#--------------------------
# VARIABLES FOR USER TO CHANGE:

lang = 'fr'
searchwords = ['géothermie', 'Fukushima', 'énergie', 'renouvelable', 'nucléaire']

regexes = {'géothermie': '(?i)géotherm.*?', 'Fukushima': '(?i)Fo?uko?ushima.?', 'énergie': '(?i)énergies?', 'renouvelable' : '(?i)renouvelables?', 'nucléaire' : '(?i)(nucléair.*|atomiqu.*)'} # If you don't want to search by regex, comment this line out

input_file = '/path/to/corpus_file.vrt'
output_folder = '/path/to/collocates_folder/'

min_freq = 3 # Minimum word frequency to be considered as a collocation candidate
window_size = 6 # Size of word window to search for collocates
unit = 'wordform' # Options: 'lemma', 'wordform', 'pos'. Hint: search for "word" when using regex, and "lemma" when using plain searchwords

coll_measure = 'likelihood_ratio' # Options: 'likelihood_ratio', 'pmi'
#---------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re, sys
# If needed: first run "sudo pip install nltk"
import nltk
from nltk.corpus import stopwords
from nltk.collocations import *
# To recognize punctuation
import string
#---------------------

# Prepares to removes punctuation
punct = set(string.punctuation + '»' + '«')

# 1) Assembles text with chosen lang combination
for sw in searchwords:
	flag1 = 0 # Prepares to search by word or by regex
	try:
		reg = regexes[sw].decode('utf-8')
		flag1 = 1
	except:
		pass
	
	print ('!! Now looking for collocates of "' + sw +'"')
	sw = sw.decode('utf-8')
	acceptables = {} # Prepares to collect acceptable word versions through regex
	text_counter = 0 # To keep track
	chunk = [] # Prepares temporary text as list
	text = []
	sw_freq = 0
	flag = 0 # To skip collocation making with irrelevant texts
	# Goes through corpus
	with open (input_file, 'r') as f:
		for line in f:
			if '</text>' not in line: # Works text by text
				if '<' not in line:
					units = {'wordform' : 0, 'pos' : 1, 'lemma' : 2} 
					chunk.append(line.split('\t')[units[unit]].decode('utf-8'))
						
				elif '<text' in line:
					chunk.append(line.decode('utf-8'))
				elif '</s' in line:
					chunk.append(line.strip('\n').decode('utf-8'))
		
			else: # Meets current text end
				chunk.append(line.strip('\n').decode('utf-8'))
			  	# Searches for chosen lang combination
				regex = re.search('class="(.*?)".*?language="'+lang, ''.join(chunk))
				if regex:
					temp = []
					for word in chunk:
						if ('<text' and '</text') not in word and word.encode('utf-8') not in punct: # Excludes xml and punctuation							
							# Saves only text chunks where word is, shifting 1 by 1
							while len(temp) < window_size:
								temp.append(word)
							if len(temp) == window_size:
								# By regex
								if flag1 == 1:
									regex2 = re.findall(reg, ' '.join(temp))
									if regex2:
										text = text + temp
										temp.pop(0)
									else:
										temp.pop(0)
								# By word 
								elif flag1 == 0:
									if sw in temp:
										text = text + temp
										temp.pop(0)
									else:
										temp.pop(0)
							
							#text.append(word)
							# Counts word freq by word or by regex (as set above)
							if flag1 == 1:
								regex3 = re.search(reg, word)
								if regex3:
									sw_freq += 1
									acceptables[word] = 1
							elif flag1 == 0:
								if sw in word or sw.lower() in word:
									sw_freq += 1
											
					text_counter += 1
				if '00000' in str(text_counter):
					print ("\tText " + str(text_counter))
				chunk = [] # Resets empty chunk for next corpus text

	# text is now a list
	if sw_freq == 0:
		print ("\nSearchword " + sw + " not in corpus.\n")
		flag = 1
	else:
		print ("Searchword " + sw + " is there " + str(sw_freq) + " times")
#----------------------------------------	
	if flag == 0:
	# 2) Starts making collocations
		time1 = datetime.now() - startTime
		print ('Making collocations after ' + str(time1) + '\n')	
		
		# Prepares text (list or string) in nltk format
		corpus = nltk.Text(text) # From list
		#corpus = nltk.wordpunct_tokenize(text) # From string
		text = None

		# Makes 2-/3-grams with PMI or log-likelihood values and given window size
		bigram_measures = nltk.collocations.BigramAssocMeasures()
		bi_finder = BigramCollocationFinder.from_words(corpus, window_size = window_size)

		# Filters ngrams by frequency
		bi_finder.apply_freq_filter(min_freq)
		# Filters ngrams with sentence boundary
		my_filter = lambda *w: '</s>' in w
		bi_finder.apply_ngram_filter(my_filter)
		
		# Filters ngrams by searchword / regex
		if flag1 == 0:
			# Throws away ngrams where neither element is the searchword
			my_filter = lambda *w: sw not in w and sw.lower() not in w
			bi_finder.apply_ngram_filter(my_filter)
		else:
			accept = [x for x in acceptables] # Previously found regex-matching words
			# Throws away bigrams where neither element is the searchword
			my_filter = lambda w1, w2: w1 not in accept and w2 not in accept
			bi_finder.apply_ngram_filter(my_filter)
		
		# Makes collocations
		if coll_measure == 'likelihood_ratio':
			bi_list = bi_finder.score_ngrams(bigram_measures.likelihood_ratio)
		else:
			bi_list = bi_finder.score_ngrams(bigram_measures.pmi)
	#----------------------------------------	
	# 3) Sorts collocates by their log-lik or pmi value

		collocates = {}
		# Prepares to remove stopwords
		pairs = {'de' : 'german', 'fr' : 'french', 'en' : 'english', 'it' : 'italian'}
		stop = set(stopwords.words(pairs[lang]) + ['L', 'l', '’', 'être', 'card', 'avoir', '@card@', 'S', '’', '@ord@'])
		
		# Collects collocates. Collocation format: ((word1, word2), (log-l-value))
		for coll in bi_list:
			for word in coll[0]:
				# For plain searchword
				if flag1 == 0:
					if not word == sw and not word == sw.lower() and word not in stop:
						if word not in collocates:
							collocates[word] = coll[1]
						else:
							collocates[word] += coll[1]
				# For regex
				else:
					if (word and word.title() and word.lower()) not in accept and word not in stop:
						if word not in collocates:
							collocates[word] = coll[1]
						else:
							collocates[word] += coll[1]
		# Sorts and prints out
		sorted_tuples = sorted(collocates.items(), key=lambda pair: pair[1], reverse=True)
		with open (output_folder + lang + '_' + sw + '.txt', 'a') as out:
			for tup in sorted_tuples:
				out.write(str('{0:.4f}'.format(tup[1])).encode('utf-8') + '\t' + str(tup[0].encode('utf-8')) + '\n') 
				print(str('{0:.4f}'.format(tup[1])).encode('utf-8') + '\t' + str(tup[0].encode('utf-8')) + '\n') 

		collocates = {} # Resets

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
