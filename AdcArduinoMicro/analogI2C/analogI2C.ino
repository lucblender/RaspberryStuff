#include <Wire.h>


int analogPins[12] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11}; 
int i = 0;
int val = 0; 

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);           //  setup serial
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
}

void loop() {
  val++;
  delay(200);
  if(val == 10000)
  {
    val = 0;
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(100);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  }
}

void receiveEvent(int count) {
  if(count >= 2){
      //Flush stream
    while(Wire.available()){
      Wire.read();
    }
  }
}
void requestEvent()
{

  uint8_t reg = Wire.read();
  
  uint16_t toSend = analogRead(analogPins[reg]);

  Serial.println(toSend);
  
  uint8_t msb = toSend>>8;
  uint8_t lsb = toSend;

  
  Serial.println(msb);
  
  Serial.println(lsb);
  
  if(reg<12)
  {
      Wire.write(lsb);
      Wire.write(msb);
      delay(3);
  }
      
  //Flush stream
  while(Wire.available()){
    reg = Wire.read();       
  }
    
}
