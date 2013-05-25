import sys
from SPARQLWrapper import SPARQLWrapper, JSON

keyWord = 'Andy_Roddick'
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
queryStr = """

    SELECT ?abs
    WHERE { 
      <http://dbpedia.org/resource/"""+keyWord+"""> dbpedia-owl:abstract ?abs.
	  FILTER (langMatches(lang(?abs),"en"))
    }
"""
sparql.setQuery(queryStr)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print (results["results"]["bindings"][0]["abs"]["value"])
