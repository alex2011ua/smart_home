class DebagArduino:
    def __init__(self):
        print('run degug Arduino object')
        self.param = None
        self.dict_param = {
            b'0': 'rele off',
            b'1': 'rele on',
            b'2': 'Humidity:22.00:Temperature:29.00',
            b'3': 'Humidity:64.00:Temperature:4.20',
            b't': 'OK',
            b'B': 'bouiler on',

            b'p': "Read fail;gaz#{'temp_street': 2.20, 'Humidity_street': 85.70,'temp_voda': 31.00, 'Humidity_voda': 21.00}",

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