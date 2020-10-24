import argparse
from binascii import hexlify
import socket
import paramiko
import sys
import threading
import time
import protocols.ssh as essh
import protocols.http as ehttp
import log.elogger as elogger


if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("--ssh", "-S", help="Setup a SSH Honeypot", action="store_true")
        parser.add_argument("--password", "-P", help="Uses password to authenticate client", action="store_true")
        parser.add_argument("--key", "-K", help="Uses public key to authenticate client", action="store_true")
        parser.add_argument("--http", "-H", help="Setup a HTTP Honeypot", action="store_true")

        args = parser.parse_args()

        if args.ssh:
            print("Running SSH Honeypot...")
            uplist_logger = elogger.setup_logger('ssh-honeypot-usernames-passwords', 'ssh-usernames-passwords.log')
            iplist_logger = elogger.setup_logger('ssh-honeypot-ip-address', 'ssh-ip-addresses.log')

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
