'''
Ver:		0.1
Author:		Feng Wu
Env:		Run on python 3.3
'''

#regex module
import re
import rdflib
import networkx as nx
from SPARQLWrapper import SPARQLWrapper


def buildClassTree(topic):
	classDict = {}
	classTree = nx.Graph()
	typeFilter = re.compile('.*(owl#Thing|schema.org).*')
	
	for objType in topic.objects(rdflib.namespace.RDF.type):
		print (objType.identifier)
		if typeFilter.match(str(objType.identifier)):
			continue
		classDict[objType.qname()] = rdflib.Graph()
		for i in range(20):
			try:
				classDict[objType.qname()].parse(str(objType.identifier),format="application/rdf+xml")
				break
			except:
				print ("connection down... retrying...")
				if i == 20:
					print ("connection lost...")
		print(len(classDict[objType.qname()]))
