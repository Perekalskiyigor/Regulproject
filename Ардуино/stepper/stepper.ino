
//https://ampermarket.kz/base/ex40-nema17-tb6600/

//Шаговый двигатель NEMA17 и драйвер TB6600s

int PUL=5;
int DIR=6;
int ENA=7;
int freq = 500;
  
void setup() {
  pinMode (PUL, OUTPUT);
  pinMode (DIR, OUTPUT);
  pinMode (ENA, OUTPUT);
  Serial.begin(9600);
 
}
 
void loop() {

  for (int i=0; i<1000; i++)    // Вперед на 5000 шагов
  {
    digitalWrite(DIR,LOW);
    digitalWrite(ENA,HIGH);
    digitalWrite(PUL,HIGH);
    delayMicroseconds(freq);
    digitalWrite(PUL,LOW);
    delayMicroseconds(freq);
   Serial.print("rotate right ");
   Serial.println(i);
  }
  for (int i=0; i<1000; i++)   // Назад на 5000 шагов
  {
    digitalWrite(DIR,HIGH);
    digitalWrite(ENA,HIGH);
    digitalWrite(PUL,HIGH);
    delayMicroseconds(freq);
    digitalWrite(PUL,LOW);
    delayMicroseconds(freq);
    Serial.print("rotate left");
    Serial.println(i);
  }
}
