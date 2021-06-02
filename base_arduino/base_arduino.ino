#include "DHT.h"
#include <SPI.h>                                               // Подключаем библиотеку для работы с шиной SPI.
#include <nRF24L01.h>                                          // Подключаем файл настроек из библиотеки RF24.
#include <RF24.h>                                              // Подключаем библиотеку для работы с nRF24L01+.
RF24     radio(53, 49);                                         // Создаём объект radio для работы с библиотекой RF24, указывая номера выводов модуля (CE, SS).
// список пинов:
#define PIN_RELAY1         2    // LIGHT_BALKON
#define DHTPIN             3    // dht 11 датчик температуры воды в котел
#define DHT22PIN           4    // уличный dht 22
#define PIN_RELAY2         5    // включаем балкон
#define PIN_6          6    //
#define PIN_DHT11_GAZ      7    //Температура воздуха возле вытяжки
#define PIN_RELAY3         8    // LIGHT_TREE
    // ce                  9    // ce
    // csn                 10   // csn


#define PIN_DHT22_TEPLICA  6  // Пин датчика температуры теплицы
#define PIN_RELAY_VIN_KLAPAN  22  // Включение питания для клапанов
#define PIN_RELAY_1_KLAPAN  23  // Управление первым клапаном
#define PIN_RELAY_2_KLAPAN  24  // Управление вторым клапаном
#define PIN_RELAY_3_KLAPAN  25  // Управление третьим клапаном
#define PIN_RELE_5v  26  // Управление реле питания датчиков 5 в


    //mi                   50
    //mo                   51
    //sck                 52
int buzzerPin = 42; //Define buzzerPin

const int analogSignal_MQ135 = A0; //подключение аналогового сигналоьного пина
const int analogSignal_MQ4 = A1; //подключение аналогового сигналоьного пина
const int analogSignal_muve_kitchen = A2; //подключение датчика движения

// список команд с serial port
#define RELE_5v_ON     'H'
#define RELE_5v_OFF     'h'

#define LIGHT_BALKON_ON     'A'
#define LIGHT_BALKON_OFF    'a'

#define LIGHT_TREE_ON       'B'
#define LIGHT_TREE_OFF      'b'

#define LIGHT_PERIM_ON      'C'
#define LIGHT_PERIM_OFF     'c'

#define POLIV_VIN_ON      'D'
#define POLIV_VIN_OFF      'd'

#define POLIV_RELE_1_ON      'E'
#define POLIV_RELE_1_OFF      'e'
#define POLIV_RELE_2_ON      'F'
#define POLIV_RELE_2_OFF      'f'
#define POLIV_RELE_3_ON      'G'
#define POLIV_RELE_3_OFF      'g'

#define SEND_PARAM       'p'   // опрос датчиков ардуино

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
DHT dht22_teplica(PIN_DHT22_TEPLICA, DHTTYPE22);
DHT dht_gaz(PIN_DHT11_GAZ, DHTTYPE);  //Температура воздуха возле вытяжки

int sound = 0;  // sound on/off
int      myData[6] = {0,0,0,0,0,0};
int      ackData[6] = {0,0,0,0,0,0};

int i;
uint32_t myTimer_room; // переменная хранения времени (unsigned long)
uint32_t myTimer_Send_room; // переменная хранения времени (unsigned long)

