'''
Ver:		0.3
Author:		Feng Wu
Env:		Run on python 3.3
'''

import sys
import rdflib
import threading
from SPARQLWrapper import SPARQLWrapper

class ThreadParser(threading.Thread):
	'''ThreadParser object will parse the URI and return'''

	def __init__(self,URI=None):
		'''initialize the result to be empty, so that if the query process takes too long, the calling party may receive a null object as result'''
		threading.Thread.__init__(self)
		self.inURI = URI
		self.__result = rdflib.Graph()
		
	def run(self):
		'''spawn a thread to parse the URI for the associated RDF graph'''
		self.setResult(rdflib.Graph().parse(self.inURI,format="application/rdf+xml"))
		
	def getGraphResult(self):
		#the following change is made due to DBpedia domain change
		# for sub, pre, obj in self.__result:
			# print (sub,obj,file=sys.stderr)
			# sub=str(sub).replace("local:/","http://dbpedia.org/")
			# pre=str(pre).replace("local:/","http://dbpedia.org/")
			# obj=str(obj).replace("local:/","http://dbpedia.org/")
		# '''getter for result'''
		return self.__result
		
	def getResourceResult(self):
		# '''wrap the result as rdflib Resource class object'''
		# the following change is made due to DBpedia domain change
		# self.inURI = self.inURI.replace("http://dbpedia.org/","local:/")
		# print (self.inURI,'---',file=sys.stderr)
		# for sub, pre, obj in self.__result:
			# sub=str(sub).replace("local:/","http://dbpedia.org/")
			# pre=str(pre).replace("local:/","http://dbpedia.org/")
			# obj=str(obj).replace("local:/","http://dbpedia.org/")
			# if str(sub) == str(self.inURI):
				# print (obj,file=sys.stderr)
		#wrap
		# print (self.__result.label(self.inURI),file=sys.stderr)
		self.__resultRes = rdflib.resource.Resource(self.__result,self.inURI)
		return self.__resultRes
		
	def setResult(self,rdfGraph):
		'''setter for result'''
		self.__result = rdfGraph
		#for debugging
		# if rdfGraph is not None:
			# print ("___!!!---graph lenght is ",len(rdfGraph),' -- ',self.inURI,file=sys.stderr)
		# else:
			# print ("___!!!--Not properly queried -- ",self.inURI,file=sys.stderr)
			