'''
Ver:		0.2
Author:		Feng Wu
Env:		Run on python 3.3
'''
import cgi
import webbrowser # open finished plot
import json
import pickle
import networkx as nx
from networkx.readwrite import json_graph
from classRelation import *

import cgitb
cgitb.enable()

with open('res/tlstore.pickle', 'rb') as topicListStoreHandler:
    topicList=pickle.load(topicListStoreHandler)
	
chosenTopic = topicList[int(cgi.FieldStorage()['mySelect'].value)]

#create a directedd graph instance
classTree = nx.DiGraph()

try:
	buildClassTree(chosenTopic,classTree)
except Exception as ex:
	raise ex

g_json = json_graph.node_link_data(classTree)
json.dump(g_json,open('res/plot.json','w'))

print ("Content-Type: text/html\n\n")
print ("""
<html>
  <head>
    <title>Class output</title>

	<script language=javascript>
		function redirect(){
			window.location = "../plot.html";
		}
	</script>

	<body onload="redirect()">

	</body>
</html>
""")