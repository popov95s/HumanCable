/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Graphical representation is available using serial plotter (Tools > Serial Plotter menu)
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.
*/
/* Baud Rate 115200; 1 byte opening closing sequence; 13 byte message */

int baudRate = 38400;
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(baudRate);
  pinMode(5, OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  if(Serial.available()>0){
    int incomingByte = Serial.read();
    for(int i=0; i<8;i++){
        
        if(bitRead(incomingByte,i) == 0){
          digitalWrite(5,HIGH); 
        }
        else{
          digitalWrite(5,LOW);
        }
        
        delay(1/baudRate);
    }
  }
}

