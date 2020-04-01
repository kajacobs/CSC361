# Katherine Jacobs
# V00783178
# Last Modified: Mar 03 2020

# Resources I used for this assignment
# https://thispointer.com/python-how-to-get-current-date-and-time-or-timestamp/

from socket import *
from datetime import datetime
import sys

host = sys.argv[1]
port = int(sys.argv[2])

clientSocket = socket(AF_INET, SOCK_DGRAM)

i = 1
while i <= 100:
    # create timestamp
    start_time = datetime.now()
    message = f"Ping {i} {start_time.time()}"
    # send message to server
    clientSocket.sendto(message.encode(), (host, port))

    # receive message from client
    data = clientSocket.recv(4096)

    
    # if ping is not allcaps, resend
    while (data.decode('ascii') == 'Packet Dropped'):
        print(f"    ...Sending packet {i} again!")
        clientSocket.sendto(message.encode(), (host, port))
        data = clientSocket.recv(4096)
    
    end_time = datetime.now()

    RTT = end_time - start_time
    print(data.decode('ascii'))
    print(str(RTT.total_seconds()) + ' seconds.')
    i += 1




