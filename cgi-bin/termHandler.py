'''
Ver:    0.4
Author: Feng Wu
Env:	Run on python 3.3
'''

import sys
import rdflib
import time
from SPARQLWrapper import SPARQLWrapper

#param: command line input
#return a list of related topics
def disam(keywords,resultLimit):

	#build the query string
	queryStr = __queryKeyword(keywords)
	#print (queryStr)
	
	#execute the query
	results = __execQuery(queryStr)	
	#print("graph has %s statements." % len(results))
	
	#iterate through the results and put each topic into a list
	topicList = []
	index = 1
	for subjUri in results.subjects(predicate=rdflib.namespace.RDFS.label):	
		if index > resultLimit:
			break
		topic = rdflib.resource.Resource(results,subjUri)	
		topicList.append(topic)
		#print("No."+str(index)+"  Title:  ",topic.label())
		#print("Absract: ",str(topic.comment()).encode(encoding='utf-8',errors='ignore'))		
		#for objType in topic.objects(rdflib.namespace.RDF.type):
		#	print("\tThe type of the topic is",objType.qname())	
		#print("--------------\n")
		index += 1
	
	return topicList
	
def __queryKeyword(keywords):
	
	#Split words into a list
	rawList = keywords.split(' ')

	#
	filterString = ''
	for i in range(1,len(rawList)):
		filterString+='FILTER regex(?label, "['+rawList[i][0].upper()+\
			rawList[i][0].lower()+']'+rawList[i][1:]+'").\n'
		
	queryStr = """
	construct {
	?subj 	rdfs:label 	?label;
			rdf:type  	?type;
			rdfs:comment	?comment.
	}
	where {
		?subj 	rdfs:label 	?label;
				rdf:type	?type;
				rdfs:comment 	?comment.
		FILTER langMatches( lang(?label), "en" ).
		FILTER langMatches( lang(?comment), "en" ).
		?label bif:contains '"""+rawList[0].title()+"""'.
		"""+filterString+"""
	}
	"""
	return queryStr

def __execQuery(queryStr):

	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(queryStr)
	sparql.setReturnFormat('rdf')

	for i in range(20):
		try:
			results = sparql.query().convert()
			break
		except:
			print ('error: cannot query.')
			time.sleep(5)
		
	return results
