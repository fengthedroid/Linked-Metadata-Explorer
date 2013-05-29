'''
Ver:		0.1
Author:		Feng Wu
Env:		Run on python 3.3
'''
import sys
from disam import disam
from classRelation import buildClassTree


if (len(sys.argv) > 2):
	assert int(sys.argv[2])
	chosenTopic = disam(sys.argv[1],sys.argv[2])
else:
    chosenTopic = disam(sys.argv[1],0)
	
print ("You have chosen "+chosenTopic.label()) 
buildClassTree(chosenTopic)
