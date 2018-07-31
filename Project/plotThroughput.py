# plot throughput

import numpy as np
import matplotlib.pyplot as plt

plt.rcdefaults()

n = 3
throughput = (9.73, 5.69, 3.10)
hop = ('1', '2', '3')
y_pos = np.arange(len(hop))
width = 0.35

fig, ax = plt.subplots()
rects = ax.bar(y_pos, throughput)
ax.set_ylabel('End-to-end tihroughput (Mbits/sec)')
ax.set_xlabel('Number of hop')

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % float(height),
                ha='center', va='bottom')

autolabel(rects)
plt.show()
