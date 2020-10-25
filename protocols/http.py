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
	def do_GET(self):
		http_get_logger.info(f'{self.client_address}')
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
