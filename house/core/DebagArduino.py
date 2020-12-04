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
            b'p': "#{'temp_street': 0.30, 'humidity_street': 95.40,'temp_voda': 5.00, 'humidity_voda': 76.00,'temp_gaz': 27.00, 'humidity_gaz': 28.00,'MQ135_value': 70,'MQ4_value': 49,'muve_kitchen': 0}",

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