## WSN Final Project
## Localization of an unknown stationary sensor node based on RSSI
## Intro: You deploy your sensor node in the free space.
## You know all of the locations of your sensor nodes except one of them.
## Luckily, you can get signal strength (RSSI) between the unknown node and other nodes.
## Let's try to locate this node!

import matplotlib.pyplot as plt
import numpy as np
import sys
import subprocess

## Global parameters
# determine these parameters based on log distance path loss model
# PL_d0_to_d = PL_d0 +10nlog(d/d0)
# where, PL_d0      = path loss at distance d0
#        PL_d0_to_d = path loss at an arbitrary distance d
#        n          = path loss exponent
#        d          = current distance of the node

## Task #0: Determine initial parameters (Hint: d0 can be defined using an appropriate value)
d0 =
n =
PL_d0 =

## Task #0.5: Find the mac address of each node and its coordinate. We will call these nodes as landmarks.
##          In addition, input the unknown node's coordinate as node_groundtruth
node1_mac = 'xx:xx:xx:xx:xx:xx'
node2_mac = ''
node3_mac = ''
landmarks_mac = [node1_mac, node2_mac, node3_mac]
landmarks = np.array([[node1_x, node1_y],[1, 0][node1_x, node1_y],[node1_x, node1_y]])

node_groundtruth = [node_groundtruth_x, node_groundtruth_y]

## Task #1: Find the way to measure RSSI from unknown node to other nodes.
## The command for measure RSSI from source to destination is...

## iw dev wlan0 station get <destination_mac_address>
## Try it in Terminal first! The result should look like this:

## Station xx:xx:xx:xx:xx:xx (on wlan0)
##	rx packets:	400605
##	tx packets:	225023
##	tx failed:	3
##	rx drop misc:	2641
##	signal:  	-48 dBm    << This is your RSSI reading!
##	tx bitrate:	72.0 MBit/s

## Big Hint: you can use the command ' egrep "signal:" ' to get only the RSSI line. Ex.

## iw dev wlan0 station get <destination_mac_address> | egrep "signal:"

## You can get mac address by using the command 'ifconfig' in Terminal
def rssi_measurement(iter):
    # measure RSSI from landmarks for [iter] iterations
    for node in landmarks_mac:
        for i in range(iter):

            command =

            ## this subprocess.check_output function is used to get the result from the input command shell script.
            proc = subprocess.check_output(command, shell=True)

            ## try to do some text processing here to get the RSSI number output.





    return landmarks_rssi

## Task #2: Define each particle by random its location(x,y) and calculate its RSSI
def create_uniform_particles(x_range, y_range, N, landmarks):
        particles = np.empty((N, 3))

        # uniformly random x coordinate over [0, x_range]
        particles[:, 0] =
        # uniformly random y coordinate over [0, y_range]
        particles[:, 1] =

        # calculate the particle's RSSI based on landmarks
        for i in range (N):
                x = particles[i, 0]
                y = particles[i, 1]
                ## your particle RSSI calculation start here...





                particles[i, 2] =
                # each particle should be like: [x_coord, y_coord, RSSI_cal]

        return particles

# Task #3: Define the weights update of particles based on the RSSI measurements
def update(particles, weights, z, R, landmarks):
        N = len(particles)

        ## your weight update code start here...
        ## by using normal distribution (Hint: pdf should be like f(x = RSSI_cal | mu = z, var^2 = R))
        ## the weight of each particle should be the product of each landmark pdf
        ## e.g. weight_t = weight_t_minus_1 * weight_node_1 * weight_node_2 * ... * weight_node_n
        for i in range (N):
            for j, landmark in enumerate(landmarks):
                ## your code here...





                weights[i] =
                # final weight should be in array coresponding to particles array

        # avoid round-off to zero
        weights += 1.e-300

        # finally we normalize the weight
        weights =

## Task #4: Define the estimation method
def estimate(particles, weights):
        # Determine the location of the unknown node by using the information from particles and their weights
        # What is your estimation method
        # (Hint: some popular estimation methods: mean, weight average, numbers of best particles, etc. Please do discuss the choice that you make.)

        particle_position_xy = particles[:, 0:2]

        # your code here...





        return estimate_coordinate

## Task #5: Define resampling method
def resample(particles, weights):
        # Resample your particle! You want particles with higher weight to survive to the next iteration for more accurate result.
        # There are various methods for resampling your particles. You can try to pick top particles and get rid of the lowest ones.
        # Or pick new set of particles based on the weights! Let's try your method and do some discussion.

        # your code here...





## Task Bonus!
def neff(weights):
        return ##?????

def run_pf1(N, iters, sensor_std_err=1,
                        do_plot=True, plot_particles=False,
                        xlim, ylim):
        plt.figure()

        ## Task 2 initialize particles and weights
        particles = create_uniform_particles(xlim, ylim, N, landmarks)

        weights = np.zeros(N)
        weights.fill(1.0 / N)

        for x in range(iters):

                print('Loop ' + str(x+1) + ' of ' + str(iters))

                ## Task 1: RSSI measurement and update particles RSSI
                RSSI_measurement_iteration =
                rssi_current = rssi_measurement(RSSI_measurement_iteration)
                print('RSSI Measurement from each node')
                print(rssi_current)

                ## Task 3: update particles' weight
                update(particles, weights, z=rssi_current, R=sensor_std_err,
                                 landmarks=landmarks)


                ## Task Bonus! Resample occured if the effective particles are low. But why?
##                if neff(weights) < ???:
##                    resample(particles, weights)

                ## Task 4: estimation
                estimation_result = estimate(particles, weights)

                ## Task 5: resample
                resample(particles, weights)



                print('Estimate node location')
                print(estimation_result)
                print('---------------------------------------------------')

                if plot_particles:
                        plt.scatter(particles[:, 0], particles[:, 1],
                                                color='k', marker=',', s=1)
                p1 = plt.scatter(landmarks[:,0], landmarks[:,1], marker='+',color='k', s=180,lw=3)
                p2 = plt.scatter(estimation_result[0], estimation_result[1], marker='s', color='r')
                plt.xlim(*xlim)
                plt.ylim(*ylim)
                plt.legend([p1, p2], ['nodes', 'PF'], loc=4, numpoints=1)
                plt.pause(0.5)
                plt.clf()

        print('Final estimate node location')
        print(estimation_result)
        print('Real node location')
        print(node_groundtruth)
        print('Position error (m)')
        print(np.sqrt(np.square(estimation_result[0]-node_groundtruth[0]) + np.square(estimation_result[1]-node_groundtruth[1])))

        plt.scatter(estimation_result[0], estimation_result[1], marker='s', color='r')
        plt.scatter(landmarks[:,0], landmarks[:,1], marker='+',color='k', s=180,lw=3)
        plt.legend([p1, p2], ['nodes', 'PF_estimate'], loc=4, numpoints=1)
        plt.xlim(*xlim)
        plt.ylim(*ylim)
        plt.show()

######## Run main program here #######
## You will also need to define the following:

## N       = number of particles
## iters   = number of iterations
## xlim, ylim = size of your workspace in meter, e.g. xlim = (0,10), ylim = (0,10)

run_pf1(N = ???, iters = ???, sensor_std_err=1, do_plot=True, plot_particles=True,
                        xlim=(0, ???), ylim=(0, ???)))
