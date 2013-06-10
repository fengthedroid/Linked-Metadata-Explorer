'''
Ver:    0.4
Author: Feng Wu
Env:	Run on python 3.3
'''

import sys
import rdflib
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
		#wrap every subject into a rdflib resource class object
		topic = rdflib.resource.Resource(results,subjUri)	
		topicList.append(topic)
		index += 1
	
	return topicList
	
def __queryKeyword(keywords):
	
	#Split words into a list
	rawList = keywords.split(' ')

	#Using regular expression to build query to enable case insensitive
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

	#DBpedia may not be responsive
	try:
		results = sparql.query().convert()
	except:
		print ('error: cannot query.')
	return results
