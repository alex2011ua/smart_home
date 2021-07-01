#include "DHT.h"
// список пинов:


#define DHTPIN             3   // dht 11 датчик температуры воды в котел
#define DHT22PIN           4   // уличный dht 22
#define PIN_RELAY_BOILER   5 // реле включения бойлера
#define PIN_SOUND          6   // пищалка
#define PIN_DHT11_GAZ      7   //Температура воздуха возле вытяжки
#define MQ135              8      //  MQ-135
#define PIN_RELAY          9   // реле перезагрузки камер
#define SOUND              10      //  Пищалка
#define MQ4                11      //  MQ-4

const int analogSignal_MQ135 = A0; //подключение аналогового сигналоьного пина
const int analogSignal_MQ4 = A1; //подключение аналогового сигналоьного пина





int led = 13; // led как пин 13

// список команд с serial port
#define RELE_OFF    '0'
#define RELE_ON     '1'

#define SEND_PARAM  'p'

#define RESET       'r'
#define TEST        't'

#define BOILER_ON   'B'
#define BOILER_OFF  'b'

#define SOUND_ON    'S'
#define SOUND_OFF   's'

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
  pinMode(PIN_RELAY, OUTPUT); // Объявляем пин реле как выход
  pinMode(PIN_RELAY_BOILER, OUTPUT);
  digitalWrite(PIN_RELAY, HIGH); // Выключаем реле - посылаем высокий сигнал
  digitalWrite(PIN_RELAY_BOILER, HIGH);
  pinMode(PIN_SOUND, OUTPUT);
  pinMode(led, OUTPUT); // объявляем пин 13 как выход
  pinMode(analogSignal_MQ135, INPUT); //установка режима пина MQ135
  pinMode(analogSignal_MQ4, INPUT); //установка режима пина MQ4

}

void(* resetFunc) (void) = 0; // объявляем функцию reset

void read_dht_param(){  // чтение температуры dh11
    boolean noGas; //переменная для хранения значения о присутствии газа
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
    noGas = digitalRead(MQ135); //считываем значение о присутствии газа
    gasValue = analogRead(analogSignal_MQ135); // и о его количестве
    json += "'MQ135': ";
    if (noGas) {
    json += "false,";
    }
    else{
    json += "true,";
    }
    json += "'MQ135_value': ";
    json += String(gasValue);
    json += ',';

    noGas = digitalRead(MQ4); //считываем значение о присутствии газа
    gasValue = analogRead(analogSignal_MQ4); // и о его количестве
    json += "'MQ4': ";
    if (noGas) {
    json += "false,";
    }
    else{
    json += "true,";
    }
    json += "'MQ4_value': ";
    json += String(gasValue);

    json += "}";
    Serial.println(json);
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
    if (val == SEND_PARAM){ //  если P шлем параметры
      read_dht_param();
    }
    if (val == RESET){ //  если r  перезапускаем Arduino

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


void rele(int status){
  if (status == 1){
    digitalWrite(PIN_RELAY, LOW); // Отключаем реле - посылаем высокий уровень сигнала
    Serial.println("rele on");
  }
  if (status == 0){
    digitalWrite(PIN_RELAY, HIGH); // Включаем реле - посылаем низкий уровень сигнала
    Serial.println("rele off");
   }
}

void Boiler(int status){ //управление бойлером
    if (status == 1){
    digitalWrite(PIN_RELAY_BOILER, LOW); // Отключаем реле - посылаем высокий уровень сигнала
    Serial.println("bouiler on");
  }
  if (status == 0){
    digitalWrite(PIN_RELAY_BOILER, HIGH); // Включаем реле - посылаем низкий уровень сигнала
    Serial.println("boiler off");
    }
}
