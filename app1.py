#!/usr/bin/python

try:
	from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
except:
	from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
try:
	from urlparse import urlparse
	from urlparse import urlparse, parse_qs
except:
	from urllib.parse import urlparse, parse_qs

import os
port = int(os.environ.get("PORT", 5000))	
PORT_NUMBER = port


#de leo borrar
import citas

citas=citas.citas
f=open('citas.py','w')
f.write('citas='+str(citas))
f.close()
####

class myHandler(BaseHTTPRequestHandler):
	global citas
	#Handler for the GET requests
	def do_GET(self):
		self.path=self.path.split('?')
		try:
			arg=self.path[1].replace('%20',' ')
			print(arg)
			arg=arg.split(';')
			citas[arg[0]][arg[1]][arg[2]].append(arg[3])
			print(citas[arg[0]])
			f=open('citas.py','w')
			f.write('citas='+str(citas))
			f.close()
		except:
			pass
		self.path=self.path[0]
		
		
			
		if self.path=="/":  #127.0.0.1:5000/
			self.path="/index.html" #127.0.0.1:5000/index.html
		print()
		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
				f = open(curdir + sep + self.path)
				data=f.read()
				f.close()
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				
				mimetype='application/javascript'
				
				data='citas='+str(citas)
				f=open('citas.py','r')
				data=f.read()
				f.close()
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				#f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				#data=f.read()
				
				try:
					self.wfile.write(data)
				except:
					self.wfile.write(bytes(data, 'UTF-8'))
				
			return


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
