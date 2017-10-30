#coding=utf8
'''
Anna Bonazzi, 06/09/2017

Script to find frequency of specific words from a corpus.

What the script does:
	1) Selects texts of chosen language
	2) Saves frequency of searchwords through regex

Current settings (".encode/.decode('utf-8)") for python2.7. Comment it out for python 3.
'''
#--------------------------
# VARIABLES FOR USER TO CHANGE:

languages = ['en', 'de']#lang = 'de'

#input_file = '/home/bonz/releases/sep17v2.vrt'
#output_folder = '/home/bonz/Corpus_work/GEothermie2020/frequenz/2'

input_file = '/home/bonz/Documents/Corpora/geothermie_test2.vrt'
output_folder = '/home/bonz/Documents/Corpus_work/GEothermie2020/frequenz/9'

unit = 'wordform' # Options: 'lemma', 'wordform', 'pos'

# Specify regexes for each chosen language below!

#---------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re, sys
#---------------------
for lang in languages:
	if lang == 'de':
		word_counter = 0
		regexes = {'Atomkraft' : '(nuklear.*?|^atom.*?)', 'Geothermie' : 'geotherm.*', 'Solarkraft':'(sonnen(k|e).*|solar(k|e).*|photovolt.*)', 'Fossil':'(fossil.*?|kohl.*?)', 'Erneuerbar':'erneuerb.*', 'Windkraft':'windk.*?', 'Biomasse':'Biomas.*', 'Wasserkraft':'(wasser(k|e).*|hydroel.*)', 'Holzenergie':'holz-?(kr|en).*?'}# Uppercase/Lowercase will be fixed later
	elif lang == 'fr':
		regexes = {'Nucléaire': '(nucléai.*|atomiq.*)', 'Géothermie': 'géotherm.*', 'Solaire': '(solair.*?|photovolt.*)', 'Fossile': '(fossil.*?|charbon)', 'Renouvelable': 'renouvelab.*?', 'Éolien': 'éolien.*?', 'Biomasse': 'biomass.*?', 'Hydroélectrique': 'hydr(au|oé).*', 'Bois': '^bois.*?'}
		word_counter = 0
	elif lang == 'it':
		regexes = {'Nucleare': '(nuclea.*|atomic.*)', 'Geotermia': 'geoterm.*', 'Solare': '(solar.*?|fotovolt.*)', 'Fossile': '(fossil.*?|carbone)', 'Rinnovabile': 'rinnovabil.*?', 'Eolico': '(eolic.*?|vento)', 'Biomassa': 'biomass.*?', 'Idroelettrico': 'idroelettri.*', 'Legno': 'legn(o|a|ame)'}
		word_counter = 0
	elif lang == 'en':
		regexes = {'Nuclear' : '(nuclear.*?|^atom.*)', 'Geothermal' : 'geotherm.*', 'Solar':'(solar.*?|photovolt.*)', 'Fossil':'(fossil|coals?)', 'Renewable':'renewables?', 'Wind':'wind$', 'Biomass':'Biomasse?s?', 'Water energy':'(hydroel|hydraul)', 'Wood':'(wood$|timber)'}
		word_counter = 0
	switch = 0
	# Prepares dictionaries to save classes
	pab ={}; pbv = {}; peb = {}; pfu = {}
	def initiate_dic(dic, regexes):
		for keyword in regexes:
			if keyword not in dic:
				dic[keyword] = 0
		return dic
	pab = initiate_dic(pab, regexes); pbv = initiate_dic(pbv, regexes)
	peb = initiate_dic(peb, regexes) ; pfu = initiate_dic(pfu, regexes)
	# Searches corpus
	print ('\nGoing through corpus. Go have a coffee...')
	text_counter = 0 # To keep track
	chunk = [] # Prepares temporary text as list
	with open (input_file, 'r') as f:
		for line in f:
			if '</text>' not in line: # Works text by text
				if '<' not in line:
					units = {'wordform' : 0, 'pos' : 1, 'lemma' : 2} 
					chunk.append(line.split("\t")[units[unit]].decode('utf-8'))
					
				elif '<text' in line:
					chunk.append(line.decode('utf-8'))
	
			else: # Meets current text end
				chunk.append(line.decode('utf-8'))
			  	# Checks text for chosen properties
				regex = re.search('class="(.*?)"', ''.join(chunk))
				if regex:
					cl = regex.group(1)
					old_cl = cl
				else:
					cl = old_cl
				try:
					regex1 = 
					if regex1:
						switch = 1
				except:
					# Finds languages
					languages = re.findall('(de=".*?)".*?(en=".*?)".*?(fr=".*?)".*?(it=".*?)".*?(other=".*?)"', ''.join(chunk))
					# Makes lang - percent pairs
					lang_dic = {}
					if languages:
						for l in list(languages[0]):
							lang_dic[l.split('="')[0]] = float(l.split('="')[1])

						# Sorts percents to find the highest	
						languages = [float(l.split('="')[1]) for l in list(languages[0])]
						languages.sort()
						if lang_dic[lang] == languages[-1]:
							# Selects desired language
							switch = 1
					if switch == 1:
						for word in chunk:
							if '<' not in word:
								word_counter += 1
								for keyword in regexes:
									reg = regexes[keyword].decode('utf-8')
									regex = re.search('(?i)'+reg, word)
							
									if regex:
										if 'pab' in cl:
											pab[keyword] += 1
										elif 'pbv' in cl:
											pbv[keyword] += 1
										elif 'peb' in cl:
											peb[keyword] += 1
										elif 'pfu' in cl:
											pfu[keyword] += 1
			
				text_counter += 1
				if '000000' in str(text_counter):
					print(text_counter)
				chunk = []

	# Prints out in searchable form
	#keyw1 = "Nucléaire / atomique"	
	#dic1 = {"pab": 856, "pbv": 7495, "peb": 8, "pfu": 509}

	keywords = pab.keys()
	i = 0
	with open (output_folder + lang + '_energiesorten.txt', 'a') as out:
		for keyword in keywords:
			i += 1
			print('keyw'+str(i)+' = "'+keyword+'"')
			out.write('keyw'+str(i)+' = "'+keyword+'"\n')
	# Prints in absolute
	i = 0
	with open (output_folder + lang + '_energiesorten.txt', 'a') as out:
		out.write('\n\n')
		for keyword in keywords:
			i += 1
			print('dic'+str(i)+' = {"pab": '+str(pab[keyword])+', "pbv": '+str(pbv[keyword])+', "peb": '+str(peb[keyword])+', "pfu": '+str(pfu[keyword])+'}')
			out.write('dic'+str(i)+' = {"pab": '+str(pab[keyword])+', "pbv": '+str(pbv[keyword])+', "peb": '+str(peb[keyword])+', "pfu": '+str(pfu[keyword])+'}\n')
	# Prints in percent	not per class	
	i = 0
	with open (output_folder + lang + '_energiesorten.txt', 'a') as out:
		out.write('\n\n')
		for keyword in keywords:
			i += 1
			freq = '{:.4f}'.format(float(float(pab[keyword] + pbv[keyword] + peb[keyword] + pfu[keyword]) * 1000000 / word_counter))
			
			print('dic'+str(i)+' '+str(freq)+' von '+str(word_counter)+' Wörtern')
			out.write('dic'+str(i)+' '+str(freq)+' von '+str(word_counter)+' Wörtern\n')
		out.write('\n\n-------\n\n')
	print('\n\n')
#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")	
