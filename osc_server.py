from liblo import *
import sys
import time

class MuseServer(ServerThread):
    #listen for messages on port 5001
    def __init__(self):
        ServerThread.__init__(self, 5001)

    #receive accelrometer data
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):
        acc_x, acc_y, acc_z = args
        print "%s %f %f %f" % (path, acc_x, acc_y, acc_z)

    #receive battery data
    @make_method('/muse/batt', 'iiii')
    def batt_callback(self, path, args):
        state_charge, fuel_gauge, adc, temperature = args
        print "%s %i %i %i %i" % (state_charge, fuel_gauge, adc, temperature)

    #receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        print "%s %f %f %f %f" % (path, l_ear, l_forehead, r_forehead, r_ear)

    #receive DRLREF data
    #@make_method('/muse/drlref', 'ff')


    #this block is devoted to picking up elements data [digital signal processing portions]
    #receive Fourier Fast Trasform [for each channel]
    #@make_method('/muse/element/raw_fft0', 'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')


    #handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        print "Unknown message \
        \n\t Source: '%s' \
        \n\t Address: '%s' \
        \n\t Types: '%s ' \
        \n\t Payload: '%s'" \
        % (src.url, path, types, args)

try:
    server = MuseServer()
except ServerError, err:
    print str(err)
    sys.exit()

server.start()

if __name__ == "__main__":
    while 1:
        time.sleep(1)
