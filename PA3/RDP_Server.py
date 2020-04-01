# Katherine Jacobs
# V00783178
# Last Modified: April 1 2020

# Resources I used for this assignment:
# https://docs.python.org/3/library/socket.html
# https://www.geeksforgeeks.org/python-map-function/

# imports
from socket import *
import sys

# create UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.settimeout(1.0)

# Assign IP address and port number
host = sys.argv[1]
port = int(sys.argv[2])
serverSocket.bind((host, port))
print ("Reliable UDP Server is now running.")
client_address = False


payload_size = 1024


def main():
    global client_address

    while True:
        if client_address:
            listen()
        else:
            client_address = handshake()    
    return
# End of Main function

def listen():
    packet_in = None

    # Wait for first packet
    while True:
        try:
            packet_in = serverSocket.recvfrom(1024)
        except:
            continue
        break
    split_packet = packet_in[0].decode().split("|")
    if split_packet[0] == "GET":
        filename = split_packet[4]
        with open(filename, "rb") as f:
            while True:
                header = create_header(["DATA", (int(split_packet[2]) + 1024), 0, payload_size]).encode()
                expected_ack = int(split_packet[2]) + payload_size
                bytes_to_send = 1024 - sys.getsizeof(header)
                outputdata = f.read(bytes_to_send)
                if not outputdata:
                    print("Closing connection")
                    # close connection here
                    header = create_header(["FIN", (int(split_packet[2]) + 1024), 0, payload_size])
                    while True:
                        try:
                            serverSocket.sendto(header.encode(), client_address)
                            packet_in = serverSocket.recvfrom(1024)
                        except:
                            continue
                        split_packet = packet_in[0].decode().split("|")
                        if split_packet[0] != "FIN/ACK":
                            continue
                        print("Connection closed with: " + str(client_address))
                        sys.exit()
                while True:
                    try:
                        print("Sending data packet ack # " + str(split_packet[2]))
                        packet_out = header + outputdata
                        serverSocket.sendto(packet_out, client_address)
                        packet_in = serverSocket.recvfrom(1024)
                    except:
                        continue
                    split_packet = packet_in[0].decode().split("|")
                    if int(split_packet[2]) !=  expected_ack:
                        print("expected " + str(expected_ack) + " but got " + split_packet[2])
                        continue
                    break
                

        return
    else:
        print("Received a non-get packet...")


'''
This function securely completes the three-way handshake
using UDP
'''
def handshake():
    packet = None
    split_packet = None
    address = None

    # Receive SYN
    while True:
        try:
            packet = serverSocket.recvfrom(1024)
        except:
            continue
        data = packet[0]
        address = packet[1]
        split_packet = packet[0].decode().split("|")
        if split_packet[0] != "SYN":
            continue
        break

    # Send SYN/ACK, receive ACK
    header = create_header(["SYN/ACK", 0, 1, 0])
    while True:
        serverSocket.sendto(header.encode(), address)
        try:
            packet = serverSocket.recvfrom(1024)
        except:
            continue
        data = packet[0]
        address = packet[1]
        split_packet = packet[0].decode().split("|")
        if split_packet[0] != "ACK" or packet[1] != address:
            continue
        break

    print("Connection with Client Established")
    return address


# Creates a header for each packet
def create_header(header_fields):
    header = "|".join(list(map(lambda x: str(x), header_fields)))
    return header + "|"

main()