'''
Ver     0.1
Author  Feng Wu
'''

import sys
from SPARQLWrapper import SPARQLWrapper, JSON


#Split words into a list
rawList = sys.argv[1].split(' ')

filterString = ''
for i in range(1,len(rawList)):
	filterString+='FILTER regex(?label, "['+rawList[i][0].upper()+\
		rawList[i][0].lower()+']'+rawList[i][1:]+'").\n'
	
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
queryStr = """
select ?s ?label ?abstract where {
    ?s rdfs:label ?label;
       dbpedia-owl:abstract ?abstract.
    FILTER langMatches( lang(?label), "en" ).
    FILTER langMatches( lang(?abstract), "en" ).
    ?label bif:contains '"""+rawList[0].title()+"""'.
	"""+filterString+"""
} LIMIT 10
"""
print (queryStr)
sparql.setQuery(queryStr)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print (result["s"]["value"],'\n')
    print (result["label"]["value"],'\n')
    print (result["abstract"]["value"][:800],'\n')
