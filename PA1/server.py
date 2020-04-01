# Katherine Jacobs
# V00783178
# Last Modified: January 25th 2020

# Resources Used for this Assignment:
# https://www.binarytides.com/python-socket-programming-tutorial/

#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket
#bind and listen
host = sys.argv[1]
port = int(sys.argv[2])
print(host)
print(port)
serverSocket.bind((host, port))
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')
    #connecting to the client and accepting connection
    connectionSocket, addr =  serverSocket.accept()

    try:
        #HTTP request
        message = connectionSocket.recv(4096)
        filename = message.split()[0]
        f = open(message)
        outputdata = f.read()
        #Send one HTTP header line into socket
        #Send the content of the requested file to the client
        response = "HTTP/1.1 200 OK\n\n" + outputdata
        connectionSocket.send(response.encode())

        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        response = "404 Not Found"
        connectionSocket.send(response.encode())

        #Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
