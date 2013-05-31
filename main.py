'''
Ver:		0.2
Author:		Feng Wu
Env:		Run on python 3.3
'''

import sys
import json
import networkx as nx
from networkx.readwrite import json_graph
from disam import *
from classRelation import *

topicList = disam(sys.argv[1])

if (len(sys.argv) > 2):
	assert int(sys.argv[2])
	chosenTopic = topicList[int(sys.argv[2])-1]
else:
	chosenTopic = topicList[int(input("Choose the number of the topic: "))-1]
	
print ("You have chosen "+chosenTopic.label()) 

#create a directedd graph instance
classTree = nx.DiGraph()

try:
	buildClassTree(chosenTopic,classTree)
except Exception as ex:
	raise ex

print (classTree.nodes())
print (classTree.edges())

g_json = json_graph.node_link_data(classTree)
json.dump(g_json,open('./res/plot.json','w'))