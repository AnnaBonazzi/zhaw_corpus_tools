#coding=utf8
'''
Anna Bonazzi, 16/08/2017

Script to make a plot of corpus word frequency evolution over time by language.
Word frequency is taken from the corpus.vrt file, one text at a time. 

Works both for corpora with a "language" attribute and for corpora with different percentages for each language
'''
# VARIABLES FOR USER TO CHANGE:

corpus = '/home/bonz/Documents/Corpora/geothermie_test3.vrt'

#selected_sources = '/home/bonz/Documents/Corpus_work/Quellen/pbv_quellen_juli.txt' # Comment out if not needed

keyword = 'Geothermie'

regex_fr = '(G|g)(e|é)o(t|th)erm.*?'
regex_de = '(G|g)(e|é)o(t|th)erm.*?'
regex_en = '(G|g)(e|é)o(t|th)erm.*?'
regex_it = '(G|g)(e|é)o(t|th)erm.*?'

# Time window to search
min_year = 2007; max_year = 2017

frequency = 'per_million' # Options: 'absolute', 'per_million'
unit = 'word' # Options: 'word', 'pos', 'lemma'

# Overall plot attributes
myfont = 'DejaVu Sans' # Arial
fontcolor = '#185a92' # Pick colors from http://htmlcolorcodes.com/
#--------------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#--------------------------

# 1) Collects data

# Prepares dictionary to save word freq by language
de = {}; fr = {}; it = {}; en = {}
dic = {}
text_counter = 0
all_words = {}
# Temporary text chunk to be analyzed
chunk = []

# Optional ist of sources to be searched for specific queries (e.g. media) 
sources = []
try:
	with open (selected_sources, 'r') as f:
		for word in f:
			sources.append(word.strip('\n'))
except:
	pass

# Goes through the corpus one text at at time
with open (corpus, 'r') as f:
	print ('  Searching corpus. Go have some coffee...')
	for line in f:
		if '</text>' not in line:
			if '<' not in line:
				units = {'word' : 0, 'pos' : 1, 'lemma' : 2}
				word = line.split("\t")[units[unit]] # 0 wordform, 1 pos, 2 lemma
				chunk.append(word) # Fills temporary text chunk with lemmas
			elif '<text' in line:
				chunk.append(line)
		else: # Meets text end
			# Searches for selected lang and class combination
			regex = re.search('.*?class="(.*?)".*?date_published="(.*?)".*?source="(.*?)".*?', ''.join(chunk))
			if regex:
				regex2 = re.search('language="(.*?)"', ''.join(chunk))
				if regex2:
					lang = regex2.group(1)
				else:
					languages = re.findall('(de=".*?)".*?(en=".*?)".*?(fr=".*?)".*?(it=".*?)".*?(other=".*?)"', ''.join(chunk))
					# Makes lang - percent pairs
					lang_dic = {}
					if languages:
						for l in list(languages[0]):
							lang_dic[l.split('="')[0]] = float(l.split('="')[1])
						# Sorts percents to find the highest	
						languages = [float(l.split('="')[1]) for l in list(languages[0])]
						languages.sort()
						candidates = []
						for l in lang_dic:
							if lang_dic[l] == languages[-1]:
								candidates.append(l)
								# If there are several options, 'other' does not get picked
								lang = candidates[0]
								if len(candidates) > 1 and 'other' in candidates:
									if lang == 'other':
										lang = candidates[1]
									if len(candidates) > 1 and 'en' in candidates and 'other' not in candidates:
										if lang == 'en':
											lang = candidates[1]
								if len(candidates) > 2 and 'en' in candidates and 'other' in candidates:
									if lang == 'en':
										lang = candidates[1]
										if len == 'other':
											lang == [2]
				
				cl = regex.group(1); source = regex.group(3)
				try:
					l = len(selected_sources)
					print (l)
				except:
					sources = []
					sources.append(source)
				# Counts words by language
				if lang in all_words:
					all_words[lang] += 1
				else:
					all_words[lang] = 1
		
				# Looks only in selected sources
				if source in sources: 
					if '-' in regex.group(2):
						date = regex.group(2)
						# Checks date: right format, right time window
						if len(date.split('-')[0]) == 4 and int(date.split('-')[0]) >= min_year and int(date.split('-')[0]) <= max_year and int(date.split('-')[0]) < 9999:
							if int(date.split('-')[1]) > 7: # Makes half-years
								year = str(date.split('-')[0]) + ".2"
							else:
								year = str(date.split('-')[0]) + ".1"

							#------------------
							# Counts searchword frequency per language or year
							def fill_dic(dic, year, lang, reg):	
								for word in chunk:
									regex2 = re.search(reg, word)
									if regex2:
										if year in dic:
											dic[year] += 1
										else:
											dic[year] = 1
								return dic
							#------------------
							if lang == 'fr':
								fr = fill_dic(fr, year, lang, regex_fr)	
							if lang == 'de':
								de = fill_dic(de, year, lang, regex_de)
							if lang == 'en':
								en = fill_dic(en, year, lang, regex_en)
							if lang == 'it':	
								it = fill_dic(it, year, lang, regex_it)			
			
			chunk = [] # Resets empty text chunk
			text_counter += 1
			if '00000' in str(text_counter):
				print ("\tText " + str(text_counter))
		
