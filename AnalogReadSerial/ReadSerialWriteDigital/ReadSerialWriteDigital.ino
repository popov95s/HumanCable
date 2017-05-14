/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Graphical representation is available using serial plotter (Tools > Serial Plotter menu)
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.
*/
/* Baud Rate 115200; 1 byte opening closing sequence; 13 byte message */

long baudRate = 9600;
int qbf[] = {255, 84, 104, 101, 32, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120, 32, 106, 117, 109, 112, 115, 32, 111, 118, 101, 114, 32, 116, 104, 101, 32, 108, 97, 122, 121, 32, 100, 111, 103, 84, 104, 101, 32, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120, 32, 106, 117, 109, 112, 115, 32, 111, 118, 101, 114, 32, 116, 104, 101, 32, 108, 97, 122, 121, 32, 100, 111, 103, 0};
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(baudRate);
  pinMode(5, OUTPUT);
  pinMode(4, INPUT);
}
// the loop routine runs over and over again forever:
void loop() {
  //digitalWrite(5,HIGH);
  
  for(int i=0; i< 45;i++){
      for(int j=0;j<8;j++){
          bool bitToWrite = bitRead(qbf[i],j);
          if(bitToWrite){
              digitalWrite(5,HIGH);
          }
          else{
              digitalWrite(5,LOW);
          }
                  
          byte val = digitalRead(4);
          Serial.write(val);
          delay(1000/baudRate);
      }
  }
   
  //delay(1);
//  if(Serial.available()>0){
//    byte incomingByte=Serial.read();
//
//    for(int i=0; i<8;i++){
//        if(bitRead(incomingByte,i)){
//          digitalWrite(5,HIGH); 
//        }
//        else{
//          digitalWrite(5,LOW);
//        }
//        delay(1);
//    }
//  }
//  delay(1);
//  if(Serial.available()>0){
//    
//    byte incomingByte = Serial.read();
//    
//    Serial.write(incomingByte);
//    for(int i=0; i<8;i++){
//        if(bitRead(incomingByte,i)){
//          digitalWrite(5,HIGH); 
//        }
//        else{
//          digitalWrite(5,LOW);
//        }
//        
//        
//
//    }
//  }
}

