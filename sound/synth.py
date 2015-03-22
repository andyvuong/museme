from mingus.midi import fluidsynth
import mingus.core.progressions as progressions
import mingus.core.notes as notes
from simpleOSC import initOSCClient, sendOSCMsg, initOSCServer, startOSCServer, setOSCHandler
import time, math, random, sys
import threading


try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range

def process_mood(addr, tags, data, source):
  print "received new osc msg from %s" % getUrlStr(source)
  print "with addr : %s" % addr
  print "typetags :%s" % tags
  print "the actual data is : %s" % data
  mood = data


chords = [
['I', 'III', 'V', 'II'],
['I', 'IV', 'V', 'ii'],
['IV', 'viidim', 'iii', 'V'],
['III', 'VII', 'VI', 'V'],
['iidim', 'iv', 'v', 'III'],
['IIdim', 'IVdim', 'IIIdim', 'VIdim']]

tempo = [1, 0.5, 0.4, 0.3, 0.2, 0.2]

#mood goes from 0-5, calm to angry
#angry should cause faster and redder
mood = 3




eeg_waves = []
a_waves = []
b_waves = []



ip = "localhost"
port1 = 9002
port_receive = 9001
base_a4=440


port1 = sys.argv[1]

initOSCClient(ip, int(port1))
'''
initOSCServer(ip, int(port_receive), 0)
setOSCHandler('/mood', process_mood)
startOSCServer()
'''

def mtof(midi):
	return base_a4*2**((midi-9)/12.0)



def process_eeg(addr, tags, data, source):

  print "received new osc msg from %s" % getUrlStr(source)
  print "with addr : %s" % addr
  print "typetags :%s" % tags
  print "the actual data is : %s" % data
  avg = sum(data) / float(len(data))
  eeg_waves.append(avg)
  if(len(eeg_waves) > 100):
    eeg_waves.pop(0)

def process_alpha(addr, tags, data, source):

  print "received new osc msg from %s" % getUrlStr(source)
  print "with addr : %s" % addr
  print "typetags :%s" % tags
  print "the actual data is : %s" % data
  avg = sum(data) / float(len(data))
  a_waves.append(avg)
  if(len(a_waves) > 100):
    a_waves.pop(0)

def process_beta(addr, tags, data, source):

  print "received new osc msg from %s" % getUrlStr(source)
  print "with addr : %s" % addr
  print "typetags :%s" % tags
  print "the actual data is : %s" % data
  avg = sum(data) / float(len(data))
  b_waves.append(avg)
  if(len(b_waves) > 100):
    b_waves.pop(0)

def is_peak(freqs):
  minf = min(freqs)
  maxf = max(freqs)


p = progressions.to_chords(chords[mood])
print progressions.to_chords(p, "D")


for k, chord in enumerate(p):
	temp = []
	for j, note in enumerate(chord):
		temp.append(60 + notes.note_to_int(note))
	print temp
	p[k] = temp

i=0
j=0
curchord = 0
#n iterations of while loop
chord_length = 4
index = 0
offset = 0
speed = 1
sleeptime = 0.5
try:
  while(1):
    print i
    note_play = random.randint(0, 10)

    
    if mood > 3:
        sleeptime = tempo[mood]
        speed = 3

    if note_play*speed >= 4:

      offset = random.randint(-1,2)*11
      index = random.randint(0, len(p[i])-1)
      templist = p[curchord] + [mood] + [p[curchord][index]+offset]
      sendOSCMsg("/out", [templist])
      print 'played', templist
      j += 1

    
    #every i intereations
    elif i >= 4 and note_play != 0:
      templist = p[curchord] + [mood] + [p[curchord][index]+offset]
      sendOSCMsg("/out", [templist])
      print 'played', templist

    i += 1
    
    if (i >= len(p)):
      curchord += 1
      i = 0
    if (j >= len(p)):
      j = 0
    if (curchord >= len(p)):
      
      curchord = 0

    time.sleep(sleeptime)
except (SystemExit, KeyboardInterrupt) as exc:
  print "closing all OSC connections... and exit"
  closeOSC()
