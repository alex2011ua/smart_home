#include "DHT.h"
#define DHTPIN 3     // к какому пину будет подключен вывод Data
#define PIN_RELAY 2 // Определяем пин, используемый для подключения реле
//выбор используемого датчика
#define DHTTYPE DHT11   // DHT 11 
//#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

#define RELE_ON '1'
#define RELE_OFF '0'
#define SEND_DATA_TEMP '2'

//инициализация датчика
DHT dht(DHTPIN, DHTTYPE);

void setup(){
  Serial.begin(9600);
  pinMode(PIN_RELAY, OUTPUT); // Объявляем пин реле как выход
  digitalWrite(PIN_RELAY, HIGH); // Выключаем реле - посылаем высокий сигнал
  pinMode(13, OUTPUT); // объявляем пин 13 как выход
}
float temp(){
  // чтение температуры и влажности займет примерно 250 миллисекунд
  dht.begin();
  float t = dht.readTemperature();
  // проверяем правильные ли данные получили
  if (isnan(t) ){
    Serial.println("Error_reading_from_DHT;");
  } else {
    return t;
  }
}

float Humidity() {
  // чтение температуры и влажности займет примерно 250 миллисекунд
  dht.begin();
  float h = dht.readHumidity();
  // проверяем правильные ли данные получили
  if ( isnan(h)) {
    Serial.println("Error_reading_from_DHT;");
  } 
  else {
    return h;
  }
}

void rele(int status){
  if (status == 0){
    digitalWrite(PIN_RELAY, HIGH); // Отключаем реле - посылаем высокий уровень сигнала

  }
  if (status == 1){
    digitalWrite(PIN_RELAY, LOW); // Включаем реле - посылаем низкий уровень сигнала
  }
}

void send_data_to_pi(){
  float tt;
  float hh;
  tt = temp();
  hh = Humidity();
  Serial.print("Humidity:");
  Serial.print(hh);
  Serial.print(":");
  Serial.print("Temperature:");
  Serial.print(tt);
}
void loop(){
  char val;
  if (Serial.available()){
    val = Serial.read(); // переменная val равна полученной команде
    if (val == RELE_OFF) {
      Serial.println("rele off");
      digitalWrite(13, HIGH);
      rele(1);
    } // при 1 включаем светодиод
    if (val == RELE_ON){
      Serial.println("rele on");
      digitalWrite(13, LOW);
      rele(0);
    } // при 0 выключаем светодиод
    if (val == SEND_DATA_TEMP){
      Serial.println("get data");
      send_data_to_pi();
    } // при 2 посылаем данные в raspbery
  }
}
