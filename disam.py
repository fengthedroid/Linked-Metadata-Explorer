'''
Ver     0.1
Author  Feng Wu
'''

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

rawWord = 'blade runner'
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
queryStr = """
select ?s ?label ?abstract where {
    ?s rdfs:label ?label;
       dbpedia-owl:abstract ?abstract.
    FILTER langMatches( lang(?label), "en" ).
    FILTER langMatches( lang(?abstract), "en" ).
    ?label bif:contains "Blade" .
FILTER (CONTAINS(?label, "Runner"))
}
"""
sparql.setQuery(queryStr)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print (result["s"]["value"],'\n')
    print (result["label"]["value"],'\n')
    print (result["abstract"]["value"],'\n')
