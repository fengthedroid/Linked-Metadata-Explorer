

'''
Ver:		0.4
Author:		Feng Wu
Env:		Run on python 3.3
'''

import sys
import cgi
import pickle

from termHandler import *

#this package will provide better debugging functionalities for cgi script
import cgitb
cgitb.enable()

#read the search term from http GET
searchTerm = cgi.FieldStorage()['mySearch'].value

print(searchTerm,file=sys.stderr)

#display 25 results for the given keyword
showLimit = 25

#query and obtain a list of matched topics
topicList = disam(searchTerm,showLimit)

#dump the query result as pickle file which is to be used by the visual module
with open('res/tlstore.pickle', 'wb') as topicListStoreHandler:
	pickle.dump(topicList, topicListStoreHandler)
	sys.stderr.write('dumped')

#display the list of topics in html
print ("Content-Type: text/html\n\n")
print('<div>You have entered: '+ searchTerm +'</div>')
print('<div>New search: <form method="get" action="main.py"><input type="text" size="50" name="mySearch"><input type="submit" value="search" /></form></div>')
for topic in topicList:
	print("<hr /><hr /><div><a href=show.py?mySelect="+str(topicList.index(topic))+">\n No."+str(topicList.index(topic)+1)+"  Title:  ",topic.label(),'</a>')
	print("<br><br> Abstract: ",str(topic.comment()).encode(encoding='utf-8',errors='ignore'),"</div>")		
