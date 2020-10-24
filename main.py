import argparse
from binascii import hexlify
import logging
import socket
import sys
import threading
import time
import protocols.ssh as essh
import protocols.http as ehttp

def setup_logger(name, log_file, level=logging.INFO):
    """To setup the loggers"""

    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger



if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("--ssh", "-S", help="Setup a SSH Honeypot", action="store_true")
        parser.add_argument("--password", "-P", help="Uses password to authenticate client", action="store_true")
        parser.add_argument("--key", "-K", help="Uses public key to authenticate client", action="store_true")
        parser.add_argument("--http", "-H", help="Setup a HTTP Honeypot", action="store_true")

        args = parser.parse_args()

        if args.ssh:
            print("Running SSH Honeypot...")
            uplist_logger = setup_logger('first_logger', 'uplist.log')
            iplist_logger = setup_logger('second_logger', 'iplist.log')

            HOST_KEY = essh.paramiko.RSAKey(filename='/root/.ssh/id_rsa')
            t0 = time.time()

            paramiko.util.log_to_file("paramiko-log.log", level = "DEBUG")
            if args.password:
                essh.PasswordThreadedServer().listen()

            elif args.key:
                print("Going to use Key.")
                essh.PublicKeyThreadedServer().listen()
            else:
                print("You have entered a wrong argument for the SSH honeypot. Please run with the -h option.")
        elif args.http:
            print("Running HTTP Honeypot...")
            ehttp.run()
        else:
            print("Invalid arguments passed. Try main.py --help for help.")
