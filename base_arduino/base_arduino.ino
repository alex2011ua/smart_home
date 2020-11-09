#include "DHT.h"
#define DHTPIN 3     // к какому пину будет подключен вывод Data dht 11
#define PIN_RELAY 2 // Определяем пин, используемый для подключения реле
#define DHT22PIN 4
//выбор используемого датчика
#define DHTTYPE DHT11   // DHT 11 
#define DHTTYPE22 DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

#define RELE_ON '1'
#define RELE_OFF '0'
#define SEND_DATA_TEMP '2'
#define SEND_DATA_TEMP22 '3'
#define RESET '9'
#define TEST 't'

int led = 13; // led   как пин 13
//инициализация датчика
DHT dht(DHTPIN, DHTTYPE);
DHT dht22(DHT22PIN, DHTTYPE22);


void setup(){
  delay(10000); // ждем секунду
  Serial.begin(9600);
  pinMode(PIN_RELAY, OUTPUT); // Объявляем пин реле как выход
  digitalWrite(PIN_RELAY, HIGH); // Выключаем реле - посылаем высокий сигнал
  pinMode(led, OUTPUT); // объявляем пин 13 как выход
}

void(* resetFunc) (void) = 0; // объявляем функцию reset

void send_data_to_pi(){  // чтение температуры dh11
  dht.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(t) ||  ( isnan(h)) ){
    Serial.println("Error_reading_from_DHT");
  }
  else {
  Serial.print("Humidity:");
  Serial.print(h);
  Serial.print(":");
  Serial.print("Temperature:");
  Serial.println(t);
  }
}

void send_temp22_to_pi(){  // чтение температуры dh22
  dht22.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(t) ||  ( isnan(h)) ){
    Serial.println("Error_reading_from_DHT22");
  }
  else {
  Serial.print("Humidity:");
  Serial.print(h);
  Serial.print(":");
  Serial.print("Temperature:");
  Serial.println(t);
  }
}

void rele(int status){
  if (status == 1){
    digitalWrite(PIN_RELAY, HIGH); // Отключаем реле - посылаем высокий уровень сигнала
    Serial.println("rele on");
    digitalWrite(led, HIGH);        // при 1 включаем светодиод
  }
  if (status == 0){
    digitalWrite(PIN_RELAY, LOW); // Включаем реле - посылаем низкий уровень сигнала
    Serial.println("rele off");
    digitalWrite(led, LOW);       // при 0 выключаем светодиод
  }
}

void loop(){
  char val;
  if (Serial.available()){
    val = Serial.read(); // переменная val равна полученной команде
    if (val == RELE_OFF) {
      rele(0);
    }
    if (val == RELE_ON){
      rele(1);
    }
    if (val == SEND_DATA_TEMP){
      send_data_to_pi();
    } // при 2 посылаем данные в raspbery
    if (val == SEND_DATA_TEMP22){
      send_temp22_to_pi();
    } // при 2 посылаем данные в raspbery
    if (val == RESET){
      Serial.println("get data");
      resetFunc(); //вызываем reset
    } // при 9 вызываем reset
    if (val == TEST){  // при t  возврат OK
        digitalWrite(led, HIGH);
        delay(10);
        digitalWrite(led, LOW);
        Serial.println("OK");
    }
  }
}