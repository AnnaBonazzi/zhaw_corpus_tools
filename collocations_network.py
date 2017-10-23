#coding=utf8
'''
Anna Bonazzi, 22/08/2017

Script to make a network chart.

Network of the collocates of a chosen word in four different classes. 

Developed from model on https://www.udacity.com/wiki/creating-network-graphs-with-python

Current settings for python 2.7. For python 3, comment out all the ".decode('utf-8')"
'''
#--------------------------
# VARIABLES FOR USER TO CHANGE:

keyword = 'Geothermie'
color_scale = 'red_scale' # Options: black_scale, blue_scale, lightblue_scale, green_scale, lightgreen_scale, orange_scale, brown_scale, red_scale,  pink_scale

txtcolor = '#3c3838' # Choose color codes from http://htmlcolorcodes.com/
txtfont = 'DejaVu Sans'
node_font_size = 13
title_font_size = 16
graph_layout = 'spring' # Options: spring, spectral, random, shell

# Input folder (current setting: folder containing several class-folders. Each class-folder contains collocations files)
folder = "/home/bonz/Documents/Corpus_work/GEothermie2020/collocates/bearbeitet/log-lik_nltk/adj-nouns/" 
#--------------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re
import networkx as nx
import matplotlib.pyplot as plt
#--------------------------

# Creates empty networkx graph
G=nx.Graph()

# Prepares content as a list of tuples (keyword, collocate))
graph = []
class_names = []
os.chdir(folder)

files = glob.glob("*/*" + 'géo' + ".txt")
for file1 in files:
	class_names.append(file1[0:3].upper())
	with open (file1, 'r') as f:
		for line in f:
			line = line.decode('utf-8')
			graph.append((''.join(file1[0:3].upper()), line.strip('\n'))) # line.split('\t')[0]

# Adds edges, collects frequency of each node
freq_dic = {} 
for edge in graph:
	G.add_edge(edge[0], edge[1])
	for word in edge:
		if word in freq_dic:
			freq_dic[word] += 1
		else:
			freq_dic[word] = 1

# Possible network layouts
if graph_layout == 'spring':
	graph_pos=nx.spring_layout(G)
elif graph_layout == 'spectral':
	graph_pos=nx.spectral_layout(G)
elif graph_layout == 'random':
	graph_pos=nx.random_layout(G)
elif graph_layout == 'shell':
	graph_pos=nx.shell_layout(G)


# Prepares scales of node sizes / colors
color_map = []
size_map = []

all_colors = {'red_scale' : {'col1' : 'mistyrose', 'col2' : 'lightcoral', 'col3' : 'red', 'col4' : 'firebrick'}, 'blue_scale' : {'col1' : 'powderblue', 'col2' : 'lightskyblue', 'col3' : 'dodgerblue', 'col4' : 'darkblue'}, 'lightblue_scale' : {'col1' : '#ace2fc', 'col2' : '#4fb0e0', 'col3' : '#0a5578', 'col4' : '#2f6aa4'}, 'green_scale' : {'col1' : '#a8fbc9', 'col2' : '#2ac3a3', 'col3' : '#10866d', 'col4' : '#045443'}, 'lightgreen_scale': {'col1' : '#a5d6a7', 'col2' : '#cddc39', 'col3' : '#689f38', 'col4' : '#1b5e20'}, 'pink_scale' : {'col1' : '#ffebee', 'col2' : '#f8bbd0', 'col3' : '#e57373', 'col4' : '#c2185b'}, 'brown_scale' : {'col1' : '#e9cea7', 'col2' : '#ac9068', 'col3' : '#7d5c2d', 'col4' : '#5f3c0a'}, 'orange_scale' : {'col1' : '#ffd800', 'col2' : '#f5b041', 'col3' : '#d35400', 'col4' : '#a04000'}, 'black_scale' : {'col1' : '#d6dbdf', 'col2' : '#85929e', 'col3' : '#2e4053', 'col4' : '#212121'}}

for word in freq_dic:
	if freq_dic[word] > 5:
		color_map.append(all_colors[color_scale]['col4'])
		size_map.append(1600)
	elif freq_dic[word] >2 and freq_dic[word] <5:
		color_map.append(all_colors[color_scale]['col3'])
		size_map.append(1400)
	elif freq_dic[word] >1 and freq_dic[word] <=2:
		color_map.append(all_colors[color_scale]['col2'])
		size_map.append(1200)
	else: 
		color_map.append(all_colors[color_scale]['col1'])
		size_map.append(800)
	
# Nodes
nx.draw_networkx_nodes(G, graph_pos, node_size=size_map, alpha=0.3, node_color =color_map)

# Edges
width_map = []
for tup in graph:
	width_map.append(int(1 + freq_dic[tup[1]] * 1))
  
nx.draw_networkx_edges(G, graph_pos, width=width_map, alpha=0.3, edge_color="#8e7e8b")

# Node labels
nx.draw_networkx_labels(G, graph_pos,font_size=node_font_size, fontname=txtfont, color=txtcolor)

# Edge labels
'''
labels = None
# or 
#labels = map(chr, range(65, 65+len(graph))) # To name the labels with characters from the character list

if labels is None:
	labels = range(len(graph))

edge_labels = dict(zip(graph, labels))
nx.draw_networkx_edge_labels(G, graph_pos, label_pos=0.3, edge_labels=edge_labels)
'''

# Title
if keyword == 'cantone':
	keyword = 'canton'
plt.title('"' + keyword + '"\n\nKollokatoren (Nomina und Adjektive) nach Klasse', color=txtcolor, fontname = txtfont, fontsize = title_font_size)

# Legend
labels_string = ''
labels_names = {'PAB': ' PAB: Wirtschaft\n', 'PBV' : ' PBV: Medien\n', 'PEB' : ' PEB: Wissenschaft\n', 'PFU' : ' PFU: Politik'}
for cl in labels_names:
	if cl in class_names:
		labels_string = labels_string + labels_names[cl]
labels_list = [labels_string]
# , ' In 3 Klassen', 'In 2 Klassen', 'In 1 Klasse'
leg = plt.legend(loc='best', labels = labels_list, frameon=False)#, facecolor = 'r', edgecolor = 'b' # Don't have to unless I want to change them

# Changes all legend 
for text in leg.get_texts():
	text.set_fontsize(12)
	text.set_fontname(txtfont)
	text.set_color(txtcolor)
	
# Shows graph
plt.show()

#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")
