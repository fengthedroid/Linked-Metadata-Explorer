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
	
	# initialize the tree
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
					queriedResult = thread.getResourceResult()
					classDict[queriedResult.identifier] = queriedResult	
			except:
					print ("connection down...",file=sys.stderr)

			#if connected:
			if queriedResult is not None:
				#add class node to the graph if not yet added
				if not queriedResult.identifier in classTree.nodes():
					classTree.add_node(queriedResult.identifier)
					classTree.add_edge(topic.identifier,queriedResult.identifier)
					classTree.node[queriedResult.identifier]['group']=6

				#test whether the newly added node has edges to other nodes
				#find subclass relations
				for subClass in classDict[queriedResult.identifier].subjects(rdflib.namespace.RDFS.subClassOf):
					if typeFilter.match(str(subClass)):
					#ignore classes from schema.org or w3
						continue
					if subClass.identifier in classTree.nodes():
						classTree.add_edge(subClass.identifier,queriedResult.identifier)
					# print ("----subclass is "+str(subClass.identifier),file=sys.stderr)

				#find superclass relations
				for superClass in classDict[queriedResult.identifier].objects(rdflib.namespace.RDFS.subClassOf):
					if typeFilter.match(str(superClass)):
					#ignore classes from schema.org or w3
						continue
					if superClass.identifier in classTree.nodes():
						classTree.add_edge(queriedResult.identifier,superClass.identifier)
					# print ("----superclass is "+str(superClass.identifier),file=sys.stderr)
					
				#find all instances for the given class
				index = 0
				for instance in classDict[queriedResult.identifier].subjects(rdflib.namespace.RDF.type):
					if index > 5:
						break
					if instance.identifier not in classTree.nodes():
						classTree.add_node(instance.identifier)
						classTree.add_edge(instance.identifier,queriedResult.identifier)
						classTree.node[instance.identifier]['group']=10
						index += 1
	return classTree