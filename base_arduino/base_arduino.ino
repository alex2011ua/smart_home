#include "DHT.h"
// список пинов:
#define PIN_RELAY1         2    // LIGHT_BALKON
#define DHTPIN             3    // dht 11 датчик температуры воды в котел
#define DHT22PIN           4    // уличный dht 22
#define PIN_RELAY2         5    // LIGHT_PERIM
#define PIN_SOUND          6    // пищалка
#define PIN_DHT11_GAZ      7    //Температура воздуха возле вытяжки
#define PIN_RELAY3         8    // LIGHT_TREE
    // ce                  9    // ce
    // csn                 10   // csn
    //mi                   11
    //mo                   12

const int analogSignal_MQ135 = A0; //подключение аналогового сигналоьного пина
const int analogSignal_MQ4 = A1; //подключение аналогового сигналоьного пина


// список команд с serial port
#define LIGHT_BALKON_ON     'A'
#define LIGHT_BALKON_OFF    'a'

#define LIGHT_TREE_ON       'B'
#define LIGHT_TREE_OFF      'b'

#define LIGHT_PERIM_ON      'C'
#define LIGHT_PERIM_OFF     'c'

#define SEND_PARAM       'p'
#define RESET            'r'
#define TEST             't'

#define SOUND_ON         'S'
#define SOUND_OFF        's'

//выбор используемого датчика
#define DHTTYPE DHT11   // DHT 11
#define DHTTYPE22 DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)
//инициализация датчика
DHT dht(DHTPIN, DHTTYPE);
DHT dht22(DHT22PIN, DHTTYPE22);
DHT dht_gaz(PIN_DHT11_GAZ, DHTTYPE);  //Температура воздуха возле вытяжки

void setup(){
  delay(1000); // ждем 1 секунду
  Serial.begin(9600);

  pinMode(PIN_RELAY1, OUTPUT); // Объявляем пин реле как выход
  pinMode(PIN_RELAY2, OUTPUT); // Объявляем пин реле как выход
  pinMode(PIN_RELAY3, OUTPUT); // Объявляем пин реле как выход
  digitalWrite(PIN_RELAY1, LOW); // Выключаем реле - посылаем высокий сигнал
  digitalWrite(PIN_RELAY2, LOW); // Выключаем реле - посылаем высокий сигнал
  digitalWrite(PIN_RELAY3, LOW); // Выключаем реле - посылаем высокий сигнал
  pinMode(PIN_SOUND, OUTPUT);

  pinMode(analogSignal_MQ135, INPUT); //установка режима пина MQ135
  pinMode(analogSignal_MQ4, INPUT); //установка режима пина MQ4

}

void(* resetFunc) (void) = 0; // объявляем функцию reset

void read_dht_param(){  // чтение температуры dh11

  int gasValue = 0; //переменная для хранения количества газа
  float h;
  float t;
  char myStr[5];  // текстовый массив
  String json = "#{";
  dht22.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
  h = dht22.readHumidity();
  t = dht22.readTemperature();
  if (isnan(h) || isnan(t) ) {
    Serial.print(";street; ");
  }
  else {
    json += "'temp_street': ";
    dtostrf(t, 2,2,myStr);
    json += myStr;
    json += ", 'humidity_street': ";
    dtostrf(h, 2,2,myStr);
    json += myStr;
    json += ',';
  }
    dht.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
    h = dht.readHumidity();
    t = dht.readTemperature();
    if (isnan(h) || isnan(t)) {
        Serial.print(";voda; ");
    }
    else {
      json += "'temp_voda': ";
      dtostrf(t, 2,2,myStr);
      json += myStr;
      json += ", 'humidity_voda': ";
      dtostrf(h, 2,2,myStr);
      json += myStr;
      json += ',';
    }
  dht_gaz.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
  h = dht_gaz.readHumidity(); //Температура воздуха возле вытяжки
  t = dht_gaz.readTemperature();
  if (isnan(h) || isnan(t)) {
        Serial.print(";gaz; ");
    }
  else {
    json += "'temp_gaz': ";
    dtostrf(t, 2,2,myStr);
    json += myStr;
    json += ", 'humidity_gaz': ";
    dtostrf(h, 2,2,myStr);
    json += myStr;
    json += ',';
  }
    gasValue = analogRead(analogSignal_MQ135); // и о его количестве
    json += "'MQ135_value': ";
    json += String(gasValue);
    json += ',';
    gasValue = analogRead(analogSignal_MQ4); // и о его количестве
    json += "'MQ4_value': ";
    json += String(gasValue);
    json += "}";
    Serial.println(json);
}
void loop(){
  char val;
  if (Serial.available()){
    val = Serial.read(); // переменная val равна полученной команде
    if (val == LIGHT_BALKON_OFF) { //  если 0 выключаем реле
      rele_light_balkon(0);
    }
    if (val == LIGHT_BALKON_ON){//  если 1 включаем реле
      rele_light_balkon(1);
    }
    if (val == LIGHT_TREE_ON){ // управление бойлером Включаем
        rele_light_tree(1);
    }
    if (val == LIGHT_TREE_OFF){ // управление бойлером Выключаем
        rele_light_tree(0);
    }
    if (val == LIGHT_PERIM_ON){ // управление бойлером Включаем
        rele_light_perim(1);
    }
    if (val == LIGHT_PERIM_OFF){ // управление бойлером Выключаем
        rele_light_perim(0);
    }

    if (val == SEND_PARAM){ //  если p шлем параметры
      read_dht_param();
    }
    if (val == RESET){ //  если r  перезапускаем Arduino
      resetFunc(); //вызываем reset
    }
    if (val == TEST){  // при  t 6 раз мигнем диодом возврат OK
        Test();
    }

    if (val == SOUND_ON){ // управление бойлером Включаем
        Sound(1);
    }
    if (val == SOUND_OFF){ // управление бойлером Выключаем
        Sound(0);
    }
  }
}


void Sound(int status){
  if (status == 1){
    analogWrite(PIN_SOUND, 50); // включаем пьезоизлучатель
    Serial.println("Sound on");
  }
  if (status == 0){
    analogWrite(PIN_SOUND, 0); // выключаем звук
    Serial.println("Sound off");
  }
}


void Test(){  // во время теста 6 раз мигнем светодиодом
    Serial.println("OK");
}


void rele_light_balkon(int status){
  if (status == 1){
    digitalWrite(PIN_RELAY1, HIGH); // Отключаем реле - посылаем высокий уровень сигнала
    Serial.println("rele on");
  }
  if (status == 0){
    digitalWrite(PIN_RELAY1, LOW); // Включаем реле - посылаем низкий уровень сигнала
    Serial.println("rele off");
   }
}


void rele_light_perim(int status){
  if (status == 1){
    digitalWrite(PIN_RELAY2, HIGH); // Отключаем реле - посылаем высокий уровень сигнала
    Serial.println("rele on");
  }
  if (status == 0){
    digitalWrite(PIN_RELAY2, LOW); // Включаем реле - посылаем низкий уровень сигнала
    Serial.println("rele off");
   }
}


void rele_light_tree(int status){ //управление бойлером
    if (status == 1){
    digitalWrite(PIN_RELAY3, HIGH); // Отключаем реле - посылаем высокий уровень сигнала
    Serial.println("rele on");
  }
  if (status == 0){
    digitalWrite(PIN_RELAY3, LOW); // Включаем реле - посылаем низкий уровень сигнала
    Serial.println("rele off");
    }
}
