import struct

class Data:
    def __init__(self,data,sequence) -> None:
        self.raw = data
        self.sequence = f'{sequence:04d}'
        self.data = self.encapsulate()

    def __str__(self) -> str:
        return f'{self.data}'

    def suffix(self,type='packet'):
        if type == 'ack':
            return f'{0b1010101010101010:02d}'
        elif type== 'packet':
            return f'{0b0101010101010101:02d}'


    def checksum(self):
        checksum = 0
        data_len = len(self.raw)
        if (data_len % 2):
            data_len += 1
            self.raw += struct.pack('!B', 0)
        
        for i in range(0, data_len, 2):
            w = (self.raw[i] << 8) + (self.raw[i + 1])
            checksum += w

        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum = ~checksum & 0xFFFF
        return f'{checksum:02d}'
    
    def encapsulate(self,type):
        if type == 'ack':
            self.data = self.sequence + f'{0:02d}' + self.suffix(type)
        elif type == 'packet':
            self.data = self.sequence+self.checksum()+self.suffix(type)+self.raw
        return self.data
