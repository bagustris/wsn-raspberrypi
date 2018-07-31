# WSN Part A for 1-hop
# bagustris (bagus@jaist.ac.jp)

import numpy as np
import os
import socket
from time import gmtime, strftime, sleep, time, localtime
from random import randint
import socket
#import time

def get_address_to_connect_to(server_addr):
    non_open_port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect((host, 9))
        client = s.getsockname()[0]
    except socket.error:
        client = "Unknown IP"
    finally:
        del s
    return client

UDP_TARGET = "127.0.0.1"
#UDP_IP = "150.65.249.112"
UDP_PORT = 5005
UDP_SOURCE = "192.168.43.117"

#MESSAGE = "Hello, World!"
#temp = os.system("watch -n 5 'sensors | grep temp1'")
#MESSAGE =str(temp)
		#dummy temperature
#MESSAGE = str(randX)
# waktu2 = 
sequence = 1	# change sequence according to hope
data2 = ()

#print "UDP target IP:", UDP_IP
#print "UDP target port:", UDP_PORT
#print "Time: ", waktu1

n = 1
while n <= 20:
    randX = randint(50, 55)
    waktu1 = strftime("%Y-%m-%d %H:%M:%S", localtime())
    MESSAGE = np.hstack([[waktu1], [UDP_SOURCE], [UDP_TARGET], [sequence], [randX]])
    print "message:", MESSAGE
    sock = socket.socket(socket.AF_INET, # Internet
    					socket.SOCK_DGRAM) # UDP
    millis1 = int(round(time() * 1000))
    data1 = np.hstack((MESSAGE, millis1))
    data3 = ",".join(map(str, data1))
    sock.sendto(data3, (UDP_TARGET, UDP_PORT))
    data2 = np.append(data2, data3)
    n = n + 1
    sleep (5.0)


np.savetxt('tes0.csv', data2[:-1], fmt='%s', delimiter=',')

# to listen use this:
# nc -ul 127.0.0.1 5005
