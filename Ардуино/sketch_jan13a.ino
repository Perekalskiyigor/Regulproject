int PUL = 5;
int DIR = 6;
int ENA = 7;

void setup() {
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(ENA, OUTPUT);

  digitalWrite(ENA, LOW); // Enable the motor
  digitalWrite(DIR, LOW); // Set direction (LOW or HIGH)
}

void loop() {
  digitalWrite(PUL, HIGH);
  delayMicroseconds(200);
  digitalWrite(PUL, LOW);
  delayMicroseconds(200);
}
