'''
Ver:		0.1
Author:		Feng Wu
Env:		Run on python 3.3
'''

#regex module
import re
import rdflib
import networkx as nx
#from pprint import pprint
from SPARQLWrapper import SPARQLWrapper


def buildClassTree(topic):
	classDict = {}
	classTree = nx.Graph()
	
	
	typeFilter = re.compile('.*(owl#Thing|schema.org).*')
	
	for objType in topic.objects(rdflib.namespace.RDF.type):
		#print (objType.identifier)
		if typeFilter.match(str(objType.identifier)):
			continue
			
		try:	
			for i in range(20):
				try:
					classDict[objType.qname()]=rdflib.resource.Resource(\
					rdflib.Graph().parse(str(objType.identifier),format="application/rdf+xml"),\
					rdflib.URIRef(objType.identifier))
					#
					#classDict[objType.qname()]=rdflib.Graph().parse(str(objType.identifier),format="application/rdf+xml")
					#print (len(classDict[objType.identifier]))
					break
				except:
					print ("connection down... retrying...")
					if i == 19:
						raise Exception("connection lost...")
						
			lang = re.compile('.*en.*')
			for label in classDict[objType.qname()].objects(rdflib.namespace.RDFS.label):
				
				if str(label._language)=='en':
				# cannot use the getter for rdflib.term.literal
					print ("belongs to "+ label._value)
					#break
			
			for subClass in classDict[objType.qname()].subjects(rdflib.namespace.RDFS.subClassOf):
				if typeFilter.match(str(subClass)):
					continue
				print ("subclass is "+str(subClass.identifier))
			
		except Exception as ex:
			#print (ex)
			raise ex