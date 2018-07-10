source_mac_address = ''
destination1_mac_address = ''

landmarks_mac = [destination1_mac_address]

def rssi_measurement(iter):
    # measure RSSI from landmarks for [iter] iterations
    landmarks_rssi = []
    for node in landmarks_mac:
        for i in range(iter):
            
            command = 'iw dev wlan0 station get ' + node + ' | egrep "signal:"'
            
            ## this subprocess.check_output function is used to get the result from the input command shell script.
            proc = subprocess.check_output(command, shell=True)
            
            ## try to do some text processing here to get the RSSI number output.
            
            buffer = proc.split(' ')
	    ##['signal:', '', '\t-48', 'dBm']
	    RSSI = buffer[2]
            ##'\t-48'
	    RSSI = RSSI[2:]
	    ##'48'
            landmarks_rssi.append(int(RSSI))

    landmarks_rssi = sum(landmarks_rssi)/float(iters)
    return landmarks_rssi

## main
rssi_measurement(1)
