#coding=utf8
'''
Anna Bonazzi, 16/08/2017

Script to make a plot of part-of-speech frequency (in %) in each corpus class. 

Current settings for python 2.7. Fpr python 3, comment all the ".decode('utf-8')" out.
'''
# To time the script
from datetime import datetime
startTime = datetime.now()

import os, glob, re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#--------------------------
# VARIABLES FOR USER TO CHANGE

lang = 'fr' # fr, de, it, en
input_file = '/path/to/corpus_file.vrt'

keyw1 = "Nomina"
keyw2 = "Adjektive"
keyw3 = "Verben"
keyw4 = "Adverbien"
keyw5 = "Pronomina"
keyw6 = "Artikel"

# You can run after editing here
#---------------------------

# 1) Collects data from corpus: for each class, 1) total word freq and 2) pos freq 

if lang == 'fr':
	pos = {'Nomina': '(NAM|NOM)', 'Adjektive': 'ADJ', 'Verben': 'VER.*?', 'Adverbien': 'ADV', 'Pronomina': 'PRO.*?', 'Artikel': 'DET.*?'}#, 'Andere' : ''}
elif lang == 'de':
	pos = {'Nomina': '(NN|NE)', 'Adjektive': 'ADJ.', 'Verben': '(VV|VA|VM).*?', 'Adverbien': '(ADV|PAV)', 'Pronomina': '(PD|PI|PP|PR|PW).*?', 'Artikel': 'ART'}#, 'Andere' : ''}
elif lang == 'it':
	pos = {'Nomina': '(NPR|NOM)', 'Adjektive': 'ADJ', 'Verben': 'VER.*?', 'Adverbien': 'ADV', 'Pronomina': 'PRO.*?', 'Artikel': '(DET.*?|PRE:det)'}#, 'Andere' : ''}
elif lang == 'en':
	pos = {'Nomina': '(NN|NP).?', 'Adjektive': 'JJ.*?', 'Verben': '(VB|VH|VV).?', 'Adverbien': 'W?RB.?', 'Pronomina': '(WP.?|WDT|PP.?)', 'Artikel': 'DT'}#, 'Andere' : ''}

# Prepares dictionary to save class
pab = {}; pbv = {}; peb = {}; pfu = {}
class_tot = {}
counter = 0
# Prepares temporary text as list								
chunk = [] 
# Counts average sent length
sent_length = {}
sent_total = {}
# Goes through corpus without reading it in.
with open (input_file, 'r') as f:
	print ('  Searching corpus. Go have some coffee...')
	sent_counter = 0
	for line in f:
		if '</text>' not in line: # Works text by text
			if '<' not in line:
				# Lemmas [2], wordforms [0], pos [1]
				chunk.append(line.split("\t")[1].decode('utf-8'))
			elif '<' in line:
				chunk.append(line)
		
		else: # Meets text end, works on temporary text chunk
			# Searches for chosen lang/class combination
			regex = re.search('class="(.*?)".*?language="'+lang+'"', ''.join(chunk))
			if regex:
				cl = regex.group(1)
				for word in chunk:
					if '<' not in word:
						sent_counter += 1 # Sentence length
						if cl in class_tot:
							class_tot[cl] += 1
						else:
							class_tot[cl] = 1
						#-----------------
						# Counts frequency per part-of-speech
						def fill_dic(dic):
							fill = 0
							for p in pos:
								reg = pos[p].decode('utf-8')
								regex2 = re.search(reg, word)
								if regex2:
									fill = 1
									if p in dic:
										dic[p] += 1
									else:
										dic[p] = 1
							'''
							# Catches other pos
							if fill == 0:
								if 'Andere' in dic:
									dic['Andere'] += 1
								else:
									dic['Andere'] = 1
							'''
							return dic
						#-----------------
						# Counts word stats in chosen corpus part
						if cl == 'pab':
							pab = fill_dic(pab)	
						elif cl == 'pbv':
							pbv = fill_dic(pbv)
						elif cl == 'peb':
							peb = fill_dic(peb)
						elif cl == 'pfu':
							pfu = fill_dic(pfu)
					elif '</s' in word:
						if cl in sent_total:
							sent_total[cl] += 1
						else:
							sent_total[cl] = 1
							
						if cl in sent_length:
							sent_length[cl] += sent_counter
						else:
							sent_length[cl] = sent_counter
						sent_counter = 0 # Resets for new sentence
			chunk = [] # Resets empty list
			counter += 1
			if '00000' in str(counter):
				print ("\tText " + str(counter))

