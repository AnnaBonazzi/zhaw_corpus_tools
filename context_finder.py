#coding=utf8
'''
Anna Bonazzi, 15/10/2017

Script to find context of previously found collocations.
Makes ngrams of desired length containing two specific words (basis and changing collocate), plus a window of 10 words left and right around. 
Makes ngrams for different corpus sections (in this case, corpus is divided by class and language) using nltk ngrams, returns absolute frequency and frequency per million.

Current settings with ".decode('utf-8')" for python 2.7. Comment out for python 3
'''
#------------------------------
# VARIABLES FOR USER TO CHANGE

input_file = '/home/anna/Documents/corpus_work/corpora/geothermie_sep17.vrt'
output_folder = '/home/anna/Documents/corpus_work/geothermie/fundstellen/'

langs = ['fr'] # 'fr', 'de', 'en', 'it'
unit = 'wordform' # 'wordform', 'pos', 'lemma'
n = 6 # Ngram window with nltk
context = 10 # Context words left and right of the ngram

min_freq = 0#2 # Minimum ngram frequency
max_number = 500 # Number of ngrams to show

searchword = '(G|g)éotherm.*'; keyw = 'Géothermie' # Comment out if not needed
collocates = {'profonde' : '(?i)profond.?.?', 'renouvelable' : '(?i)renouvelable.?', 'responsable' : '(?i)responsable.?', 'transition' : '(?i)transition.?', 'SIG' : '(?i)SIG', 'énergétique' : '(?i)énergétique.?', 'nouvelle' : '(?i)nouvel.?.?.?', 'profondeur' : '(?i)profondeur.?', 'sonde' : '(?i)sonde.?', 'biomasse' : '(?i)biomasse.?', 'solaire' : '(?i)(solaire.?|photovolta.que.?)', 'chaleur' : '(?i)chaleur.?', 'moyenne' : '(?i)moyen.?.?.?', 'hydrothermale' : '(?i)hydrothermale.?'}
#------------------------------

from collections import defaultdict
from nltk import ngrams
import re
# To time the script
from datetime import datetime
startTime = datetime.now()

for lang in langs:	
	# Makes collocations with each of the above words
	for collocate in collocates:
		ngram_contexts = defaultdict(list) # Dic of lists
		dry_ngrams = {}
		tot_grams = 0
		print ('\nSearching in language '+lang.title()) 
		pab = [] ; pbv = []; peb = []; pfu = []					
		chunk = [] # Prepares temporary text as list		
		counter = 0
		units = {'wordform' : 0, 'pos' : 1, 'lemma' : 2}
		# Goes through corpus
		with open (input_file, 'r') as f:
			for line in f:
				if '</text>' not in line: # Works text by text
					if '<' not in line:
						chunk.append(line.split("\t")[units[unit]].decode('utf-8'))
					elif '<text' in line or '</s' in line:
						chunk.append(line)
				
				else: # Meets text end, works on temporary text chunk
					chunk.append(line.decode('utf-8'))
					temp_chunk = [] # Prepares to save ngrams of this chunk temporarily
				  # Selects texts with chosen lang/class combination
					regex = re.search('class="(.*?)".*?language="'+lang+'".*?source="(.*?)"', ''.join(chunk))
					grams = []
					if regex:
						cl = regex.group(1); source = regex.group(2)
						temp = []
						for word in chunk:
							if '<text' not in word and '</text' not in word:
								# Increases ngram to desired length
								while len(temp) < n:
									temp.append(word)
								if len(temp) == n:
									# Checks if temporary ngram has selected words
									gram = ' '.join(temp)
									try:
										regex_sw = re.search(searchword, gram) 
										regex_c = re.search(collocates[collocate]+' ', gram) 
										#print (gram)
										if '</s>' not in temp:
											if regex_sw and regex_c: # If searchword is given
												tot_grams += 1
												# Saves ngram for this chunk
												grams.append(gram)
												
									# Or saves ngram if searchword is not given
									except:
										if '</s>' not in gram: # Respects sentence boundary
											tot_grams += 1
											grams.append(gram)
										
									# Deletes 1st ngram word, shifts ngram to the right by 1
									del temp[0]
				
					# Counts ngrams and contexts
					for gram in grams: 
						regex1 = re.search('('+searchword+'.*? '+collocates[collocate]+' )', gram)
						regex2 = re.search(' ('+collocates[collocate]+' .*?'+searchword+')', gram)
						if regex1 or regex2:
							if regex1:
								dry_gram1 = regex1.group(1)
								# Counts frequency of different dry grams
								if searchword + ' + ' + collocate in dry_ngrams:
									dry_ngrams[searchword + ' + ' + collocate] += 1
								else:
									dry_ngrams[searchword + ' + ' + collocate] = 1
								# Prepares to save different contexts for each dry gram
							
							elif regex2:
								dry_gram2 = regex2.group(1)
								if searchword + ' + ' + collocate in dry_ngrams:
									dry_ngrams[searchword + ' + ' + collocate] += 1
								else:
									dry_ngrams[searchword + ' + ' + collocate] = 1
							
					# Finds context words in the current text chunk
					for dry_gram in dry_ngrams:
						regex = re.search('(((\w+|\.|,|:|\!|\?|<\/s>|\n) ){2,10}('+searchword+'.*? '+collocates[collocate]+' | '+collocates[collocate]+' .*?'+searchword+')( ?(\w+|\.|,|:|\!|\?|<\/s>|\n)){2,12})', ' '.join(chunk ))
						if regex:
							# Completes gram + context with source name
							ngram_context = regex.group(1)
							ngram_context = re.sub('(\n|</s>)', '', ngram_context)
							ngram_context = source+'\t'+ngram_context
							#print(ngram_context)
							# Saves several contexts for each dry gram
							if dry_gram in ngram_contexts:
								ngram_contexts[dry_gram] = ngram_contexts[dry_gram] + [ngram_context] # Not append
							else:
								ngram_contexts[dry_gram] = [ngram_context]
							
					chunk = []
					counter += 1
					if '00000' in str(counter):
						print ("\tText " + str(counter))
	
		# Sorts ngrams
		sorted_tuples = sorted(dry_ngrams.items(), key=lambda pair: pair[1], reverse=True)
		count = 0
		with open (output_folder + str(n)+'-grams_'+keyw+'_'+lang+'_'+unit+'1.txt', 'a') as out:
			for tup in sorted_tuples:
				if tup[1] >= min_freq and count <= max_number and '</s>' not in tup[0]:
					count += 1
					# Counts frequency per million 
					pmi = float('{:.2f}'.format(int(tup[1]) * 1000000 / tot_grams))
					out.write(str(tup[1]) + '\t'+ keyw + ' + ' + collocate + '\t' + str(pmi) + '\n\t' + '\n\t'.join(ngram_contexts[tup[0]]) + '\n\n\n')
					#print(str(tup[1]) + '\t'+ keyw + ' + ' + collocate + '\t' + str(pmi) + '\n\t' + '\n\t'.join(ngram_contexts[tup[0]]) + '\n\n\n') # str(pmi).decode('utf-8') 
					
		sorted_tuples = {}
#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
