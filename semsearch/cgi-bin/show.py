'''
Ver:		0.3
Author:		Feng Wu
Env:		Run on python 3.3
'''
import cgi
import json
import pickle
from networkx.readwrite import json_graph
from treeBuilder import *

#this package will provide better debugging functionalities for cgi script
import cgitb
cgitb.enable()

#read the topic list from the pickle file
with open('res/tlstore.pickle', 'rb') as topicListStoreHandler:
    topicList=pickle.load(topicListStoreHandler)
	
#find the topic the user is clicked on
chosenTopic = topicList[int(cgi.FieldStorage()['mySelect'].value)]

#create a directed graph
try:
	classTree=buildClassTree(chosenTopic)
except Exception as ex:
	raise ex

#write the networkx graph object into JSON format
g_json = json_graph.node_link_data(classTree)
#dump the JSON file on disk for the javascript
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