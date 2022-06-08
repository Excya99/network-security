import socketserver
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class ClientHandler(socketserver.BaseRequestHandler):
	def handle(self):
		encrypted_key = self.request.recv(5000).strip()
		print("Received: " + encrypted_key.hex())
		print("\n")
		#Load private key from memory
		with open("directory of private key", "rb") as key_file:
			private_key = serialization.load_pem_private_key(key_file.read(), password=None)
			decrypted_key = private_key.decrypt(encrypted_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
			self.request.sendall(decrypted_key)
			print("SENT: " + decrypted_key.hex())

if __name__ == "__main__":
	HOST, PORT = "", 8080 #HOST not required to be set for server, PORT needs to match with clients

tcpServer = socketserver.TCPServer((HOST, PORT), ClientHandler)
try:
	tcpServer.serve_forever()
except:
	print("There was an error")