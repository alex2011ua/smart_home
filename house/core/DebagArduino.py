class DebagArduino:
    def __init__(self):
        print('run degug Arduino object')
        self.param = None
        self.dict_param = {
            b'A': 'rele on',
            b'a': 'rele off',
            b'B': 'rele on',
            b'b': 'rele off',
            b'C': 'rele on',
            b'c': 'rele off',
            b'S': 'Sound on',
            b's': 'Sound off',
            b't': 'OK',
            b'r': '',
            b'p': "Read fail-street;Read fail-teplica;#{'temp_street': 17.30, 'hum_street': 72.70,'temp_teplica': 19.00, 'hum_teplica': 84.10,'temp_voda': 18.00, 'hum_voda': 81.00,'temp_gaz': 25.00, 'hum_gaz': 29.00,'MQ135': 18,'MQ4': 48,'muve_k': 0, 'sound': 0, 'temp_room': 0, 'myData': '55 0 55 55 0 0', 'ackData': '11 15 16 1 1 1'}",
            b'D': '',
            b'd': '',
            b'E': '',
            b'e': '',
            b'F': '',
            b'f': '',
            b'G': '',
            b'g': '',
            b'H': '',
            b'h': '',



        }
    def write(self, param):
        self.param = param
        print('Send Arduino ', param)

    def read(self):
        string_arduino = self.dict_param[self.param]
        print('read Arduino ', string_arduino)
        return string_arduino

    def restart(self):
        pass