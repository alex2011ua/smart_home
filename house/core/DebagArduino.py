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
            b'p': "Read fail-street;Read fail-teplica;#{'temp_street': 12.70, 'humidity_street': 76.90,'temp_voda': 15.00, 'humidity_voda': 72.00,'temp_gaz': 0.00, 'humidity_gaz': 1.00,'MQ135_value': 24,'MQ4_value': 57,'muve_kitchen': 242, 'sound': 0, 'temp_room': 0}",

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