from mingus.midi import fluidsynth
import mingus.core.progressions as progressions
import mingus.core.notes as notes
from simpleOSC import initOSCClient, sendOSCMsg
import time, math, random
import threading

try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range


chords = [
[],
[],
[],
[],
[],
[]]

ip = "localhost"
port = 9002
base_a4=440
initOSCClient(ip, port)

def mtof(midi):
	return base_a4*2**((midi-9)/12.0)

p = progressions.to_chords(['I', 'III', 'V', 'II'])
print progressions.to_chords(p, "C")
print(p)

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

while(1):
  print i
  note_play = random.randint(0, 10)

  mood = 1
  if mood > 3:
      speed = 1.5

  if note_play*speed >= 4:
    offset = random.randint(-2,2)*11
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

  time.sleep(0.75)

