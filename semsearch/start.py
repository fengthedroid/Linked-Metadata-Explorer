'''
Ver:		0.2
Author:		Feng Wu
Env:		Run on python 3.3
'''

import sys
from http.server import HTTPServer, CGIHTTPRequestHandler

#default port is 8080
port = 8080
if len(sys.argv)>1:
	port = int(sys.argv[1])
	
httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
print("Starting simple_httpd on port: " + str(httpd.server_port))
#start CGI server
httpd.serve_forever()