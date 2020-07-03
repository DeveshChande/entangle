import argparse
import logging
import paramiko
import socket
import sys
import threading
import time

def setup_logger(name, log_file, level=logging.INFO):
    """To setup the loggers"""

    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger

class PasswordServer(paramiko.ServerInterface):
        def __init__(self):
                self.event = threading.Event()

        def check_channel_request(self, kind, chanid):
                if kind == 'session':
                        return paramiko.OPEN_SUCCEEDED

                return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        def check_auth_password(self, username, password):
                uplist_logger.info(f'{username}\t{password}\n')

                return paramiko.AUTH_FAILED

class PublicKeyServer(paramiko.ServerInterface):
        def __init__(self):
                self.event = threading.Event()

        def check_channel_request(self, kind, chanid):
                if kind == 'session':
                        return paramiko.OPEN_SUCCEEDED

                return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        def check_auth_password(self, username, password):
                uplist_logger.info(f'{username}\t{password}\n')

                return paramiko.AUTH_FAILED

class PasswordThreadedServer():
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


if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("--password", "-P", help="Uses password to authenticate client", action="store_true")
        parser.add_argument("--key", "-K", help="Uses public key to authenticate client", action="store_true")

        args = parser.parse_args()

        uplist_logger = setup_logger('first_logger', 'uplist.log')
        iplist_logger = setup_logger('second_logger', 'iplist.log')

        HOST_KEY = paramiko.RSAKey(filename='/root/.ssh/id_rsa')
        t0 = time.time()

        paramiko.util.log_to_file("paramiko-log.log", level = "DEBUG")
        if args.password:
            PasswordThreadedServer().listen()

        elif args.key:
            print("Going to use Key.")
            PublicKeyThreadedServer().listen()
        else:
            print("You have entered a wrong argument. Please run with the -h option.")
        
