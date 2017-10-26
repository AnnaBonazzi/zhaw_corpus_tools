#coding=utf8
'''
Anna Bonazzi, 16/08/2017

Script to make a plot of corpus words frequency for each corpus class or language, depending on the format of the input data.
Every keyword has its frequency dic with frequency per class/language.
For more / less words: add/remove a new keyword, a new dic, a new "make_bar"-function at line 75.
'''
# VARIABLES FOR USER TO CHANGE

output_file = '/path/to/image_file.png' # To save the figure

keyw1 = 'Nucléaire / atomique'.decode('utf-8')	
keyw2 = 'Géothermie / géothermique'.decode('utf-8')	
keyw3 = 'Solaire / photovoltaique'.decode('utf-8')	
keyw4 = 'Fossile'.decode('utf-8')	
keyw5 = 'Renouvelable'.decode('utf-8')	
keyw6 = 'Éolien'.decode('utf-8')	
keyw7 = 'Biomasse'.decode('utf-8')	
keyw8 = 'Hydroélectrique / hydraulique'.decode('utf-8')	

legend_names = [keyw1, keyw2, keyw3, keyw4, keyw5, keyw6, keyw7, keyw8] # Add / remove for more / less words

bar_colors = {keyw1 : '#17202a', keyw2 : '#a93226', keyw3 : '#f1c40f', keyw4 : '#717d7e', keyw5 : '#196f3d', keyw6 : '#aed6f1', keyw7 : '#7d6608', keyw8 : '#2874a6'} # Pick colors from http://htmlcolorcodes.com/

number_of_bar_groups = 4 # 4 for 4 classes. Change for more / less bar groups, e.g. for 5 or more languages

dic1 = {'pab': 856, 'pbv': 7495, 'peb': 8, 'pfu': 509}
dic2 = {'pab': 394, 'pbv': 202, 'peb': 1, 'pfu': 172}
dic3 = {'pab': 1511, 'pbv': 1692, 'peb': 37, 'pfu': 681}
dic4 = {'pab': 182, 'pbv': 508, 'peb': 3, 'pfu': 205}
dic5 = {'pab': 2125, 'pbv': 1133, 'peb': 8, 'pfu': 856}
dic6 = {'pab': 576, 'pbv': 740, 'peb': 0, 'pfu': 108}
dic7 = {'pab': 164, 'pbv': 54, 'peb': 5, 'pfu': 73}
dic8 = {'pab': 1399, 'pbv': 482, 'peb': 20, 'pfu': 324}

title = 'Energiesorten September Release \'17\nAkteursklassen'
y_axis_title = 'Absolute frequenz\n'

bar_group_names = {'pbv' : 'PBV\n(Medien)', 'pab' : 'PAB\n(Wirtschaft)', 'peb' : 'PEB\n(Wissenschaft)', 'pfu' : 'PFU\n(Politik)'} # For languages: {'fr' : 'Französisch', 'de' : 'Deutsch'...}

#------------------------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#--------------------------

# Makes the bar plot

# For one bar group
'''
labels = ['Bildung', 'Fachzeitung', 'Newsdienste', 'Tageszeitung', 'Wochenzeitung']
y = [1.28, 5.34, 15.76, 68.09, 9.50]
x = [1, 3, 5, 7, 9]
barlist = plt.bar(x, y, align='center')
#barlist = plt.bar(range(len(dic)), dic.values(), align='center')
# bar options: color='b', edgecolor =, hatch = patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
'''

# For multiple bar groups
ax = plt.subplot(111)
#ax.bar([x + dist for x in range(len(dic1))], dic1.values(),width=0.3, align='center', color='#b9e1b4') 

# Sets number of bar groups
xlist = []; dist = 0.31; n = 2; xlist.append(n)
for i in range(1, number_of_bar_groups):
	n = n + 3 # Tweak this number to make bar groups closer / farther
	xlist.append(n)
#xlist = [2, 5, 8, 11]

def make_bars(dic, dist, bar_color):
	ax.bar([x + dist for x in xlist], dic.values(),width=0.3, align='center', color=bar_color) 
	
make_bars(dic1, -(dist*4), bar_colors[keyw1])
make_bars(dic2, -(dist*3), bar_colors[keyw2])
make_bars(dic3, -(dist*2), bar_colors[keyw3])
make_bars(dic4, -(dist), bar_colors[keyw4])
make_bars(dic5, 0, bar_colors[keyw5])
make_bars(dic6, dist, bar_colors[keyw6])
make_bars(dic7, dist*2, bar_colors[keyw7])
make_bars(dic8, dist*3, bar_colors[keyw8])

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
fig.savefig(output_file, bbox_inches='tight')
plt.show()

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
