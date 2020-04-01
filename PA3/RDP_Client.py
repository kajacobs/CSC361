# Katherine Jacobs
# V00783178
# Last Modified: April 1 2020

# Resources I used for this assignment:
# https://docs.python.org/3/library/socket.html
# https://www.geeksforgeeks.org/python-map-function/
# Link below is code that I used from stack overflow for the md5 checksum
# https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file

from socket import *
import sys
import hashlib


host = sys.argv[1]
port = int(sys.argv[2])
filename = sys.argv[3]
outputfile = sys.argv[4]

def main():

    # Create socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1.0)
    address = (host, port)
    # 3 way handshake with server
    connected = handshake(clientSocket, address)

    if not connected:
        print("unsuccessful handshake")
        sys.exit()

    # GET request for file
    expected_syn = 1
    header = create_header(["GET", 1, 1, 0])
    packet_out = header + filename
    split_packet = None
    print("sending GET request")
    with open(outputfile, "wb") as f:
        while True:
            expected_syn += 1024
            # Securely receive and send an ack
            while True:
                clientSocket.sendto(packet_out.encode(), address)
                try:
                    packet_in = clientSocket.recvfrom(1024)
                except:
                    continue
                split_packet = packet_in[0].decode().split("|")
                if int(split_packet[1]) != expected_syn:
                    continue # resend ACK if we're not getting new data
                break
            if (split_packet[0] == "FIN"):
                header = create_header(["FIN/ACK", 0, split_packet[1], 0])
                clientSocket.sendto(header.encode(), address)
                break
            data = "|".join(split_packet[4:])
            f.write(data.encode())
            packet_out = create_header(["ACK", 0, int(split_packet[1]), 0])


    with open(outputfile, "r") as f:
        print("Requested File: ")
        print(f.read())
        output_md = md5(outputfile)
        intput_md = md5(filename)
        print("md5 of input file:  " + intput_md)
        print("md5 of output file: " + output_md)
    return
# End of Main function


#3 way handshake with server
def handshake(clientSocket, address):
    packet = create_header(["SYN", 0, 0, 0])

    # Send SYN, receive SYN/ACK
    while True:
        clientSocket.sendto(packet.encode(), address)
        try:
            packet = clientSocket.recvfrom(1024)
        except:
            continue
        split_packet = packet[0].decode().split("|")

        if split_packet[0] != "SYN/ACK":
            continue
        packet = create_header(["ACK", 1, 1, 0])
        clientSocket.sendto(packet.encode(), address)
        break
    return True

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Creates a header for each packet
def create_header(header_fields):
    header = "|".join(list(map(lambda x: str(x), header_fields)))
    return header + "|"

main()