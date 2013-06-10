'''
Ver:		0.7
Author:		Feng Wu
Env:		Run on python 3.3
'''

#regex module
import re
import sys
import time
import rdflib
import networkx as nx
from threadParser import *


def buildClassTree(topic):
	'''build a classTree around the given topic
	param topic must be a rdflib Resource class object'''
	
	# initialize the graph
	classTree = nx.DiGraph()
	classDict = {topic.identifier:topic}
	classTree.add_node(topic.identifier)
	classTree.node[topic.identifier]['group']= 2
	
	#initialize a thread pool
	threadPool = set()
	#these ontologies will not be queried
	typeFilter = re.compile('.*(owl#Thing|schema.org|opengis).*')
	
	#iterate through all classes the topic assigned to
	for objType in topic.objects(rdflib.namespace.RDF.type):
		#print (objType.identifier)
		if typeFilter.match(str(objType.identifier)):
		#discard classes belongs to w3 and schema.org
			continue
			
		#using thread to query in case of hanging by rdflib
		queryThread = ThreadParser(objType.identifier)
		queryThread.start()
		threadPool.add(queryThread)

	# wait 7 seconds for the query to complete
	time.sleep(7)
	
	#join all threads back
	for thread in threadPool:
		queriedResult = None

		if thread is not threading.currentThread():
			try:
				thread.join()
				if thread.isAlive():
					raise
				else:
					# queriedResult = thread.getResourceResult()
					# classDict[queriedResult.identifier] = queriedResult
					classDict[thread.inURI] = thread.getGraphResult()
			except:
				raise
				# print ("connection down...",file=sys.stderr)

			#if connected:
			# if queriedResult is not None:
			if len(classDict[thread.inURI]) != 0:
				#add class node to the graph if not yet added
				if not thread.inURI in classTree.nodes():
					classTree.add_node(thread.inURI)
					classTree.add_edge(topic.identifier,thread.inURI)
					classTree.node[thread.inURI]['group']=6
				#test whether the newly added node has edges to other nodes
				#find subclass relations
				for subClass in classDict[thread.inURI].subjects(predicate=rdflib.namespace.RDFS.subClassOf):
					if typeFilter.match(str(subClass)):
					#ignore classes from schema.org or w3
						continue
						
					#dbpedia change:
					if subClass in classTree.nodes():
						classTree.add_edge(subClass,thread.inURI)
						
					# if subClass.identifier in classTree.nodes():
						# classTree.add_edge(subClass.identifier,queriedResult.identifier)
					# print ("----subclass is "+str(subClass),file=sys.stderr)

				#find superclass relations
				for superClass in classDict[thread.inURI].objects(predicate=rdflib.namespace.RDFS.subClassOf):
					if typeFilter.match(str(superClass)):
					#ignore classes from schema.org or w3
						continue
					
					#dbpedia change:
					if superClass in classTree.nodes():
						classTree.add_edge(thread.inURI,superClass)
					
					# if superClass.identifier in classTree.nodes():
						# classTree.add_edge(queriedResult.identifier,superClass.identifier)
					# print ("----superclass is "+str(superClass),file=sys.stderr)
					
				#find all instances for the given class
				index = 0
				for instance in classDict[thread.inURI].subjects(predicate=rdflib.namespace.RDF.type):
					if index > 5:
						break
						
					# print ("----instance "+str(instance),file=sys.stderr)
					#dbpedia change
					if instance not in classTree.nodes():
						classTree.add_node(instance)
						classTree.add_edge(instance,thread.inURI)
						classTree.node[instance]['group']=10
						index += 1
					# if instance.identifier not in classTree.nodes():
						# classTree.add_node(instance.identifier)
						# classTree.add_edge(instance.identifier,queriedResult.identifier)
						# classTree.node[instance.identifier]['group']=10
						# index += 1
	return classTree