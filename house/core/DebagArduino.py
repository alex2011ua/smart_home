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
            b'p': "Read fail;street; Read fail;voda; #{'temp_gaz': 24.00, 'humidity_gaz': 19.00,'MQ135_value': 50,'MQ4_value': 60}",

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