long baudRate=1000;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(baudRate);
  pinMode(0,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int val = digitalRead(A0);
  Serial.write(val);
  delay(1000/baudRate);
}
