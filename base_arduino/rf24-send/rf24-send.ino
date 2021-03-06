#include <SPI.h>                                               // Подключаем библиотеку для работы с шиной SPI.
#include <nRF24L01.h>                                          // Подключаем файл настроек из библиотеки RF24.
#include <RF24.h>                                              // Подключаем библиотеку для работы с nRF24L01+.
RF24     radio(9, 10);                                         // Создаём объект radio для работы с библиотекой RF24, указывая номера выводов модуля (CE, SS).
int      myData[6] = {11,12,13,14,15,16};                                            // Объявляем массив для приёма и хранения данных (до 32+2 байт включительно).
int      ackData[6]= {11,12,13,14,15,16}; 


void setup(){
  //
    
    Serial.begin(9600);
    
    radio.begin           ();                                  // Инициируем работу модуля nRF24L01+.
    radio.setChannel      (27);                                // Указываем канал передачи данных (от 0 до 125), 27 - значит передача данных осуществляется на частоте 2,427 ГГц.
    radio.setDataRate     (RF24_250KBPS);                        // Указываем скорость передачи данных (RF24_250KBPS, RF24_1MBPS, RF24_2MBPS), RF24_1MBPS - 1Мбит/сек.
    radio.setPALevel      (RF24_PA_LOW);                       // Указываем мощность передатчика (RF24_PA_MIN=-18dBm, RF24_PA_LOW=-12dBm, RF24_PA_HIGH=-6dBm, RF24_PA_MAX=0dBm).
                                                      
    radio.enableAckPayload();                                  // Указываем что в пакетах подтверждения приёма есть блок с пользовательскими данными.
//  radio.enableDynamicPayloads();                             // Разрешить динамически изменяемый размер блока данных на всех трубах.
    radio.openReadingPipe (1, 0xAABBCCDD11LL);                 // Открываем 1 трубу с адресом 0xAABBCCDD11, для приема данных.
    radio.startListening  ();                                  // Включаем приемник, начинаем прослушивать открытые трубы.
    radio.writeAckPayload (1, &ackData, sizeof(ackData) );     // Помещаем данные всего массива ackData в буфер FIFO. Как только будут получены любые данные от передатчика на 1 трубе, то данные из буфера FIFO будут отправлены этому передатчику вместе с пакетом подтверждения приёма его данных.
}                                                              // В модуле имеется 3 буфера FIFO, значит в них одновременно может находиться до трёх разных или одинаковых данных для ответа по одной или разным трубам.
                                                               // После отправки данных из буфера FIFO к передатчику, соответствующий буфер очищается и способен принять новые данные для отправки.
void loop(){                                                   //
    if(radio.available()){                                     // Если в буфере приёма имеются принятые данные от передатчика, то ...
        radio.read            (   &myData,  sizeof(myData)  ); // Читаем данные из буфера приёма в массив myData указывая сколько всего байт может поместиться в массив.
        byte i;
        for (i=0; i<(sizeof(myData)/sizeof(int)); i++)
          {
              ackData[i] = myData[i];
          }
        
        radio.writeAckPayload (1, &ackData, sizeof(ackData) ); // Помещаем данные всего массива ackData в буфер FIFO для их отправки на следующее получение данных от передатчика на 1 трубе.
    }                                                          // Если все 3 буфера FIFO уже заполнены, то функция writeAckPayload() будет проигнорирована.
}                                                              // Так как в данном скетче данные в буфер помещаются только после получения данных от передатчика, значит один из буферов был только что очищен и заполнение всех 3 буферов в данном скетче невозможно.
                                                     
