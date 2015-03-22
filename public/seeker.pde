//import oscP5.*;
//import netP5.*;
  
//OscP5 oscP5_0;

//PFont WQY10;

int numBalls = 25600;
int maxBalls = numBalls;
int fps;
boolean clearBG, doSmooth;
int shapeType;
float maxVelocity = 6, minAccel = 0.2, maxAccel = 0.6;
int time = 0;
int changingcol = 0;

int last_melody_note = 0;
int dest_x = width/2;
int dest_y = height/2;
Seeker[] ball = new Seeker[numBalls];

void setup(){
  //oscP5_0 = new OscP5(this,9001);
  size(1000,500);
  //size(displayWidth, displayHeight);
  colorMode(HSB, 255);
  noStroke();
  //WQY10 = loadFont("WenQuanYiMicroHei-10.vlw");
  //textFont(WQY10);
  clearBG = true;
  doSmooth = false;
  shapeType = 1;
  
  for(int i=0; i<numBalls; i++){
    ball[i] = new Seeker(new PVector(random(width), random(height)));
  }
  
  // numBalls adjusted to a sane default for web distribution
  numBalls = 1200;
}

void draw(){
  if(clearBG){
    background(#98C6EE);
  }
   
   
  time++;
  if(time > 200)
  {
      moveBalls(int(random(1000)));
     time = 0;
     changingcol = (changingcol+32)%255;
  } 
  rectMode(CENTER);
  for(int i=0; i<numBalls; i++){
//    smoothColor(ball[i], changingcol);
    ball[i].seek(new PVector(dest_x, dest_y));
    ball[i].render();
  }
  
  //statusWindow();

}

void statusWindow(){
  fill(50, 150);
  rectMode(CORNER);
  rect(5, 5, 140, 150);
  fill(0, 160, 255);
  text ((int)frameRate + " FPS", 15, 30);
  if (shapeType == 0){
    text ("(t) squares", 15, 45);
  }
  else{
    text ("(t) dots", 15, 45);
  }

  if (clearBG){
    text ("(p) clear BG", 15, 60);
  }
  else{
    text ("(p) paint BG", 15, 60);
  }

  if (doSmooth){
    text ("(o) smooth", 15, 75);
  }
  else{
    text ("(o) no smooth", 15, 75);
  }

  text("(z/a) Max velocity: " + nf(maxVelocity, 1, 1), 15, 90);
  text("(x/s) Min acceleration: " + nf(minAccel, 1, 2), 15, 105);
  text("(c/d) Max acceleration: " + nf(maxAccel, 1, 2), 15, 120);
  text("(v/f) Number of specks: " + numBalls, 15, 135);
  text("Current Color: " + changingcol, 15, 150);
}

void keyPressed() {
  if (key == 'p' || key == 'P') {
    clearBG = !clearBG;
  }
  if (key == 't' || key == 'T') {
    shapeType = 1-shapeType;
  }
  if (key == 'o' || key == 'O') {
    doSmooth = !doSmooth;
    if (doSmooth){
      smooth();
    }
    else{
      noSmooth();
    } 
  }
  if ((key == 'z' || key == 'Z') && maxVelocity > 1) {
    maxVelocity--;
  }
  if (key == 'a' || key == 'A') {
    maxVelocity++;
  }
  if ((key == 'x' || key == 'X') && minAccel > 0) {
    minAccel-=.05;
  }
  if (key == 's' || key == 'S') {
    minAccel+=.05;
    minAccel = min(minAccel, maxAccel);
  } 
  if (key == 'c' || key == 'C') {
    maxAccel-=0.05;
    maxAccel = max(minAccel, maxAccel);
  }
  if (key == 'd' || key == 'D') {
    maxAccel+=0.05;
  }
  if ((key == 'v' || key == 'V')) {
    numBalls-=50;
    numBalls = max(0, numBalls);
  }
  if (key == 'f' || key == 'F') {
    numBalls+=50;
    numBalls = min(maxBalls, numBalls);
  }
}
/*
void oscEvent(OscMessage theOscMessage) 
{  
  // get the first value as an float
  int firstValue = theOscMessage.get(0).intValue();
    // get the second value as a float  
    int secondValue = theOscMessage.get(1).intValue();
   
    // get the third value as a float
    int thirdValue = theOscMessage.get(2).intValue();
    int mood = theOscMessage.get(3).intValue();
    int fourthValue = theOscMessage.get(4).intValue();
    // print out the message
    print("OSC Message Received: ");
    print(theOscMessage.addrPattern() + " ");
    println(firstValue + " " + secondValue + " " + thirdValue + " " + mood + " " + fourthValue);
    
  moveBalls(fourthValue);
}
*/

void jsEvent(int chord1, int chord2, int chord3, int mood, int melodynote) 
{  
    // print out the message
    print("Message Received: ");
    println(chord1 + " " + chord2 + " " + chord3 + " " + mood + " " + melodynote);
    moveBalls(melodynote);
}

void moveBalls(int last)
{
  if (last != last_melody_note)
  {
    last_melody_note = last;
    dest_x = int(random(int(width/4), int(width - width/4)));
    dest_y = int(random(int(height/4), height - int(height/4)));
  }
}

void smoothColor(Seeker s, int myhue)
{
  int randnum = int(random(-3, 3));
  if(myhue > hue(s.fillColor))
  {
    float newcolor = randnum + int((myhue-hue(s.fillColor))/64) + hue(s.fillColor);
    s.fillColor = color(newcolor, 180, 255);
  }
  else
  {
    float newcolor = randnum + int((hue(s.fillColor)-myhue)/64) + hue(s.fillColor);
    s.fillColor = color(newcolor, 180, 255);
  }
}







class Seeker{
  PVector position;
  float accelRate, radius;
  PVector velocity = new PVector(0, 0);
  color fillColor;
  float rnd;
    
  public Seeker(PVector pos){
    position = pos;
    rnd = random(1);
    fillColor = color((int) (rnd*255), 180, 255);
  }
  
  public void seek(PVector target){
    accelRate = map(rnd, 0, 1, minAccel, maxAccel);
    target.sub(position);
    target.normalize();
    target.mult(accelRate);
    velocity.add(target);
    velocity.limit(maxVelocity);

    position.add(velocity);
  }
  
  public void render(){
    stroke(color(0,0,0));
    fill(fillColor);
    radius = sq(map(velocity.mag(), 2, maxVelocity*2, 4, 1));
    if(shapeType == 0){
      rect(position.x, position.y, radius, radius);
    }
    else{
      ellipse(position.x, position.y, radius, radius);
    }
  }
}

