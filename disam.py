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
	results = sparql.query().convert()
except:
	print (traceback.format_exc())
finally:
	pass
	

for subjLabel in results.objects(None, rdflib.namespace.RDFS.label):
	
	subjUri = results.value(predicate=rdflib.namespace.RDFS.label,object=subjLabel)
	subjComment = results.value(subject = subjUri, predicate=rdflib.namespace.RDFS.comment)
	
	pprint.pprint(subjLabel)
	pprint.pprint(subjComment)
	for objType in results.objects(subjUri,rdflib.namespace.RDF.type):
		print("\tThe type of the topic is",objType)
	
	
print("graph has %s statements." % len(results))


