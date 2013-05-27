'''
Ver:		0.1
Author:		Feng Wu
Env:		Run on python 3.3
'''
import sys
from disam import *
from classRelation import *

chosenTopic = disam(sys.argv[1])
print ("You have chosen "+chosenTopic.label()) 
buildClassTree(chosenTopic)