'''
Ver:		0.1
Author:		Feng Wu
Env:		Run on python 3.3
'''
import sys
import networkx as nx
import matplotlib.pyplot as plt
from disam import disam
from classRelation import buildClassTree


topicList = disam(sys.argv[1])

if (len(sys.argv) > 2):
	assert int(sys.argv[2])
	chosenTopic = topicList[int(sys.argv[2])-1]
else:
	chosenTopic = topicList[int(input("Choose the number of the topic: "))-1]
	
print ("You have chosen "+chosenTopic.label()) 

classTree = nx.Graph()

try:
	buildClassTree(chosenTopic,classTree)
except Exception as ex:
	raise ex

print (classTree.nodes())
print (classTree.edges())
nx.draw(classTree)
plt.show()