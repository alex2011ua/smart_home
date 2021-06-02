
#include "DHT.h"
#include <SPI.h>                                               // Подключаем библиотеку для работы с шиной SPI.
#include <nRF24L01.h>                                          // Подключаем файл настроек из библиотеки RF24.
#include <RF24.h>                                              // Подключаем библиотеку для работы с nRF24L01+.

#define DHTPIN             4    // dht 11 датчик температуры воды в котел
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);
RF24     radio(9, 10);                                         // Создаём объект radio для работы с библиотекой RF24, указывая номера выводов модуля (CE, SS).
int      myData[6] = {11,11,11,11,11,11};                                            // Объявляем массив для приёма и хранения данных (до 32+2 байт включительно).
int      ackData[6] = {11,11,11,11,11,11};;
int buzzerPin = 3; //Define buzzerPin

uint8_t  i;
unsigned long millissenddata=0; 

void setup(){
  //
  Serial.begin(9600);
    pinMode(buzzerPin, OUTPUT); //Set buzzerPin as output
    analogWrite(buzzerPin, 255);
    Serial.begin(9600);
    
    radio.begin           ();                                  // Инициируем работу модуля nRF24L01+.
    if(radio.isPVariant() ){ Serial.print("nRF24L01"      ); } // Если модуль поддерживается библиотекой RF24, то выводим текст «nRF24L01».
    else                   { 
      analogWrite(buzzerPin, 150);
    delay(100);
    analogWrite(buzzerPin, 255);
    delay(100);
    analogWrite(buzzerPin, 150);
    delay(100);
    analogWrite(buzzerPin, 255); 
    } // Иначе, если модуль не поддерживается, то выводи текст «unknown module».
                             Serial.print("\r\n"          );   //
    radio.setChannel      (20);                                // Указываем канал передачи данных (от 0 до 125), 27 - значит передача данных осуществляется на частоте 2,427 ГГц.
i = radio.getChannel(); // Получить номер используемого канала в переменную i
    Serial.println(i);
    radio.setDataRate     (RF24_250KBPS);                        // Указываем скорость передачи данных (RF24_250KBPS, RF24_1MBPS, RF24_2MBPS), RF24_1MBPS - 1Мбит/сек.
    radio.setPALevel      (RF24_PA_HIGH);                       // Указываем мощность передатчика (RF24_PA_MIN=-18dBm, RF24_PA_LOW=-12dBm, RF24_PA_HIGH=-6dBm, RF24_PA_MAX=0dBm).
                                                      
//    radio.enableAckPayload();                                  // Указываем что в пакетах подтверждения приёма есть блок с пользовательскими данными.
//  radio.enableDynamicPayloads();                             // Разрешить динамически изменяемый размер блока данных на всех трубах.
    radio.openReadingPipe (1, 0xAABBCCDD11LL);                 // Открываем 1 трубу с адресом 0xAABBCCDD11, для приема данных.
    radio.openWritingPipe (   0xFEDCBA9876LL);
    radio.startListening  ();                                  // Включаем приемник, начинаем прослушивать открытые трубы.
//    radio.writeAckPayload (1, &ackData, sizeof(ackData) );     // Помещаем данные всего массива ackData в буфер FIFO. Как только будут получены любые данные от передатчика на 1 трубе, то данные из буфера FIFO будут отправлены этому передатчику вместе с пакетом подтверждения приёма его данных.
}                                                              // В модуле имеется 3 буфера FIFO, значит в них одновременно может находиться до трёх разных или одинаковых данных для ответа по одной или разным трубам.
int s = 0;
int sound = 0;                                                     // После отправки данных из буфера FIFO к передатчику, соответствующий буфер очищается и способен принять новые данные для отправки.
void loop(){                                                   //
    if(radio.available()){  
  Serial.println("available");
        radio.read            (   &ackData,  sizeof(ackData)  ); // Читаем данные из буфера приёма в массив myData указывая сколько всего байт может поместиться в массив.
        // radio.writeAckPayload (1, &ackData, sizeof(ackData) ); // Помещаем данные всего массива ackData в буфер FIFO для их отправки на следующее получение данных от передатчика на 1 трубе.
    Serial.print( ackData[0]);
   Serial.print( ackData[1]);
   Serial.print( ackData[2]);
   Serial.print( ackData[3]);
   Serial.print( ackData[4]);
   Serial.println( ackData[5]);      
    }                                                          // Если все 3 буфера FIFO уже заполнены, то функция writeAckPayload() будет проигнорирована.
                                                       // Так как в данном скетче данные в буфер помещаются только после получения данных от передатчика, значит один из буферов был только что очищен и заполнение всех 3 буферов в данном скетче невозможно.
    if (ackData[0] == 55 && ackData[2] == 55 && ackData[3] == 55){
        sound = ackData[1];
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
  if(millis()-millissenddata>60000) { //раз в минуту
    send_pir();
    millissenddata=millis();
  }
}

void send_pir(){
  radio.stopListening  ();  
  radio.setChannel      (10); 
 i = radio.getChannel(); // Получить номер используемого канала в переменную i
    Serial.println(i);
    dht.begin(); // чтение температуры и влажности займет примерно 250 миллисекунд
    float h;
    float t;
    h = dht.readHumidity();
    t = dht.readTemperature();
    if (isnan(h)) {
        Serial.print(";voda; ");
    }
    else {
      Serial.print("Humidity:");
      Serial.println(int(h));
      Serial.print("Temp:");
      Serial.println(t);
      myData[1] = int(t);
      myData[2] = int(h);
    }
  if (radio.write(&myData, sizeof(myData)) ){
    Serial.println("Send OK");
    
  }else{
    Serial.println("Send ERROR");
    
  };
  radio.setChannel      (20);
i = radio.getChannel(); // Получить номер используемого канала в переменную i
    Serial.println(i);
  radio.startListening  ();
}
