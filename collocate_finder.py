#coding=utf8
'''
Anna Bonazzi, 06/10/2017

Script to find collocates of specific words from a corpus.

What the script does:
	1) Assembles corpus texts with chosen language. Text is assembled as a list.
	2) Saves frequency of searchwords/acceptable word versions from regex
	3) Finds collocations (basis-collocate pairs) in window of given size with nltk
	4) Selects collocations containing the desired searchword
	5) Sorts each searchword's collocates by pmi or log-likelihood value

! Requires all the encode/decode in python2.7 (comment it out for python 3).
'''
#--------------------------
# VARIABLES FOR USER TO CHANGE:

search_words = ['genevois', 'stratégie énergétique']
reg_ex = {'genevois' : '(?i)genevoise?s?', 'stratégie énergétique' : '(?i)stratégies? énergétiques?'} # If you don't want to search by regex, comment this line out

lang = 'fr'

input_file = '/path/to/corpus_file.vrt'
output_folder = '/path/to/collocates_folder/'

min_freq = 3 # Minimum collocation frequency to be considered
window_size = 6 # Size of word window to search for collocates. 6 is standard (5 right/left)

unit = 'wordform' # Options: 'lemma', 'wordform', 'pos'
# Hint: When searching by regex, use "word". When searching by plain word, use "lemma".

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
from collections import defaultdict
# To recognize punctuation
import string
#---------------------

# Prepares to removes punctuation
punct = set(string.punctuation + '»' + '«')

# 1) Assembles text with chosen properties/language
multiple = 0
flag1 = 0 # Prepares to search by word or by regex
searchwords = []
for i in range(0, len(search_words)):
	searchwords.append(search_words[i].decode('utf-8'))
try:
	regexes = {}
	for sw in searchwords:
		reg = reg_ex[sw.encode('utf-8')].decode('utf-8')
		if '.*?' in reg:
			reg = reg.replace('.*?', '.*') # But why???
			pass
		if ' ' in reg:
			multiple = 1			
		regexes[sw] = reg
	flag1 = 1
except:
	pass

text_counter = 0 # To keep track
chunk = [] # Prepares temporary text as list
text = []
sw_freq = {}
acceptables = defaultdict(list) # prepares to save acceptable regex versions

print ('\nGoing through corpus. Go have a coffee...')
with open (input_file, 'r') as f:
	for line in f:
		if '</text>' not in line: # Works text by text
			if '<' not in line:
				units = {'wordform' : 0, 'pos' : 1, 'lemma' : 2} 
				chunk.append(line.split("\t")[units[unit]].decode('utf-8'))
					
			elif '<text' in line:
				chunk.append(line.decode('utf-8'))
			elif '</s' in line:
				chunk.append(line.strip('\n').decode('utf-8'))
	
		else: # Meets current text end
			chunk.append(line.decode('utf-8'))
		  	# Checks text for chosen properties
			regex = re.search('class="(.*?)".*?language="'+lang, ''.join(chunk))
			if regex:
				chunk = chunk[1:]
				joined_chunk = ' '.join(chunk)
				if multiple == 1:
					# Connects multiple word units for easy search
					for key in regexes:
						if ' ' in key:
							regex2 = re.findall(regexes[key], joined_chunk)
							if regex2:	
								for version in set(regex2):
									if type(version) is tuple:
										version = version[0]
									newversion = version.replace(' ', '_')
									# Modifies text to have "multiple units" as "multiple_units"
									joined_chunk = joined_chunk.replace(version, newversion)	
				
				chunk = joined_chunk.split(' ')
	
				for word in chunk:
					# Excludes xml and punctuation
					if '<' not in word and word.encode('utf-8') not in punct: 
						text.append(word)
						# Counts word freq by word
						if flag1 == 0:	
							if (sw or sw.lower() or sw.title() or sw.upper()) == word:
								if sw not in sw_freq:
									sw_freq[sw] = 1
								else:
				
									sw_freq[sw] += 1
						
						# Or counts word freq by regex
						else:
							for key in regexes:
								# Checks searchwords one by one
								regex2 = re.search(regexes[key], word)
								if regex2:
									# Counts word freq
									if key in sw_freq:
										sw_freq[key] += 1
									else:
										sw_freq[key] = 1
									version = regex2.group(0)
									# Saves found searchword versions
									if key in acceptables:
										acceptables[key] = acceptables[key] + list([version])
									else:
										acceptables[key] = list([version])
									acceptables[key] = list(set(acceptables[key]))
										
			text_counter += 1
			if '00000' in str(text_counter):
				print ("\tText " + str(text_counter))
			chunk = [] # Resets empty chunk for next corpus text

