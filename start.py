#!/usr/bin/env Python

from http.server import HTTPServer, CGIHTTPRequestHandler

#port for http request
port = 8000
httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
print("Starting simple_httpd on port: " + str(httpd.server_port))
#start CGI server
httpd.serve_forever()