const int LED = 2;
const int LM35 = A0;
float temperatura;
char comando;

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    comando = (char) Serial.read();
    if (comando == 'L') {
      digitalWrite(LED, HIGH);
    } else if (comando == 'D') {
      digitalWrite(LED, LOW);
    }
  }
  
  temperatura = (float(analogRead(LM35))*5/(1023))/0.01;
  Serial.println(temperatura);
  delay(5000);
}