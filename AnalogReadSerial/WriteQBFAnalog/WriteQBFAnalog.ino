
int qbf[] = {255, 84, 104, 101, 32, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120, 32, 106, 117, 109, 112, 115, 32, 111, 118, 101, 114, 32, 116, 104, 101, 32, 108, 97, 122, 121, 32, 100, 111, 103, 84, 104, 101, 32, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120, 32, 106, 117, 109, 112, 115, 32, 111, 118, 101, 114, 32, 116, 104, 101, 32, 108, 97, 122, 121, 32, 100, 111, 103, 0};
long baudRate=1000;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(baudRate);
  pinMode(5,OUTPUT);
}

void loop() {
  for(int i=0;i<45;i++){
    for(int j=0;j<8;j++){
      bool bitToWrite= bitRead(qbf[i],j);
      if(bitToWrite){
        digitalWrite(5,HIGH);
      }
      else{
        digitalWrite(5,LOW);
      }
      delay(1000/baudRate);
    }
  }
}