#------------------------------------
# 2) Starts making plot

print ('Starting plot')
# Sorts dictionaries and fills x/y lists
def plot_line(dic, linecolor, lang_tot):
	# Fills x/y axes
	x = []
	y = []
	xlist = []
	# Absolute Frequency
	if frequency == 'absolute':
		ytitle = 'Absolute Frequenz'
		for i in range (2007, 2018):
			if str(i + 0.1) in dic:
				xlist.append(str(i))
				y.append(dic[str(i + 0.1)])
			else:
				xlist.append(str(i))
				y.append(0)
			if str(i + 0.2) in dic:
				xlist.append('')
				y.append(dic[str(i + 0.2)])
			else:
				xlist.append('')
				y.append(0)
		for i in range (1, len(xlist) + 1):
			x.append(i)
	else:	
		# Frequency per million
		ytitle = 'Frequenz per 100'
		for i in range (min_year, max_year + 1):
			if str(i + 0.1) in dic:
				xlist.append(str(i))
				freq = int(dic[str(i + 0.1)]) * 100 / lang_tot
				y.append(float("{:.5f}".format(freq)))
			else:
				xlist.append(str(i))
				y.append(0)
			if str(i + 0.2) in dic:
				xlist.append('')
				freq = int(dic[str(i + 0.2)]) * 100 / lang_tot
				y.append(float("{:.5f}".format(freq)))
			else:
				xlist.append('')
				y.append(0)
		for i in range (1, len(xlist) + 1):
			x.append(i)
	
	# Plots the line
	plt.plot(x, y, color=linecolor, linewidth = 3,  marker='o', linestyle='-') # label = 
	
	return xlist, x, y, ytitle
#------------------
	
xlist, x, y, ytitle = plot_line(fr, '#bbcbdb', all_words['fr'])
plot_line(de, '#9ebd9e', all_words['de'])
plot_line(en, '#dd855c', all_words['en'])
plot_line(it, '#745151', all_words['it'])

# Set ax ticks
plt.xticks(x, xlist, fontname = myfont, fontsize = '16') # xlist, 
plt.yticks(fontname = myfont, fontsize = '16')

# Get current figure and then add subplot - to do additional format stuff
fig = plt.gcf() 
ax = fig.add_subplot(111)
'''
# Set datapoint labels:
pointlabels = ['60\nMio.', '114.8\nMio.', '166.6    \nMio.', '331.6\n   Mio.     ', '    358\n     Mio.', '  N/A', '457.9\nMio.', '1.03\nMia.']
for i, j in zip(x, y):  
	# Pick element from desired label list through index of current i
	pointlabel = pointlabels[x.index(i)]
	ax.annotate(pointlabel, xy=(i,j), xytext=(-25,15), textcoords='offset points', fontname = myfont, fontsize = '16')
''' 
         
# Set ax labels
#plt.xlabel('Releases', color = fontcolor, fontname = myfont, fontsize = '20', position = (0.5, 0.5))

plt.ylabel(ytitle, color = fontcolor, fontname = myfont, fontsize = '20', position = (-1, 0.5))


# Set title 
plt.title(keyword + '\n', color = fontcolor, fontname = myfont, fontsize = '24')

# Set subtitle (use suptitle - moves up with \n)
plt.suptitle('\n\nEntwicklung je nach Sprache (' + xlist[0] + '-' + xlist[-2] + ')', color = fontcolor, fontname = myfont, fontsize = '16')# , position = (-1, 0.5))

# Set legend
leg = plt.legend(loc='best', frameon=False, facecolor = 'r',  labels = ['Fr', 'De', 'En', 'It']) # edgecolor = 'b', # Don't have to specify them unless to change them

# Change all legend 
for text in leg.get_texts():
    text.set_fontsize(16)
    text.set_fontname(myfont)
    text.set_color(fontcolor)
    
# Change legend elements individually
#text = leg.get_texts() # get lines, patches, title, set_frame_on(True|False), set_title
#text[0].set_color('c')

 # Set / edit edge
plt.box(on=True) # Or nothing, to make the box disappear
       
# Set / edit grid
plt.grid()
ax.grid(color='paleturquoise', linestyle='-.', linewidth=0.5) # Requires ax = fig.add_subplot(111)

# Set background
# fig.set_facecolor('c') # Color around the plot
#ax.set_facecolor('#f5ffff') # Needs box to work

# Edit plot size
fig.set_size_inches(12,6.5)# Needs fig = plt.gcf()
plt.tight_layout() # Adjusts subplot params for the subplot(s) to fit in the figure area

# Show plot
plt.show()
# Save plot
fig.savefig('/home/bonz/Documents/Corpus_work/Images/100-3_entwickl_geo_medien.png')

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