void setup(){

  pinMode(buzzerPin, OUTPUT); //Set buzzerPin as output


  delay(100); // ждем 0.5секунду
  analogWrite(buzzerPin, 255);
  Serial.begin(9600);


   pinMode(PIN_RELAY_VIN_KLAPAN, OUTPUT); // Объявляем пин реле как выход
   pinMode(PIN_RELAY_1_KLAPAN, OUTPUT); // Объявляем пин реле как выход
   pinMode(PIN_RELAY_2_KLAPAN, OUTPUT); // Объявляем пин реле как выход
   pinMode(PIN_RELAY_3_KLAPAN, OUTPUT); // Объявляем пин реле как выход
   pinMode(PIN_RELE_5v, OUTPUT); // Объявляем пин реле как выход

   digitalWrite(PIN_RELAY_VIN_KLAPAN, HIGH); // Выключаем реле
   digitalWrite(PIN_RELAY_1_KLAPAN, HIGH); // Выключаем реле 1
   digitalWrite(PIN_RELAY_2_KLAPAN, HIGH); // Выключаем реле 2
   digitalWrite(PIN_RELAY_3_KLAPAN, HIGH); // Выключаем реле 3
   digitalWrite(PIN_RELE_5v, LOW); // Выключаем реле питания датчиков 5 в

  pinMode(PIN_RELAY1, OUTPUT); // Объявляем пин реле как выход
  pinMode(PIN_RELAY2, OUTPUT); // Объявляем пин реле как выход
  pinMode(PIN_RELAY3, OUTPUT); // Объявляем пин реле как выход
  digitalWrite(PIN_RELAY1, LOW); // Выключаем реле - посылаем высокий сигнал
  digitalWrite(PIN_RELAY2, HIGH); // Выключаем реле - посылаем высокий сигнал
  digitalWrite(PIN_RELAY3, LOW); // Выключаем реле - посылаем высокий сигнал

  pinMode(analogSignal_MQ135, INPUT); //установка режима пина MQ135
  pinMode(analogSignal_MQ4, INPUT); //установка режима пина MQ4


    radio.begin();                                             // Инициируем работу nRF24L01+.
    if(radio.isPVariant() ){  } // Если модуль поддерживается библиотекой RF24, то выводим текст «nRF24L01».
    else                   {
      analogWrite(buzzerPin, 150);
    delay(100);
    analogWrite(buzzerPin, 255);
    delay(100);
    analogWrite(buzzerPin, 150);
    delay(100);
    analogWrite(buzzerPin, 255);
    } // Иначе, если модуль не поддерживается, то выводи текст «unknown module».

    radio.setChannel      (10);                                // Указываем канал передачи данных (от 0 до 125), 27 - значит приём данных осуществляется на частоте 2,427 ГГц.
    radio.setDataRate     (RF24_250KBPS);                        // Указываем скорость передачи данных (RF24_250KBPS, RF24_1MBPS, RF24_2MBPS), RF24_1MBPS - 1Мбит/сек.
    radio.setPALevel      (RF24_PA_HIGH);                       // Указываем мощность передатчика (RF24_PA_MIN=-18dBm, RF24_PA_LOW=-12dBm, RF24_PA_HIGH=-6dBm, RF24_PA_MAX=0dBm).
    //radio.enableAckPayload();                                   // Указываем что в пакетах подтверждения приёма есть блок с пользовательскими данными.
    radio.openReadingPipe (1, 0xFEDCBA9876LL);
    radio.openWritingPipe (   0xAABBCCDD11LL);
    radio.startListening  ();


}
void(* resetFunc) (void) = 0; // объявляем функцию reset

int s = 0;
void loop(){
    if (millis() - myTimer_room >= 60000*5) {   // ищем разницу за 5 минут
        myTimer_room = millis();              // сброс таймера
        for (i = 0; i < 5; i = i + 1) {
        ackData[i] = 1;
     }

    }
    if (millis() - myTimer_Send_room >= 1000) {   // ищем разницу за 1 c
        myTimer_Send_room = millis();              // сброс таймера
        send_NRF();
    }
  if(radio.available()){
    radio.read( &ackData, sizeof(ackData) );
    myTimer_room = millis();
    //Serial.print("Humidity:");
    //Serial.println(ackData[2]);
    //Serial.print("Temp:");
    //Serial.println(ackData[1]);

  }

    if (sound == 1){
    analogWrite(buzzerPin, s);
    s = s + 1;
    if (s == 255){
      s = 0;
    }
    }
    else{
    analogWrite(buzzerPin, 255);
    }
  char val;
  if (Serial.available()){
    val = Serial.read(); // переменная val равна полученной команде
    if (val == LIGHT_BALKON_OFF) { //  если 0 выключаем реле
      rele_light_balkon(0);    }
    if (val == LIGHT_BALKON_ON){//  если 1 включаем реле
      rele_light_balkon(1);    }
    if (val == LIGHT_TREE_ON){ // управление бойлером Включаем
        rele_light_tree(1);    }
    if (val == LIGHT_TREE_OFF){ // управление бойлером Выключаем
        rele_light_tree(0);    }
    if (val == LIGHT_PERIM_ON){ // управление бойлером Включаем
        rele_light_perim(1);    }
    if (val == LIGHT_PERIM_OFF){ // управление бойлером Выключаем
        rele_light_perim(0);    }

    if (val == SEND_PARAM){ //  если p шлем параметры
      read_dht_param();
    }
    if (val == RESET){ //  если r  перезапускаем Arduino
      resetFunc(); //вызываем reset
    }
    if (val == TEST){
        Serial.println("OK");
    }

    if (val == SOUND_ON){
       sound = 1;
       }
    if (val == SOUND_OFF){
       sound = 0;
       }
    if (val == POLIV_VIN_ON){
       Poliv_on(PIN_RELAY_VIN_KLAPAN);
    }
    if (val == POLIV_VIN_OFF){
       Poliv_off(PIN_RELAY_VIN_KLAPAN);
    }
    if (val == POLIV_RELE_1_ON){
       Poliv_on(PIN_RELAY_1_KLAPAN);
    }
    if (val == POLIV_RELE_1_OFF){
       Poliv_off(PIN_RELAY_1_KLAPAN);
    }
    if (val == POLIV_RELE_2_ON){
       Poliv_on(PIN_RELAY_2_KLAPAN);
    }
    if (val == POLIV_RELE_2_OFF){
       Poliv_off(PIN_RELAY_2_KLAPAN);
    }
    if (val == POLIV_RELE_3_ON){
       Poliv_on(PIN_RELAY_3_KLAPAN);
    }
    if (val == POLIV_RELE_3_OFF){
       Poliv_off(PIN_RELAY_3_KLAPAN);
    }
    if (val == RELE_5v_ON){
       Poliv_on(PIN_RELE_5v);
    }
    if (val == RELE_5v_OFF){
       Poliv_off(PIN_RELE_5v);
    }
  }
}

