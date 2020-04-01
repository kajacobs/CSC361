# Katherine Jacobs
# V00783178
# Last Modified: January 25th 2020

# Resources Used for this Assignment:
# https://www.binarytides.com/python-socket-programming-tutorial/
# https://docs.python.org/2/library/socket.html

from socket import *
import sys

host = sys.argv[1]
port = int(sys.argv[2])

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((host, port))
clientSocket.sendall(sys.argv[3])
data = clientSocket.recv(4096)
print(data)
clientSocket.close()
