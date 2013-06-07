'''
Ver:		0.1
Author:		Feng Wu
Env:		Run on python 3.3
'''

import rdflib
from threadParser import *

#test case 1
def test1():

	tp = ThreadParser(rdflib.URIRef("http://umbel.org/umbel/rc/Movie_CW"))
	tp.start()
	tp.join(3)
	print (tp.getGraphResult())
	print (tp.getResourceResult())
	print (tp.getResourceResult().identifier)
	if tp.isAlive():
		raise
	
#test	
test1()