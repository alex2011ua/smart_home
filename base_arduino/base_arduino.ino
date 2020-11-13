#include "DHT.h"
// список пинов:

#define PIN_RELAY 2 // Определяем пин, используемый для подключения реле
#define DHTPIN 3     // к какому пину будет подключен вывод Data dht 11
#define DHT22PIN 4 // уличный dht 22
#define PIN_RELAY_BOILER  5 // реле включения бойлера



int led = 13; // led как пин 13

// список команд с serial port
#define RELE_OFF '0'
#define RELE_ON '1'
#define SEND_DATA_TEMP '2'
#define SEND_DATA_TEMP22 '3'
#define RESET 'r'
#define TEST 't'
#define BOILER_ON 'B'
#define BOILER_OFF 'b'



//выбор используемого датчика
#define DHTTYPE DHT11   // DHT 11 
#define DHTTYPE22 DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)
//инициализация датчика
DHT dht(DHTPIN, DHTTYPE);
DHT dht22(DHT22PIN, DHTTYPE22);
int temp_street = 0;
int temp_podval = 1;


void setup(){
  delay(1000); // ждем 1 секунду
  Serial.begin(9600);
  pinMode(PIN_RELAY, OUTPUT); // Объявляем пин реле как выход
  pinMode(PIN_RELAY_BOILER, OUTPUT);
  digitalWrite(PIN_RELAY, LOW); // Выключаем реле - посылаем высокий сигнал
  digitalWrite(PIN_RELAY_BOILER, LOW);
  pinMode(led, OUTPUT); // объявляем пин 13 как выход
}

void(* resetFunc) (void) = 0; // объявляем функцию reset

void read_dht_param(int place){  // чтение температуры dh11
  float h;
  float t;
  if (place == 0){
        dht22.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
        h = dht22.readHumidity();
        t = dht22.readTemperature();
  }
  if (place == 1){
        dht.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
        h = dht.readHumidity();
        t = dht.readTemperature();
  }
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

void Test(){  // во время теста 6 раз мигнем светодиодом
    for (int i = 0; i < 6; i++) {
        digitalWrite(led, HIGH);
        delay(400);
        digitalWrite(led, LOW);
        delay(400);
        digitalWrite(led, HIGH);
        delay(400);
        digitalWrite(led, LOW);
    }
    Serial.println("OK");
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

void Boiler(int status){ //управление бойлером
    if (status == 1){
    digitalWrite(PIN_RELAY_BOILER, HIGH); // Отключаем реле - посылаем высокий уровень сигнала
    Serial.println("bouiler on");
  }
  if (status == 0){
    digitalWrite(PIN_RELAY_BOILER, LOW); // Включаем реле - посылаем низкий уровень сигнала
    Serial.println("boiler off");
}

void loop(){
  char val;
  if (Serial.available()){
    val = Serial.read(); // переменная val равна полученной команде
    if (val == RELE_OFF) { //  если 0 выключаем реле
      rele(0);
    }
    if (val == RELE_ON){//  если 1 включаем реле
      rele(1);
    }
    if (val == SEND_DATA_TEMP){ //  если 2 смотрим домашний датчик
      read_dht_param(temp_podval);
    }
    if (val == SEND_DATA_TEMP22){ //  если 3 смотрим уличный датчик
      read_dht_param(temp_street);
    }
    if (val == RESET){ //  если r  перезапускаем Arduino
      Serial.println("get data");
      resetFunc(); //вызываем reset
    }
    if (val == TEST){  // при  t 6 раз мигнем диодом возврат OK
        Test();
    }
    if (val == BOILER_ON){ // управление бойлером Включаем
        Boiler(1);
    }
    if (val == BOILER_OFF){ // управление бойлером Выключаем
        Boiler(0);
    }
  }
}
