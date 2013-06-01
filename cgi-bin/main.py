'''
Ver:		0.4
Author:		Feng Wu
Env:		Run on python 3.3
'''

import sys
import cgi
import pickle

from disam import *

import cgitb
cgitb.enable()

searchTerm = cgi.FieldStorage()['mySearch'].value

showLimit = 25

topicList = disam(searchTerm,showLimit)

with open('res/tlstore.pickle', 'wb') as topicListStoreHandler:
	pickle.dump(topicList, topicListStoreHandler)
	sys.stderr.write('dumped')

print ("Content-Type: text/html\n\n")
print('<div>You have entered: '+ searchTerm +'</div>')
print('<div>New search: <form method="get" action="./cgi-bin/main.py"><input type="text" size="50" name="mySearch"><input type="submit" value="search" /></form></div>')

for topic in topicList:
	print("<hr /><hr /><div><a href=show.py?mySelect="+str(topicList.index(topic))+">\n No."+str(topicList.index(topic)+1)+"  Title:  ",topic.label(),'</a>')
	print("<br><br> Absract: ",str(topic.comment()).encode(encoding='utf-8',errors='ignore'),"</div>")		