sent_average = {}
for cl in sent_length:
	sent_average[cl] = float("{:.2f}".format(sent_length[cl] / sent_total[cl]))

#------------------------------------

# 2) Bar plot

'''
# One bar group
labels = ['PAB', 'PBV', 'PEB', 'PFU']
y = [30, 40, 23, 55]
x = [1, 2, 3, 4]
barlist = plt.bar(range(len(dic)), dic.values(), align='center')
# bar options: color='b', edgecolor =, hatch = patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
'''

# Multiple bar groups
#ax.bar([x + dist for x in range(len(dic1))], dic1.values(),width=0.3, align='center', color='#b9e1b4')

ax = plt.subplot(111)

tick_loc = []
pos_order = ['Nomina','Adjektive', 'Verben', 'Adverbien', 'Pronomina', 'Artikel']
#-----------------
def make_bar(dic, tot, x_loc):
	# Prepares x
	dist = 0.31
	x = []
	for i in range (0, len(dic.items())):
		x.append(x_loc + dist * i)
	# Fixes position of x ticks
	tick_loc.append(x_loc + (len(dic.items()) / 2) - 2)

	# Prepares y
	y = []
	
	for p in pos_order:
		if p in dic:
			# Takes y values as percentages
			y.append(float("{:.2f}".format(dic[p] * 100 / class_tot[tot])))

	# Plots line\t
	barlist = ax.bar(x, y, width=0.3, align='center')#, color=bar_color) 
	colors = ['#c62828', '#512da8', '#1976d2', '#00796b', '#ff8f00', '#ffeb3b'] # blue-pab, green-pbv, yellow-pfu, red-peb
	for i in range (0, len(x)):
		barlist[i].set_color(colors[i])
	
	return x, y
#-----------------
ticks = []
# Makes bar groups and tick names for existing classes
if 'pab' in sent_average:
	x, y = make_bar(pab, 'pab', 2)
	ticks.append("PAB\n(Wirtschaft)\nDurchschn. Satzlänge: ".decode('utf-8')+str(sent_average['pab']).decode('utf-8'))
if 'pbv' in sent_average:
	make_bar(pbv, 'pbv', 5)
	ticks.append("PBV\n(Medien)\nDurchschn. Satzlänge: ".decode('utf-8')+str(sent_average['pbv']).decode('utf-8'))
if 'peb' in sent_average:
	make_bar(peb, 'peb', 8)
	ticks.append("PEB\n(Wissenschaft)\nDurchschn. Satzlänge: ".decode('utf-8')+str(sent_average['peb']).decode('utf-8'))
if 'pfu' in sent_average:
	make_bar(pfu, 'pfu', 11)
	ticks.append("PFU\n(Politik)\nDurchschn. Satzlänge: ".decode('utf-8')+str(sent_average['pfu']).decode('utf-8'))


# Set x ticks
x_positions = []
plt.xticks(tick_loc, ticks, fontsize = 14)

# Set axis labels
plt.xlabel('\nAnteil der Klassen im Korpus:\nPBV: 50.17%, PFU: 19.59%, PEB: 17.53%, PAB: 12.69%', fontsize = 14)
plt.ylabel("Prozentsatz \n", fontsize = 14)


# Set legend
'''
leg = plt.legend(pos.keys(), loc='best', frameon=False, facecolor = 'r') # edgecolor = 'b'
for text in leg.get_texts():
\ttext.set_fontsize(12)
'''

# Set text box
plt.text(12, 20, '1) Nomina\n2) Adjektive\n3) Verben\n4) Adverbien\n5) Pronomina\n6) Artikel', fontsize=14)

# Set grid
plt.grid(True)
ax.grid(color='gray', linestyle='-', linewidth=0.2) # Requires ax = fig.add_subplot(111)

# Set title
langs = {'de' : 'Deutsch', 'fr' : 'Französisch', 'it' : 'Italienisch', 'en' : 'Englisch'}
plt.title('Wortarten - '+langs[lang].decode('utf-8')+':\nAnteil in jeder Akteursklasse', fontsize = 16)

ax.autoscale(tight=False)
plt.show()

#matplotlib.pyplot.barh(yaxis, ywidths, 1, xaxis, x_labels)

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
