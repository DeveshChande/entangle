import logging
import socket
import paramiko
from paramiko.py3compat import b, u, decodebytes
import sys
import time
import threading

def setup_logger(name, log_file, level=logging.INFO):
    """To setup the loggers"""

    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger

t0 = time.time()
HOST_KEY = paramiko.RSAKey(filename='/root/.ssh/id_rsa')
paramiko.util.log_to_file("paramiko-log.log", level = "DEBUG")
uplist_logger = setup_logger('ssh-honeypot-usernames-passwords', 'ssh-usernames-passwords.log')
iplist_logger = setup_logger('ssh-honeypot-ip-address', 'ssh-ip-addresses.log')

class PasswordServer(paramiko.ServerInterface):
        def __init__(self):
                self.event = threading.Event()

        def check_channel_request(self, kind, chanid):
                if kind == 'session':
                        return paramiko.OPEN_SUCCEEDED

                return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        def check_auth_password(self, username, password):
                uplist_logger.info(f'PasswordAuth:{username}\t{password}\n')

                return paramiko.AUTH_FAILED

class PublicKeyServer(paramiko.ServerInterface):
        def __init__(self):
                self.event = threading.Event()

        def get_allowed_auths(self, username):
                return "publickey, password"

        def check_channel_request(self, kind, chanid):
                if kind == 'session':
                        return paramiko.OPEN_SUCCEEDED

                return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        def check_auth_publickey(self, username, key):

                log_key = u(hexlify(key.get_fingerprint()))
                uplist_logger.info(f'PublicKeyAuth:{username}\t{log_key}\n')
                return paramiko.AUTH_FAILED

class PasswordThreadedServer():
        def __init__(self):
                self.host = 'localhost'
                self.port = 22000
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.sock.bind((self.host, self.port))

        def listen(self):
                self.sock.listen(5)
                while True:
                    clientsocket, address = self.sock.accept()
                    t1 = time.time()
                    if (t1-t0) > 30:
                        sys.exit()
                    threading.Thread(target = self.listenToClient,args = (clientsocket,address)).start()

                    iplist_logger.info(f'{str(address[0])}\t{str(address[1])}\n')

        def listenToClient(self, clientsocket, address):
                size = 1024
                while True:
                        ssh_connection = paramiko.Transport(clientsocket)
                        ssh_connection.add_server_key(HOST_KEY)
                        server = PasswordServer()
                        try:
                            ssh_connection.start_server(server=server)
                        except:
                            print('Failed to start ssh connection over TCP.')

                        try:
                                data_channel = ssh_connection.accept()
                                data_channel.close()
                        except:
                                print('Channel exception.')

                        ssh_connection.close()
                        clientsocket.close()
                        sys.exit()
                        return False

class PublicKeyThreadedServer():

        def __init__(self):
                self.host = '192.168.56.104'
                self.port = 22
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.sock.bind((self.host, self.port))



        def listen(self):
                self.sock.listen(5)
                while True:
                    clientsocket, address = self.sock.accept()
                    t1 = time.time()
                    if (t1-t0) > 30:
                        sys.exit()
                    threading.Thread(target = self.listenToClient,args = (clientsocket,address)).start()

                    iplist_logger.info(f'{str(address[0])}\t{str(address[1])}\n')

        def listenToClient(self, clientsocket, address):
                size = 1024
                while True:
                        ssh_connection = paramiko.Transport(clientsocket)
                        ssh_connection.add_server_key(HOST_KEY)
                        server = PublicKeyServer()
                        print(address)
                        try:
                            ssh_connection.start_server(server=server)
                        except:
                            print('Failed to start ssh connection over TCP.')

                        try:
                                data_channel = ssh_connection.accept()
                                data_channel.close()
                        except:
                                print('Channel exception.')

                        ssh_connection.close()
                        clientsocket.close()
                        sys.exit()
                        return False
