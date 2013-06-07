'''
Ver:		0.1
Author:		Feng Wu
Env:		Run on python 3.3
'''

import rdflib
import threading
from threadParser import *

class ThreadParser(threading.Thread):
	'''ThreadParser object will parse the URI and return'''

	def __init__(self,URI=None):
		'''initialize the result to be empty, so that if the query process takes too long, the calling party may receive a null object as result'''
		threading.Thread.__init__(self)
		self.inURI = URI
		self.setResult(None)
		
	def run(self):
		'''spawn a thread to parse the URI for the associated RDF graph'''
		self.setResult(rdflib.Graph().parse(self.inURI,format="application/rdf+xml"))
		
	def getGraphResult(self):
		'''getter for result'''
		return self.__result
		
	def getResourceResult(self):
		'''getter for result'''
		return rdflib.resource.Resource(self.__result,self.inURI)
		
	def setResult(self,rdfGraph):
		'''setter for result'''
		self.__result = rdfGraph