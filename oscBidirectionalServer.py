#!/usr/bin/env python

"""
Python script for setting up a bidirectional OSC server between the computer and the Muse

This script was tested using Python 2.7.9 and MuseIO firmware 3.6.5 ['muse-io 3.6.5 (Build-21 Jan 30 2015 20:12:18)']

tested with 'muse-io --osc osc.udp://localhost:5001,osc.udp://localhost:5002'
need to add condition with timestamp flag
"""

from liblo import *
import sys
import time
import signal
import socket

# port to listen for osc messages
listener_port = 5002
# port to send our osc messages
target_port = Address('localhost', 5003)
# 10.1.101.51 for remote

def handler(signum, frame):
    print 'Ctrl+Z pressed, but ignored. Try Ctrl+C instead.'

class MuseServer(ServerThread):
    #listen for messages on the specified port
    def __init__(self):
        ServerThread.__init__(self, listener_port)

    #receive accelrometer data
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):
        acc_x, acc_y, acc_z = args
        print "%s %f %f %f" % (path, acc_x, acc_y, acc_z)
        send(target_port, "%s %f %f %f" % (path, acc_x, acc_y, acc_z))
        #send(target_port, path, acc_x, acc_y, acc_z)

    #receive battery data
    @make_method('/muse/batt', 'iiii')
    def batt_callback(self, path, args):
        state_charge, fuel_gauge, adc, temperature = args
        print "%s %i %i %i %i" % (path, state_charge, fuel_gauge, adc, temperature)
        send(target_port, "%s %i %i %i %i" % (path, state_charge, fuel_gauge, adc, temperature))

    #receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        print "%s %f %f %f %f" % (path, l_ear, l_forehead, r_forehead, r_ear)
        send(target_port, "%s %f %f %f %f" % (path, l_ear, l_forehead, r_forehead, r_ear))

    #receive EEG quantization data
    @make_method('/muse/eeg/quantization', 'iiii')
    def eeg_quantize_callback(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        print "%s %i %i %i %i" % (path, l_ear, l_forehead, r_forehead, r_ear)
        send(target_port, "%s %i %i %i %i" % (path, l_ear, l_forehead, r_forehead, r_ear))

    #receive DRLREF data
    @make_method('/muse/drlref', 'ff')
    def drlref_callback(self, path, args):
        drl, reference = args
        print "%s %f %f" % (path, drl, reference)
        send(target_port, "%s %f %f" % (path, drl, reference))

    #
    #this block is devoted to picking up elements data [digital signal processing portions]
    #[DO NOT THINK THIS IS NEEDED]
    #
    #receive Fourier Fast Trasform [for each channel]
    @make_method('/muse/elements/raw_fft0', 'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
    def fft0_callback(self, path, args):
        myList = args
        #print "%s" % (path)

    @make_method('/muse/elements/raw_fft1', 'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
    def fft1_callback(self, path, args):
        myList = args
        #print "%s" % (path)

    @make_method('/muse/elements/raw_fft2', 'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
    def fft2_callback(self, path, args):
        myList = args
        #print "%s" % (path)

    @make_method('/muse/elements/raw_fft3', 'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
    def fft3_callback(self, path, args):
        myList = args
        #print "%s" % (path)
    
    """
    #Absolute Band Powers
    #logarithm of the Power Spectral Density of the EEG data for each channel (may have negative values)
    #units in Bels, emitted at 10Hz
    """
    #1-8Hz, log band power (B)
    @make_method('/muse/elements/low_freqs_absolute', 'ffff')
    def lowfreqabs_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))

    #1-4Hz, log band power (B)
    @make_method('/muse/elements/delta_absolute', 'ffff')
    def deltaabs_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))

    #5-8Hz, log band power (B)
    @make_method('/muse/elements/theta_absolute', 'ffff')
    def thetaabs_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))

    #9-13Hz, log band power (B)
    @make_method('/muse/elements/alpha_absolute', 'ffff')
    def alphaabs_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))

    #13-30Hz, log band power (B)
    @make_method('/muse/elements/beta_absolute', 'ffff')
    def betaabs_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))

    #0-50Hz, log band power (B)
    @make_method('/muse/elements/gamma_absolute', 'ffff')
    def gammaabs_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))

    """
    #Relative Band Powers
    #calculated by taking the absolute band power score and dividing by the sum of the total band powers
    #                                                    alpha_absolute  
    #relative_alpha =           ------------------------------------------------------------------
    #                   alpha_absolute + beta_absolute + delta_absolute + gamma_absolute + theta_absolute
    """
    #delta relative
    @make_method('/muse/elements/delta_relative', 'ffff')
    def deltarel_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))
    #theta relative
    @make_method('/muse/elements/theta_relative', 'ffff')
    def thetarel_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))
    #alpha relative
    @make_method('/muse/elements/alpha_relative', 'ffff')
    def alpharel_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))
    #beta relative
    @make_method('/muse/elements/beta_relative', 'ffff')
    def betarel_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))
    #gamma relative
    @make_method('/muse/elements/gamma_relative', 'ffff')
    def gammarel_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
        send(target_port, "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4))

    """
    #Band Power Sessions Scores
    #[DO NOT THINK THIS IS NEEDED]
    """
    #delta relative
    @make_method('/muse/elements/delta_session_score', 'ffff')
    def delta_score_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        #print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
    #theta relative
    @make_method('/muse/elements/theta_session_score', 'ffff')
    def theta_score_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        #print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
    #alpha relative
    @make_method('/muse/elements/alpha_session_score', 'ffff')
    def alpha_score_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        #print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
    #beta relative
    @make_method('/muse/elements/beta_session_score', 'ffff')
    def beta_score_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        #print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)
    #gamma relative
    @make_method('/muse/elements/gamma_session_score', 'ffff')
    def gamma_score_callback(self, path, args):
        channel_1, channel_2, channel_3, channel_4 = args
        #print "%s %f %f %f %f" % (path, channel_1, channel_2, channel_3, channel_4)

    """
    #Headband Status
    #emitted at 10Hz
    """
    #Boolean value 1 represents that Muse is on the head correctly
    @make_method('/muse/elements/touching_forehead', 'i')
    def forehead_callback(self, path, args):
        touching = args
        print "%s %r" % (path, touching)
        send(target_port, "%s %r" % (path, touching))

    #Status indicator for each channel (think of the Muse status indicator that looks like a horseshoe).
    #1 = good, 2 = ok, >=3 bad
    @make_method('/muse/elements/horseshoe', 'ffff')
    def horseshoe(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        print "%s %f %f %f %f" % (path, l_ear, l_forehead, r_forehead, r_ear)
        send(target_port, "%s %f %f %f %f" % (path, l_ear, l_forehead, r_forehead, r_ear))

    #Strict data quality indicator for each channel, 0= bad, 1 = good.
    @make_method('/muse/elements/is_good', 'iiii')
    def qualitycheck(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        print "%s %i %i %i %i" % (path, l_ear, l_forehead, r_forehead, r_ear)
        send(target_port, "%s %i %i %i %i" % (path, l_ear, l_forehead, r_forehead, r_ear))

    """
    #Muscle Movement
    #emitted at 10Hz
    """
    #Boolean 1 represents a blink was detected
    @make_method('/muse/elements/blink', 'i')
    def blinkcheck(self, path, args):
        blink = args
        print "%s %r" % (path, blink)
        send(target_port, "%s %r" % (path, blink))

    #Boolean value 1 represents a jaw clench was detected
    @make_method('/muse/elements/jaw_clench', 'i')
    def jawcheck(self, path, args):
        clench = args
        print "%s %r" % (path, clench)
        send(target_port, "%s %r" % (path, clench))

    
    #Experimental
    #paths in this section can change with each release - they may even disappear entirely!
    #will approximately take 1 minute with Muse on the head to start producing meaningful values
    #emitted at 10Hz
    #Each channel is scored independently for alpha/gamma for mellow/concentration, 
    #and the average of the two channels is taken every time. 
    #If there is bad data, the previous score is used, but there is always an average of channels.

    #Concentration
    #based on gamma, but with additional processing to make it more reflective of the user's experience
    """
    #This value goes up when you are focusing on something particular, thinking about something with intensity, 
    #concentrating on something, waiting in expectation for something to happen, trying to solve a problem, 
    #or working your intellectual mind. 
    #Warning: If you tense up your muscles, 
    #it can get confuse this measure in that this value may go up when you do that.

    #The concentration score is 1 when your attention is directed at something very particular 
    #and with high intensity. The dynamics of the score (i.e. the range and the variations) 
    #haven't been tuned since it is an experimental release. The transitions between high 
    #concentration and low concentration are usually abrupt, so the score is currently 
    #more of a "yes/no" type score instead of a gradient from 0-1.
    """
    @make_method('/muse/elements/experimental/concentration', 'f')
    def concentrationcheck(self, path, args):
        fromconcentrate = args
        print "%s %s" % (path, fromconcentrate)
        send(target_port, "%s %s" % (path, fromconcentrate))

    #Mellow
    #based on alpha, but with additional processing to make it more reflective of the user's experience
    """
    #This value goes up when you are relaxing, letting go of judgement, letting go of trying to control things, 
    #letting go of attachment to outcome, not thinking about anything with a goal, 
    #or being without an active task.  
    #You are not engaged in strenuous mental processing but still alert to your senses. 
    #A ready, waiting state.
    """
    @make_method('/muse/elements/experimental/mellow', 'f')
    def mellowcheck(self, path, args):
        mellowing = args
        print "%s %s" % (path, mellowing)
        send(target_port, "%s %s" % (path, mellowing))
    
    #handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        print "Unknown message \
        \n\t Source: '%s' \
        \n\t Address: '%s' \
        \n\t Types: '%s ' \
        \n\t Payload: '%s'" \
        % (src.url, path, types, args)

signal.signal(signal.SIGTSTP, handler)

try:
    server = MuseServer()
except (KeyboardInterrupt, SystemExit):
    raise
#except (signal.SIGTSTP, SystemExit):
#    raise
except ServerError, err:
    print str(err)
    sys.exit()

server.start()


if __name__ == "__main__":
    while 1:
        time.sleep(1)
