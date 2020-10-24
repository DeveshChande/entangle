from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler

class HTTPHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		print(self.client_address)

		if self.path == 'passwords.txt':
			self.path='passwords.txt'
			return SimpleHTTPRequestHandler.do_GET(self)
		else:
			self.path=='/'
			return SimpleHTTPRequestHandler.do_GET(self)


	def do_POST(self):
		pass



def run(server_class=HTTPServer, handler_class=HTTPHandler):
	server_address = ('127.0.0.1', 8080)
	httpd = server_class(server_address, handler_class)
	httpd.serve_forever()
