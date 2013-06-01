'''
Ver:		0.4
Author:		Feng Wu
Env:		Run on python 3.3
'''

#regex module
import re
import time
import rdflib

import threading

from SPARQLWrapper import SPARQLWrapper


def buildClassTree(topic,classTree):

	classDict = {topic.identifier:topic}
	classTree.add_node(topic.identifier)
	
	#the two ontology will not be queried
	typeFilter = re.compile('.*(owl#Thing|schema.org).*')
	#iterate through all classes the topic assigned to
	for objType in topic.objects(rdflib.namespace.RDF.type):
		#print (objType.identifier)
		if typeFilter.match(str(objType.identifier)):
		#discard classes belongs to w3 and schema.org
			continue
			
		connFlag = 0
		#for each attempt, print out connection status if failed
		for i in range(5):
			try:
				
				print ("connecting ",objType.identifier)
				
				#using thread to query in case of hanging by rdflib
				qT = QueryThread(objType)
				qT.start()
				qT.join(3)
				if qT.isAlive():
					raise
				else:
					classDict[objType.identifier] = qT.result
				"""
				classDict[objType.identifier]=rdflib.resource.Resource(\
				rdflib.Graph().parse(str(objType.identifier),format="application/rdf+xml"),\
				rdflib.URIRef(objType.identifier))
				"""
				"""
				queryQueue = multiprocessing.Queue()
				queryProc = multiprocessing.Process(target=globals().ontologyQuery, args=(objType,queryQueue,))
				queryProc.start()
				classDict[objType.identifier]=queryQueue.get()
				queryProc.join(10)
				if queryProc.is_alive:
					print ("proc timeout...")
					# Terminate
					queryQueue.close()
					queryProc.terminate()
					queryProc.join()
					raise
				"""
				
				connFlag = 1
				break
			except:
				print ("connection down... retrying...")
				time.sleep(2)
				if i == 4:
					print ("unable to connect, discard this class...")							

		#if connected:
		if connFlag == 1:
			#add class node to the graph if not yet added
			if not objType.identifier in classTree.nodes():
				classTree.add_node(objType.identifier)
				classTree.add_edge(topic.identifier,objType.identifier)
				
			#test whether the newly added node has edges to other nodes
			
			#find subclass relations
			for subClass in classDict[objType.identifier].subjects(rdflib.namespace.RDFS.subClassOf):
				if typeFilter.match(str(subClass)):
				#ignore classes from schema.org or w3
					continue
				if subClass.identifier in classTree.nodes():
					classTree.add_edge(subClass.identifier,objType.identifier)
				print ("subclass is "+str(subClass.identifier))
				
			#find superclass relations
			for superClass in classDict[objType.identifier].objects(rdflib.namespace.RDFS.subClassOf):
				if typeFilter.match(str(superClass)):
				#ignore classes from schema.org or w3
					continue
				if superClass.identifier in classTree.nodes():
					classTree.add_edge(objType.identifier,superClass.identifier)
				print ("superclass is "+str(superClass.identifier))
			
	return classTree

	
# need multi-thread to kill hanging query issued by rdflib


class QueryThread(threading.Thread):
	def __init__(self,typeObj):
		threading.Thread.__init__(self)
		self.typeO = typeObj
		self.result = ''
	def run(self):
		self.result = rdflib.resource.Resource(rdflib.Graph().parse(str(self.typeO.identifier),format="application/rdf+xml"),rdflib.URIRef(self.typeO.identifier))


"""	
def ontologyQuery(objType,queue):
	print ("separate proc ", objType)
	queue.put(rdflib.resource.Resource(rdflib.Graph().parse(str(objType.identifier),format="application/rdf+xml"),rdflib.URIRef(objType.identifier)))
"""