void rele_light_balkon(int status){
  if (status == 1){
    digitalWrite(PIN_RELAY1, HIGH); // Отключаем реле - посылаем высокий уровень сигнала
    digitalWrite(22, HIGH);

    Serial.println("rele on");
  }
  if (status == 0){
    digitalWrite(PIN_RELAY1, LOW); // Включаем реле - посылаем низкий уровень сигнала
    digitalWrite(22, LOW);

    Serial.println("rele off");
   }
}

void rele_light_perim(int status){
  if (status == 1){
    digitalWrite(PIN_RELAY2, LOW); // Отключаем реле - посылаем высокий уровень сигнала
    Serial.println("rele on");
  }
  if (status == 0){
    digitalWrite(PIN_RELAY2, HIGH); // Включаем реле - посылаем низкий уровень сигнала
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

void send_NRF(){
  if(radio.isPVariant() ){}
  else {
    for (i = 0; i < 5; i = i + 1) {
        myData[i] = 1;
     }
  return;
  }
   myData[0] = 55;
   myData[1] = sound;
   myData[2] = 55;
   myData[3] = 55;

   radio.stopListening  ();
   radio.setChannel      (20);

    if( radio.write(&myData, sizeof(myData)) ){                // Если указанное количество байт массива myData было доставлено приёмнику, то ...
      //  Данные передатчика были корректно приняты приёмником.  // Тут можно указать код который будет выполняться при получении данных приёмником.
      //Serial.println("radio.write - OK send");
      myData[4] = 11;
      myData[5] = 11;
    }else{                                                     // Иначе (если данные не доставлены) ...
      //  Данные передатчика не приняты или дошли с ошибкой CRC. // Тут можно указать код который будет выполняться если приёмника нет или он не получил данные.
      //Serial.println("radio.write - Error send");
      myData[4] = 0;
      myData[5] = 0;
    }
    radio.setChannel      (10);
    radio.startListening  ();
}

void read_dht_param(){  // чтение температуры dh11
  int gasValue = 0; //переменная для хранения количества газа
  float h;
  float t;
  char myStr[5];  // текстовый массив
  String json = "#{";
  dht22.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
  h = dht22.readHumidity();
  t = dht22.readTemperature();
  if (isnan(h)) {
    Serial.print("-street;");
  }
  else {
    json += "'temp_street': ";
    dtostrf(t, 2,2,myStr);
    json += myStr;
    json += ", 'hum_street': ";
    dtostrf(h, 2,2,myStr);
    json += myStr;
    json += ',';
  }
  //dht22_teplica
  dht22_teplica.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
  h = dht22_teplica.readHumidity();
  t = dht22_teplica.readTemperature();
  if (isnan(h)) {
    Serial.print("-teplica;");
  }
  else {
    json += "'temp_teplica': ";
    dtostrf(t, 2,2,myStr);
    json += myStr;
    json += ", 'hum_teplica': ";
    dtostrf(h, 2,2,myStr);
    json += myStr;
    json += ',';
  }
  //
    dht.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
    h = dht.readHumidity();
    t = dht.readTemperature();
    if (isnan(h)) {
        Serial.print("-voda;");
    }
    else {
      json += "'temp_voda': ";
      dtostrf(t, 2,2,myStr);
      json += myStr;
      json += ", 'hum_voda': ";
      dtostrf(h, 2,2,myStr);
      json += myStr;
      json += ',';
    }
  dht_gaz.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
  h = dht_gaz.readHumidity(); //Температура воздуха возле вытяжки
  t = dht_gaz.readTemperature();
  if (isnan(h)) {
        Serial.print("-gaz;");
    }
  else {
    json += "'temp_gaz': ";
    dtostrf(t, 2,2,myStr);
    json += myStr;
    json += ", 'hum_gaz': ";
    dtostrf(h, 2,2,myStr);
    json += myStr;
    json += ',';
  }
    gasValue = analogRead(analogSignal_MQ135); // и о его количестве
    json += "'MQ135': ";
    json += String(gasValue);
    json += ',';
    gasValue = analogRead(analogSignal_MQ4); // и о его количестве
    json += "'MQ4': ";
    json += String(gasValue);
    json += ',';
    json += "'muve_k': ";
    int pirVal = analogRead(analogSignal_muve_kitchen);
    json += pirVal;
    json += ", 'sound': ";
    json += sound;
    json += ", 'temp_room': ";
    json += ackData[1];
    json += ", 'myData': ";
    json += myData[0],myData[1],myData[2],myData[3],myData[4],myData[5];
    json += ", 'askData': ";
    json += ackData[0],ackData[1],ackData[2],ackData[3],ackData[4],ackData[5];
    json += "}";
    Serial.println(json);
}

void Poliv_on(int pin_rele){
    digitalWrite(pin_rele, LOW);
}
void Poliv_off(int pin_rele){
    digitalWrite(pin_rele, HIGH);
}