# Corpus searching is over - Text is collected as a list

# Prepares text (from list or string) in nltk format
corpus = nltk.Text(text) # From list
#corpus = nltk.wordpunct_tokenize(text) # From string
text = [] # Frees up memory

#---------------------------------
# 2) Makes collocations

for sw in searchwords:
	flag = 0 # To skip working for irrelevant words
	print ('\nNow looking for collocates of "' + sw +'"')
					
	if sw not in sw_freq or sw_freq[sw] == 0:
		print ('\n\tSearchword "' + sw + '" not in corpus.\n')
		flag = 1
	elif sw_freq[sw] > 0 and sw_freq < min_freq:
		print ('\n\tSearchword "' + sw + '" not frequent enough.\n')
		flag = 1
	else:
		print ('\n\tSearchword "' + sw + '" is there ' + str(sw_freq[sw]) + ' times')

	if flag == 0:
		time1 = datetime.now() - startTime
		print ('\tMaking collocations after ' + str(time1) + '\n')	

		# Makes 2-/3-grams with PMI or log-likelihood values and given window size
		bigram_measures = nltk.collocations.BigramAssocMeasures()
		bi_finder = BigramCollocationFinder.from_words(corpus, window_size = window_size)

		# Flters ngrams

		# Filters ngrams by frequency
		bi_finder.apply_freq_filter(min_freq)
		# Filters out ngrams with sentence boundary
		my_filter = lambda *w: '</s>' in w
		bi_finder.apply_ngram_filter(my_filter)
		# a) Filters ngrams by searchword
		if flag1 == 0:
			# Throws away ngrams where neither element is the searchword
			my_filter = lambda *w: sw not in w and sw.lower() not in w
			bi_finder.apply_ngram_filter(my_filter)
		# b) Or filters ngrams by regex
		if flag1 == 1:
			# Throws away bigrams where neither element is the searchword
			my_filter = lambda w1, w2: w1 not in acceptables[sw] and w2 not in acceptables[sw]
			bi_finder.apply_ngram_filter(my_filter)
		print ('\tWord filter applied')
		
		# Makes collocations
		if coll_measure == 'likelihood_ratio':
			bi_list = bi_finder.score_ngrams(bigram_measures.likelihood_ratio)
		else:
			bi_list = bi_finder.score_ngrams(bigram_measures.pmi)
		if (len(bi_list)) > 0:
			print ('\nCollocates of "'+sw+'" done!\n')
		
	#----------------------------------------	
	# 3) Sorts collocates by their log-lik or pmi value

		collocates = {}
		# Prepares to remove stopwords
		pairs = {'de' : 'german', 'fr' : 'french', 'en' : 'english', 'it' : 'italian'}
		stop = set(stopwords.words(pairs[lang]) + ['L', 'l', '’', 'être', 'card', 'avoir', '@card@', 'S', '’', '@ord@'])
		# Collocation format: ((word1, word2), (log-l-value))
		
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
					if (word and word.title() and word.lower()) not in acceptables[sw] and word not in stop:
						if word not in collocates:
							collocates[word] = coll[1]
						else:
							collocates[word] += coll[1]
		bi_list = []
		# Sorts and prints out
		sorted_tuples = sorted(collocates.items(), key=lambda pair: pair[1], reverse=True)
		with open (output_folder + lang + '_' + sw + '.txt', 'a') as out:
			for tup in sorted_tuples:
				out.write(str('{0:.4f}'.format(tup[1])).encode('utf-8') + '\t' + str(tup[0].encode('utf-8')) + '\n') 
				#print(str('{0:.4f}'.format(tup[1])).encode('utf-8') + '\t' + str(tup[0].encode('utf-8')) + '\n') 
				#pass

		collocates = {} # Resets	

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
