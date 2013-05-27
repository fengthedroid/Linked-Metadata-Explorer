'''
Ver:    0.3
Author: Feng Wu
Env:	Run on python 3.3
'''
import sys
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON

def disam(keywords):

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
		if index > 10:
			break
		topic = rdflib.resource.Resource(results,subjUri)	
		topicList.append(topic)
		print("No."+str(index)+"  Title:  ",topic.label())
		print("Absract: ",topic.comment())		
		#for objType in topic.objects(rdflib.namespace.RDF.type):
		#	print("\tThe type of the topic is",objType.qname())	
		print("--------------\n")
		index += 1
		
	inputIndex = input("Choose the number of the topic: ")
	return topicList[int(inputIndex)-1]

	
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

	try:
		sys.stderr=''
		results = sparql.query().convert()
		sys.stderr=sys.__stderr__
	except:
		print (traceback.format_exc())
		raise
		
	return results
