// (launch with s.ck)

// the patch
SinOsc s1 => JCRev r1 => dac;
SinOsc s2 => JCRev r2 => dac;
SinOsc s3 => JCRev r3 => dac;
SinOsc mel => JCRev melr => dac;
.08 => s1.gain;
.1 => r1.mix;
.08 => s2.gain;
.1 => r2.mix;
.08 => s3.gain;
.1 => r3.mix;
.08 => mel.gain;
.1 => melr.mix;

// create our OSC receiver
OscRecv recv;
// use port 9002 (or whatever)
9002 => recv.port;
// start listening (launch thread)
recv.listen();

// create an address in the receiver, store in new variable
recv.event( "/foo/notes, i i i i i" ) @=> OscEvent @ oe;

// infinite event loop
while( true )
{
    // wait for event to arrive
    oe => now;

    // grab the next message from the queue. 
    while( oe.nextMsg() )
    { 
        int i1;
        int i2;
        int i3;
        int i4;
        int i5;

        // getFloat fetches the expected float (as indicated by "i f")
        oe.getInt() => i1 => Std.mtof => s1.freq;
        oe.getInt() => i2 => Std.mtof => s2.freq;
        oe.getInt() => i3 => Std.mtof => s3.freq;
        oe.getInt() => i4 => Std.mtof => s4.freq;
        oe.getInt() => i5 => Std.mtof => mel.freq;

        // print
        <<< "got (via OSC):", i i i i i>>>;
    }
}