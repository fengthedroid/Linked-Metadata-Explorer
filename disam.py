'''
Ver     0.1
Author  Feng Wu
'''

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
} LIMIT 10
"""
print (queryStr)

sparql.setQuery(queryStr)

sparql.setReturnFormat(JSON)
try:
	results = sparql.query().convert()
except:
	print (traceback.format_exc())
	
#print (results)
'''
file = open('temp.tmp', 'w')
file.write(str(results))
file.close


print ('\n\n')
print ('\n\n')
print ('\n\n')
g = rdflib.Graph()
result = g.parse(results,format='n3')

print("graph has %s statements." % len(g))
'''

for result in results["results"]["bindings"]:
    print (result["subj"]["value"],'\n')
    print (result["label"]["value"],'\n')
    print (result["comment"]["value"][:300],'\n','...')
