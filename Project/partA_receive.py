# python code to receive data for I223 WSN Class at JAIST
# bagustris (bagus@jaist.ac.jp)

import socket
import numpy as np
from time import gmtime, strftime, sleep, time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
 
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
dest = socket.gethostbyname(UDP_IP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

n = 1  
write_data = []

while n<=20:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data = data.split(',')
    #data = [message, millis1]
    #waktu2 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    millis2 = int(round(time() * 1000))
    timeDif = millis2 - int(data[5])
    print "received message:", data[:-1] , "in ", timeDif, "miliseconds"
    print "from ", addr
    data2 = np.hstack((data[:-1], timeDif))
    data2 = ",".join(map(str, data2))
    write_data = np.append(write_data, data2)
    n = n + 1

np.savetxt('tes.csv', write_data, fmt='%s')

