'''
Ver     0.2
Author  Feng Wu
'''

import pprint
import sys
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON

#Split words into a list
rawList = sys.argv[1].split(' ')

filterString = ''
for i in range(1,len(rawList)):
	filterString+='FILTER regex(?label, "['+rawList[i][0].upper()+\
		rawList[i][0].lower()+']'+rawList[i][1:]+'").\n'
	
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

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
print (queryStr)

sparql.setQuery(queryStr)

sparql.setReturnFormat('rdf')

try:
	sys.stderr=''
	results = sparql.query().convert()
	sys.stderr=sys.__stderr__
except:
	print (traceback.format_exc())
finally:
	pass
	

for subjUri in results.subjects(predicate=rdflib.namespace.RDFS.label):
	
	#print (subjUri)
	topic = rdflib.resource.Resource(results,subjUri)

	pprint.pprint(topic.label())
	#pprint.pprint(topic.comment())
	for objType in results.objects(subject=subjUri,predicate=rdflib.namespace.RDF.type):
		print("\tThe type of the topic is",objType)
	
	
print("graph has %s statements." % len(results))
