import subprocess
import numpy as np
import scipy.stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import operator

node2_mac = 'b8:27:eb:12:55:da'
node3_mac = 'b8:27:eb:f1:36:38'
node4_mac = 'b8:27:eb:f3:5b:97'
landmarks_mac = [node2_mac, node3_mac, node4_mac]
# landmarks = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
landmarks = np.array([[1, 2], [2, 2], [2, 1]])
node_groundtruth = [1, 1]

def get_landmark_rssi(iters):
    print('Begin get landmark rssi...')
    landmark_rssi = []

    for node in landmarks_mac:
        rssi_value = []

        for _ in range(iters):
            command = 'iw dev wlan0 station get ' + node + ' | egrep "signal:"'
            proc = subprocess.check_output(command, shell=True)
            buffer = proc.split(' ')

            RSSI = buffer[2]
            RSSI = RSSI[2:]
            rssi_value.append(int(RSSI))

        landmark_rssi.append(sum(rssi_value) / float(iters))

    return landmark_rssi

def create_uniform_particles(x_range, y_range, N, landmarks):
    print('Begin create uniform particles...')
    particles = np.empty((N, 3))
    particles[:, 0] = np.random.uniform(x_range[0], x_range[1], size=N)
    particles[:, 1] = np.random.uniform(y_range[0], y_range[1], size=N)

    for i in range(N):
        landmark_rssi = get_landmark_rssi(5)
        particles[i, 2] = landmark_rssi[0]

    return particles


def update_particles(particles, weights, z, R, landmarks):
    print('Begin update particles...')
    N = len(particles)
    """
    for i in range(N):
        for j, landmark in enumerate(landmarks):
            distance = np.linalg.norm(particles[:, 0:2] - landmark, axis=1)
            weights[i] *= scipy.stats.norm(distance, R).pdf(z[j])
    """

    for j, landmark in enumerate(landmarks):
        distance = np.linalg.norm(particles[:, 0:2] - landmark, axis=1)
        weights *= scipy.stats.norm(distance, R).pdf(z[j])

    weights += 1.e-300
    weights /= sum(weights)

def estimate(particles, weights):
    print('Begin estimate...')
    position = particles[:, 0:2]
    mean = np.average(position, weights=weights, axis=0)
    index, value = max(enumerate(weights), key=operator.itemgetter(1))
    best = particles[index, :]
    var = np.average((position - mean) ** 2, weights=weights, axis=0)
    return np.array([[mean[0], mean[1]], [var[0], var[1]], [best[0], best[1]]])

def resample(particles, weights):
    print('Begin resample...')
    N = len(particles)
    cumulative_sum = np.cumsum(weights)
    cumulative_sum[-1] = 1.
    indexes = np.searchsorted(cumulative_sum, np.random.rand(N))

    particles[:] = particles[indexes]
    weights.fill(1.0 / N)

def systematic_resample(weights):
    N = len(weights)

    # make N subdivisions, choose positions 
    # with a consistent random offset
    positions = (np.arange(N) + random()) / N

    indexes = np.zeros(N, 'i')
    cumulative_sum = np.cumsum(weights)
    i, j = 0, 0
    while i < N:
        if positions[i] < cumulative_sum[j]:
            indexes[i] = j
            i += 1
        else:
            j += 1
    return indexes

def resample_from_index(particles, weights, indexes):
    particles[:] = particles[indexes]
    weights[:] = weights[indexes]
    weights.fill (1.0 / len(weights))

def neff(weights):
    return 1. / np.sum(np.square(weights))

def run_particle_filter(N, iters, sensor_std_err, do_plot, plot_particles, xlim, ylim):
    print('Begin run particle filter...')
    #plt.figure()

    particles = create_uniform_particles(xlim, ylim, N, landmarks)

    weights = np.zeros(N)
    weights.fill(1.0 / N)

    for x in range(iters):
        print('Loop ' + str(x + 1) + ' of ' + str(iters))

        rssi_measurement_iteration = 5
        rssi_current = get_landmark_rssi(rssi_measurement_iteration)
        print('RSSI Measurement from each node')
        print(rssi_current)

        update_particles(particles, weights, z=rssi_current, R=sensor_std_err, landmarks=landmarks)

        if neff(weights) < N / 2:
            indexes = systematic_resample(weights)
            resample_from_index(particles, weights, indexes)

        estimation_result = estimate(particles, weights)

#        resample(particles, weights)

        print('Estimate node location')
        print('Mean location:', estimation_result[0])
        print('Best location:', estimation_result[2])
        print(estimation_result)
        print('---------------------------------------------------')

        if plot_particles:
            plt.scatter(particles[:, 0], particles[:, 1], color='k', marker=',', s=1)

        p0 = plt.scatter(node_groundtruth[0], node_groundtruth[1], marker='*', color='k', s=180, lw=3)
        p1 = plt.scatter(landmarks[:, 0], landmarks[:, 1], marker='+', color='k', s=180, lw=3)
        p2 = plt.scatter(estimation_result[:, 0], estimation_result[:, 1], marker='s', color='r')
        plt.xlim(*xlim)
        plt.ylim(*ylim)
        plt.legend([p0, p1, p2], ['target', 'landmarks', 'PF'], loc=4, numpoints=1)
        plt.pause(0.5)
        plt.clf()

    print('Final estimate node location')
    # print(estimation_result)
    print('Mean location:', estimation_result[0])
    print('Best location:', estimation_result[2])
    print('Real node location')
    print(node_groundtruth)
    print('Position error (m)')
    print(np.sqrt(np.square(estimation_result[2][0] - node_groundtruth[0]) + np.square(
        estimation_result[2][1] - node_groundtruth[1])))

    plt.scatter(estimation_result[2][0], estimation_result[2][1], marker='s', color='r')
    plt.scatter(landmarks[:, 0], landmarks[:, 1], marker='+', color='k', s=180, lw=3)
    plt.scatter(node_groundtruth[0], node_groundtruth[1], marker='*', color='k', s=180, lw=3)
    plt.legend([p0, p1, p2], ['target', 'nodes', 'PF_estimate'], loc=4, numpoints=1)
    plt.xlim(*xlim)
    plt.ylim(*ylim)
    #plt.show()
    plt.savefig("find_particle.png")

## main
if __name__ == '__main__' :
    N = 100
    iters = 20
    sensor_std_err = 0.1
    do_plot = False
    plot_particles = False
    xlim = (0,3)
    ylim = (0,3)
    run_particle_filter(N, iters, sensor_std_err, do_plot, plot_particles,
                    xlim, ylim)
