## python dummy data for 2nd experiment

import numpy as np
from time import gmtime, strftime, sleep, time, localtime
from random import randint, uniform

n = 1
data3 = ()

while n<=720:
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    txpower = randint(21, 28)
    RSSI = randint(30,40)
    xy = np.random.uniform(0.1,0.4,(1,2))
    error = np.random.uniform(0.07, 0.44, (1,1))
    data = [time , txpower, RSSI, xy, float(error)]
    data2 = ",".join(map(str, data))
    data3 = np.append(data2, data3)
    print(data)
    n = n + 1
    sleep (5.0)
    
np.savetxt('partB_3.csv', data3, fmt='%s', delimiter=',')
