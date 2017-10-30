#coding=utf8
'''
Anna Bonazzi, 06/09/2017

Script to find and plot word frequencies from a corpus for each corpus class

What the script does:
	1) Selects texts of chosen language
	2) Saves frequency of searchwords through regex for each class
	3) Plots the frequencies in a bar diagram

Current settings (".encode/.decode('utf-8)") for python2.7. Comment it out for python 3.
'''
#--------------------------
# VARIABLES FOR USER TO CHANGE:

input_file = '/path/to/corpus_file.vrt'
output_folder = '/path/to/word-frequency_folder/' # To save word frequencies
diagram_file = '/path/to/diagram_image_file.png'

lang = 'de'
regexes = {'Nuklear-Atom' : '(nuklear.*|atom.*)', 'Geothermie' : 'geotherm.*', 'Solarkraft':'(sonnen(k|e).*|solar(k|e).*|photovolt.*)', 'Fossil':'(fossil.*?|kohl.*?)', 'Erneuerbar':'erneuerb.*', 'Windkraft':'windk.*?', 'Biomasse':'Biomas.*', 'Wasserkraft':'(wasser(k|e).*|hydroel.*)', 'Holzenergie':'holz-?(kr|en).*?'}
 # Uppercase/Lowercase will be fixed later
legend_names = sorted(regexes.keys()) # Keywords are in alphabetic order

# Run from here. Or set more options:

unit = 'wordform' # Options: 'lemma', 'wordform', 'pos'

bar_colors = {legend_names[0] : '#7d6608', legend_names[1] : '#196f3d', legend_names[2] : '#4d5656', legend_names[3] : '#b03a2e', legend_names[4] : '#873600', legend_names[5] : '#17202a', legend_names[5] : '#f1c40f', legend_names[7] : '#2e86c1', legend_names[8] : '#aed6f1'} # Pick colors from http://htmlcolorcodes.com/

number_of_bar_groups = 4  # Change for more / less bar groups, e.g. for 5 or more subclasses
title = 'Energiesorten - September Release \'17\nKlassen'
y_axis_title = 'Absolute frequenz\n'

bar_group_names = {'pbv' : 'PBV\n(Medien)', 'pab' : 'PAB\n(Wirtschaft)', 'peb' : 'PEB\n(Wissenschaft)', 'pfu' : 'PFU\n(Politik)'} # For languages: {'fr' : 'Französisch', 'de' : 'Deutsch'...}

# You can run the script now

#---------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re, sys
import matplotlib
import matplotlib.pyplot as plt
#---------------------

frequencies = {} # Nested dictionary to save each searchword's frequency per class

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
					for word in chunk:
						if '<' not in word:
							for keyword in regexes:
								if keyword not in frequencies:
									frequencies[keyword] = {}
								reg = regexes[keyword].decode('utf-8')
								regex = re.search('(?i)'+reg, word)
								# Counts freqency per word per class
								if regex:
									if cl in frequencies[keyword]:
										frequencies[keyword][cl] += 1
									else:
										frequencies[keyword][cl] = 1
			
			text_counter += 1
			if '000' in str(text_counter):
				print(text_counter)
			chunk = []

# Prints out in searchable form
#keyw1 = "Nucléaire / atomique"	
#dic1 = {"pab": 856, "pbv": 7495, "peb": 8, "pfu": 509}

i = 0
with open (output_folder + lang + '_energiesorten.txt', 'a') as out:
	for keyword in legend_names:
		out.write('\n'+keyword.decode('utf-8')+'":\t')
i = 0
with open (output_folder + lang + '_energiesorten.txt', 'a') as out:
	for keyword in keywords:
		i += 1
		print('dic'+str(i)+' = {"pab": '+str(pab[keyword])+', "pbv": '+str(pbv[keyword])+', "peb": '+str(peb[keyword])+', "pfu": '+str(pfu[keyword])+'}')
		out.write('dic'+str(i)+' = {"pab": '+str(pab[keyword])+', "pbv": '+str(pbv[keyword])+', "peb": '+str(peb[keyword])+', "pfu": '+str(pfu[keyword])+'}\n')

#------------------------------------

# 2) Bar plot

# One bar
'''
labels = ['Bildung', 'Fachzeitung', 'Newsdienste', 'Tageszeitung', 'Wochenzeitung']
y = [1.28, 5.34, 15.76, 68.09, 9.50]
x = [1, 3, 5, 7, 9]
barlist = plt.bar(x, y, align='center')
#barlist = plt.bar(range(len(dic)), dic.values(), align='center')
# bar options: color='b', edgecolor =, hatch = patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
'''

# Multiple bars
ax = plt.subplot(111)
dist = 0.32

# Sets number of bar groups
xlist = []; n = 2; xlist.append(n)
for i in range(1, number_of_bar_groups):
	n = n + 3 # Tweak this number to make bar groups closer / farther
	xlist.append(n)
#xlist = [2, 5, 8, 11]

def make_bars(dic, dist, bar_color):
	ax.bar([x + dist for x in xlist], dic.values(),width=0.3, align='center', color=bar_color) 

#for word in legend_names:
make_bars(dic1, -(dist*4), bar_colors[keyw1])
make_bars(dic2, -(dist*3), bar_colors[keyw2])
make_bars(dic3, -(dist*2), bar_colors[keyw3])
make_bars(dic4, -(dist), bar_colors[keyw4])
make_bars(dic5, 0, bar_colors[keyw5])
make_bars(dic6, dist, bar_colors[keyw6])
make_bars(dic7, dist*2, bar_colors[keyw7])
make_bars(dic8, dist*3, bar_colors[keyw8])


#ax.bar([x + dist for x in range(len(dic1))], dic1.values(),width=0.3, align='center', color='#b9e1b4') 

# Set x ticks

labeldic = bar_group_names
plt.xticks(xlist, [labeldic[cl] for cl in dic1.keys()], fontsize = 14)

#plt.xticks(x, labels, fontsize = 14)

# Set individual bar colors / edges etc.
'''
colors = ['#334b97', '#12713b', '#973722', '#ffca06'] # blue-pab, green-pbv, yellow-pfu, red-peb
for i in range (0, len(colors)):
	barlist[i].set_color(colors[i])
	barlist2[i].set_linewidth(3)
	barlist2[i].set_edgecolor(colors[i])
	barlist1[i].set_linewidth(3)
	barlist1[i].set_edgecolor(colors[i])
'''

# Set x axis label
#plt.xlabel('\nAnteil der Klassen im Korpus:\nPBV: 50.17%, PFU: 19.59%, PEB: 17.53%, PAB: 12.69%', fontsize = 14)

# Set legend
leg = plt.legend(loc='best', frameon=False, labels = legend_names) # edgecolor = 'b', facecolor = 'r',
for text in leg.get_texts():
	text.set_fontsize(12)

# Set text box
#plt.text(4.2, 6000, 'Hauptakteure:\nTribune de Genève (4.581)\nLe Courrier (2.439)', fontsize=12)

# Set grid
ax = plt.subplot(111)
plt.grid(True)
ax.grid(color='paleturquoise', linestyle='-.', linewidth=0.5) # Requires ax = fig.add_subplot(111) or ax = plt.subplot(111)

# Set title
plt.title(title, fontsize = 14)
plt.ylabel(y_axis_title, fontsize = 14)

# Save and show
ax.autoscale(tight=False)
fig = plt.gcf()
fig.savefig(diagram_file, bbox_inches='tight')
plt.show()
#matplotlib.pyplot.barh(yaxis, ywidths, 1, xaxis, x_labels)

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
