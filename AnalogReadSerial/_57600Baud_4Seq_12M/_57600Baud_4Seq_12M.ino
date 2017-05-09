/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Graphical representation is available using serial plotter (Tools > Serial Plotter menu)
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.
*/
/* Baud Rate 57600; 4 byte opening closing sequence; 13 byte message */
int asciiDecimal[] = {255, 255, 255, 72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100, 10, 0, 0, 0, 0};
int indexOfSendStr = 0;
int indexOfSendBits = 0;
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(57600);
  pinMode(5, OUTPUT);
  pinMode(1, INPUT);


}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A1);
  // Serial.println("Read bit: ");
  Serial.write(map(sensorValue, 0, 1024, 0, 255));
  if (indexOfSendStr == 20) {
    indexOfSendStr = 0;
    indexOfSendBits = 0;
  }
  else if (indexOfSendBits == 8) {
    indexOfSendStr++;
    indexOfSendBits = 0;
  }

  bool bitToWrite = bitRead(asciiDecimal[indexOfSendStr], indexOfSendBits);
  if (bitToWrite) {
    analogWrite(5, 255);
  }
  else {
    analogWrite(5, 0);
  }
  // Serial.print("Wrote bit: ");
  // Serial.println(bitToWrite);
  indexOfSendBits++;

  delay(1);        // delay in between reads for stability
}

