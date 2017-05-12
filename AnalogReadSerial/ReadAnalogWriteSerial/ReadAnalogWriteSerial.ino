int baudRate = 38400;
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(baudRate);
  pinMode(1, INPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  
    int sensorValue = analogRead(A1); 
    
    Serial.write(map(sensorValue, 0, 1024, 0, 255));
    delay(1/baudRate);
}
