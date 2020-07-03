from collections import Counter
import time

t0 = time.time()
list_of_remote_versions = []
list_of_kex_agreed = []
list_of_host_key_agreed = []
list_of_cipher_agreed = []
list_of_MAC_agreed = []
list_of_compression_agreed = []

with open('paramiko-log.log', "r") as file:
	for line in file:
		if "paramiko.transport: Remote version/idstring" in line:
			list_of_remote_versions.append(line[81:])
		elif "paramiko.transport: Kex agreed" in line:
			list_of_kex_agreed.append(line[68:])
		elif "paramiko.transport: HostKey agreed" in line:
			list_of_host_key_agreed.append(line[72:])
		elif "paramiko.transport: Cipher agreed" in line:
			list_of_cipher_agreed.append(line[71:])
		elif "paramiko.transport: MAC agreed" in line:
			list_of_MAC_agreed.append(line[68:])
		elif "paramiko.transport: Compression agreed" in line:
			list_of_compression_agreed.append(line[76:])
		else:
			pass

with open('sshlogs/remote-versions.log', "a") as f0:
	for i in list_of_remote_versions:
		f0.write(i + '\n')
	f0.close()

with open('sshlogs/kex_agreed.log', "a") as f1:
	for i in list_of_kex_agreed:
		f1.write(i + '\n')
	f1.close()

with open('sshlogs/host_key_agreed.log', "a") as f2:
	for i in list_of_host_key_agreed:
		f2.write(i + '\n')
	f2.close()

with open('sshlogs/cipher_agreed.log', "a") as f3:
	for i in list_of_cipher_agreed:
		f3.write(i + '\n')
	f3.close()

with open('sshlogs/MAC_agreed.log', "a") as f4:
	for i in list_of_MAC_agreed:
		f4.write(i + '\n')
	f4.close()

with open('sshlogs/compression_agreed.log', "a") as f5:
	for i in list_of_compression_agreed:
		f5.write(i + '\n')
	f5.close()

t1 = time.time()
print(t1-t0)
