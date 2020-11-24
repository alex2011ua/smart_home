#include <SPI.h>                                               // Подключаем библиотеку для работы с шиной SPI.
#include <nRF24L01.h>                                          // Подключаем файл настроек из библиотеки RF24.
#include <RF24.h>                                              // Подключаем библиотеку для работы с nRF24L01+.
RF24     radio(9, 10);                                         // Создаём объект radio для работы с библиотекой RF24, указывая номера выводов модуля (CE, SS).
int      myData[6];                                            // Объявляем массив для приёма и хранения данных (до 32 байт включительно).
uint8_t  pipe;                                                 // Объявляем переменную в которую будет сохраняться номер трубы по которой приняты данные.
int      rele1;                                                               //
int      ackData;  

void setup(){
  Serial.begin(9600);
  Serial.println("Start Server");
  //
    radio.begin();                                             // Инициируем работу nRF24L01+.
    radio.setChannel      (27);                                // Указываем канал передачи данных (от 0 до 125), 27 - значит приём данных осуществляется на частоте 2,427 ГГц.
    radio.setDataRate     (RF24_250KBPS);                        // Указываем скорость передачи данных (RF24_250KBPS, RF24_1MBPS, RF24_2MBPS), RF24_1MBPS - 1Мбит/сек.
    radio.setPALevel      (RF24_PA_LOW);                       // Указываем мощность передатчика (RF24_PA_MIN=-18dBm, RF24_PA_LOW=-12dBm, RF24_PA_HIGH=-6dBm, RF24_PA_MAX=0dBm).
    radio.enableAckPayload(); 
    radio.openReadingPipe (1, 0xAABBCCDD11LL);                 // Открываем 1 трубу с адресом 1 передатчика 0xAABBCCDD11, для приема данных.
    radio.openReadingPipe (2, 0xAABBCCDD22LL);                 // Открываем 2 трубу с адресом 2 передатчика 0xAABBCCDD22, для приема данных.
    radio.openReadingPipe (3, 0xAABBCCDD33LL);                 // Открываем 3 трубу с адресом 3 передатчика 0xAABBCCDD33, для приема данных.
    radio.openReadingPipe (4, 0xAABBCCDD96LL);                 // Открываем 4 трубу с адресом 4 передатчика 0xAABBCCDD96, для приема данных.
    radio.openReadingPipe (5, 0xAABBCCDDFFLL);                 // Открываем 5 трубу с адресом 5 передатчика 0xAABBCCDDFF, для приема данных.
    //radio.enableDynamicPayloads();
    radio.startListening  ();                                  // Включаем приемник, начинаем прослушивать открытые трубы.

}                                                              //
                                                               //
void loop(){ 
  char val;

  if (Serial.available()){
     
    val = Serial.read(); // переменная val равна полученной команде
    Serial.println(val);
    
    if (val == '0') { //  если 0 выключаем реле
      ackData = 13;  
      
      
    }
    if (val == '1'){//  если 1 включаем реле
      ackData = 12;
      
    }
  radio.writeAckPayload (1, &ackData, sizeof(ackData) );
  }
  

  //
    if(radio.available(&pipe)){                                // Если в буфере имеются принятые данные, то получаем номер трубы по которой эти данные пришли в переменную pipe.
        radio.read( &myData, sizeof(myData) );                 // Читаем данные из буфера в массив myData указывая сколько всего байт может поместиться в массив.
        
        if(pipe==1){
          
          /* Данные пришли по 1 трубе */
          Serial.print(myData[0]);
          Serial.print("  ");
          Serial.print(myData[1]);
          Serial.print(" ");
          Serial.print(myData[2]);
          Serial.print(" ");
          Serial.println(myData[3]);
          Serial.println("ack1");
          Serial.println(myData[4]);
          Serial.print("ackData - ");
          Serial.println(ackData);

          
        }                                                      // Если данные пришли от 1 передатчика (по 1 трубе), то можно выполнить соответствующее действие ...
        if(pipe==2){ /* Данные пришли по 2 трубе */ ;}         // Если данные пришли от 2 передатчика (по 2 трубе), то можно выполнить соответствующее действие ...
        if(pipe==3){ /* Данные пришли по 3 трубе */ ;}         // Если данные пришли от 3 передатчика (по 3 трубе), то можно выполнить соответствующее действие ...
        if(pipe==4){ /* Данные пришли по 4 трубе */ ;}         // Если данные пришли от 4 передатчика (по 4 трубе), то можно выполнить соответствующее действие ...
    }                                                          //
}
