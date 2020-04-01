# Katherine Jacobs
# V00783178
# Last Modified: Mar 03 2020

# Resources I used for this assignment:
# https://wiki.python.org/moin/UdpCommunication
# https://pythontic.com/modules/socket/udp-client-server-example


# We will need the following module to generate randomized lost packets
import random
from socket import *
import sys

# Create a UDP socket 
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
host = sys.argv[1]
port = int(sys.argv[2])
serverSocket.bind((host, port))
print("UDP Server is up and running.")

while True:
	# Receive the client packet along with the address it is coming from 
	message = serverSocket.recvfrom(4096) #buffer size is 4096 bytes
	address = message[1]
	msg_split = message[0].decode('ascii').split()

	print(f"Received packet {msg_split[1]}")

	reply = ''
	# Generate random number in the range of 1 to 10 and if rand is less is than 4, we consider the packet lost and tell the client to retransmit
	rand = random.randint(1, 11)    
	if rand < 4:
		reply = 'Packet Dropped' # insert an error message here?
		print("  Packet was dropped...")
	else:
		reply = message[0].decode('ascii').upper()
		print("  Responding...")
		if msg_split[1] == '100':
			serverSocket.sendto(reply.encode(), address)
			print("  Exiting...")
			sys.exit()
	
	# Capitalize the message from the client and send the capilized version to the client
	serverSocket.sendto(reply.encode(), address)
