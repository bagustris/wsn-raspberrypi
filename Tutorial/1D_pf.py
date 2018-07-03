from numpy.random import uniform
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import operator

def create_uniform_particles(x_range, N):
    particles = np.empty((N, 2))
    particles[:, 0] = uniform(x_range[0], x_range[1], size=N)
    return particles

def update(particles, weights, z, R):
    N = len(particles)
    weights *= scipy.stats.norm(particles[:, 1], R).pdf(z)
    weights += 1.e-300      # avoid round-off to zero
    weights /= sum(weights) # normalize

def estimate(particles, weights):
    pos = particles[:, 0]
    mean = np.average(pos, weights=weights, axis=0)
    index, value = max(enumerate(weights), key=operator.itemgetter(1))
    best = particles[index, 0]
    var  = np.average((pos - mean)**2, weights=weights, axis=0)
    return mean, var, best

def resample(particles, weights):
    N = len(particles)
    cumulative_sum = np.cumsum(weights)
    cumulative_sum[-1] = 1. # avoid round-off error
    indexes = np.searchsorted(cumulative_sum, np.random.rand(N))
    # resample according to indexes
    particles[:] = particles[indexes]
    weights[:] = weights[indexes]

def run_pf(N, iters, sensor_std_err, xlim):
    plt.figure()
    # initialize weights and particles
    weights = np.zeros(N)
    weights.fill(1.0 / N)
    particles = create_uniform_particles(xlim, N)

    for i in range(iters):
        # update the range sensor measurement with some error
        z = abs(robot_position[i] - target_position + np.random.normal(0, 1))
        # update the particles measurement
        particles[:, 1] = abs(particles[:, 0]-robot_position[i])
        # calculate and update weights
        update(particles, weights, z, sensor_std_err)
        # estimation
        mean, var, best = estimate(particles, weights)
        # do resample
        resample(particles, weights)

        # print and plot
        print('Iteration ' + str(i+1))
        print('Mean estimate = ' + str(mean))
        print('Best estimate = ' + str(best))
        print('==========================================')
        plt.scatter(particles[:, 0], weights, color='k', marker=',', s=1)
        p1 = plt.scatter(robot_position[i], 0, marker='s',color='k', s=180,lw=3)
        p2 = plt.scatter(target_position, 0, marker='x', color='g')
        p3 = plt.scatter(mean, 0, marker='o', color='r')
        p4 = plt.scatter(best, 0, marker='p', color='b')
        plt.xlim(*xlim)
        plt.ylim((-0.001, max(weights)))
        plt.legend([p1, p2, p3, p4], ['robot', 'target', 'mean estimate', 'best estimate'], loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
        plt.show()

    print('- Summary -')
    print('Mean estimate = ' + str(mean))
    print('Best estimate = ' + str(best))
    print('Target position = ' + str(target_position))
    print('Mean estimate error = ' + str(abs(mean-target_position)))
    print('Best estimate error = ' + str(abs(best-target_position)))

## main program
robot_position = [5,6,7,8,9]
target_position = 2
N = 100
sensor_std_err = 1
xlim = (0, 10)
run_pf(N, iters = len(robot_position), sensor_std_err = sensor_std_err, xlim = xlim)
