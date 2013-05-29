'''
Ver:		0.1
Author:		Feng Wu
Env:		Run on python 3.3
'''

import rdflib
import networkx as nx
from SPARQLWrapper import SPARQLWrapper


def buildClassTree(topic):
	classDict = {}
	classTree = nx.Graph()
	
	for objType in topic.objects(rdflib.namespace.RDF.type):
		print (objType.identifier)

		typeUri=__UriParser(str(objType.identifier))
		classDict[objType.qname()] = rdflib.Graph()
		classDict[objType.qname()].parse(typeUri)
		print(len(classDict[objType.qname()]))

		
def __UriParser(identifier):
	assert type(identifier) is str
	if 'yago' in identifier:
		pass
	elif 'dbpedia' in identifier:
		pass
	elif 'umbel' in identifier:
		parsedStr = identifier
	return parsedStr