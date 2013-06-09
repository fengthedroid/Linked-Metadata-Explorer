'''
Ver:		0.1
Author:		Feng Wu
Env:		Run on python 3.3
'''

import rdflib
import time
from tkinter import *
from threadParser import *

class Application(Frame):

	def createWidgets(self):
	
		self.parent.title("URI parser")
		self.pack(fill=BOTH, expand=1)

		self.rowconfigure(0, pad=7)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, pad=7)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, pad=7)
		
		# text label
		label=Label(self,text="Please enter an URI")
		label.grid(row=0)
		
		# result
		resultStr = StringVar()
		resultStr.set("The URI contains:")
		result=Label(self,textvariable=resultStr)
		result.grid(row=2,padx=5,pady=5)
		
		# input
		input = Entry(self,width=70)
		input.grid(row=1,column=0)
		
		#submit
		submit = Button(self)
		submit["text"] = "Submit"
		submit["command"] = lambda:self.__buttonCommand(resultStr,input)
		submit.grid(row=1,column=1)

	def __buttonCommand(self,strVar,input):
		tp = ThreadParser(rdflib.URIRef(input.get()))
		tp.start()
		tp.join(3)
		newStr = "The URI contains: " + str(len(tp.getGraphResult())) + " triples"
		strVar.set(newStr)

		
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.parent = parent
		self.createWidgets()

root = Tk()
root.geometry("500x150+300+300")
app = Application(parent=root)
app.mainloop()
root.destroy()

# test("http://umbel.org/umbel/rc/Movie_CW")