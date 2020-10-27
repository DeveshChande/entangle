from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler
import logging

def setup_logger(name, log_file, level=logging.INFO):
    """To setup the loggers"""

    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger

http_get_logger = setup_logger('http-log','http-log.log')

class HTTPHandler(SimpleHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_GET(self):
			print(self.client_address)
			if self.path == '/passwords':
				self.path = '/passwords.txt'
				return SimpleHTTPRequestHandler.do_GET(self)
			elif self.path == '/login':
				self.path = '/login.html'
				return SimpleHTTPRequestHandler.do_GET(self)

			else:
				self.path = '/index.html'
				return SimpleHTTPRequestHandler.do_GET(self)




	def do_POST(self):
		content_length = int(self.headers.get('Content-Length', 0))
		config_string = self.rfile.read(content_length).decode("UTF-8")

		print("Content length: ", content_length)
		print("Config string: [ ", config_string, " ]")
		if self.path == '/home/':
			self.path = '/home.html'
			return SimpleHTTPRequestHandler.do_GET(self)

		print("Content length: ", content_length)
		print("Config string: [ ", config_string, " ]")
		self.path='/login.html'
		return SimpleHTTPRequestHandler.do_GET(self)



def run(server_class=HTTPServer, handler_class=HTTPHandler):
	server_address = ('127.0.0.1', 8080)
	httpd = server_class(server_address, handler_class)
	httpd.serve_forever()
