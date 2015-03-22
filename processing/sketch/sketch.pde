import oscP5.*;
import netP5.*;
  
OscP5 oscP5_0;
OscP5 oscP5_1;

void setup() {
  size(400,400);
  // start oscP5, telling it to listen for incoming messages at port 5001 */
  oscP5_0 = new OscP5(this,9002);
  
}
void draw()
{
 
}

void oscEvent(OscMessage theOscMessage) 
{  
  // get the first value as an float
  int firstValue = theOscMessage.get(0).intValue();
 
  //try
  //{
    // get the second value as a float  
    int secondValue = theOscMessage.get(1).intValue();
   
    // get the third value as a float
    int thirdValue = theOscMessage.get(2).intValue();
    // print out the message
    print("OSC Message Received: ");
    print(theOscMessage.addrPattern() + " ");
    println(firstValue + " " + secondValue + " " + thirdValue);
  /*}
  catch (IndexOutOfBoundsException e) 
  {
    // print out the message
    print("OSC Message Received: ");
    print(theOscMessage.addrPattern() + " ");
    println(firstValue);
      
  }*/
  
}
