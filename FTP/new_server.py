import socket
import time
import random
import sys
import os


class Server:
    def __init__(self, PORT, FILE_OUTPUT, PROB_LOSS_SERVICE):
        self.HOST = socket.gethostname()
        self.PORT = PORT
        self.FILE_PATH = FILE_OUTPUT
        self.FILE_OUTPUT = open(FILE_OUTPUT, "wb")
        self.PROB_LOSS_SERVICE = PROB_LOSS_SERVICE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.HOST, self.PORT))
        self.SEQ_NO = 0
        self.DATA_TYPE = '0101010101010101'
        self.ACK_TYPE = '1010101010101010'
        self.COMPLETE = False
        print(f"[SERVER] ACTIVELY LISTENING AT {self.HOST} ON {self.PORT}")

    def __str__(self):
        return f"[SERVER] ACTIVELY LISTENING AT {self.HOST} ON {self.PORT}"

    def carry_around_add(self, x, y):
        return ((x+y) & 0xffff) + ((x + y) >> 16)

    def checksum_computation(self, message):
        add = 0
        for i in range(0, len(message) - len(message) % 2, 2):
            message = str(message)
            w = ord(message[i]) + (ord(message[i + 1]) << 8)
            add = self.carry_around_add(add, w)
        return ~add & 0xffff

    def packet_accepted(self):
        r = random.random()
        return r > self.PROB_LOSS_SERVICE

    def send_packet(self, data, addr):
        self.sock.sendto(str.encode(data), addr)
            

    def retransmit(self):
        self.WINDOW_TIMEOUT = []
        for data in self.WINDOW:
            self.send_packet(data)
            self.WINDOW_TIMEOUT.append(time.time())

    def rdt_rcv(self):
        self.sock.settimeout(10)
        try:
            while True:
                data, CLIENT_ADDR = self.sock.recvfrom(2048)
                data = data.decode()
                if data == "EOF":
                    print("[SERVER] TRANSMISSION COMPLETE")
                    self.COMPLETE = True
                    break
                # print()
                # print(f"[SERVER] Recieved Packet {data[64:]}")

                # print("RECIEVED")
                # print(f'SEQUENCE NO: {data[:32]}')
                # print(f'CHECKSUM: {data[32:48]}')
                # print(f'HEADER TYPE: {data[48:64]}')
                # print(f'DATA: {data[64:]}')

                
                computed_checksum = self.checksum_computation(data[:32]+data[48:])
                computed_checksum = f'{computed_checksum:016b}'
                # print(computed_checksum)
      
                if computed_checksum == data[32:48] and data[48:64] == self.DATA_TYPE:
                    if self.SEQ_NO == int(data[:32], 2):
                        # print('Sending ACK')
                        if self.packet_accepted():
                            self.FILE_OUTPUT.write(str.encode(data[64:]))
                            # reply
                            header = data[:32]
                            header += '0000000000000000'
                            header += self.ACK_TYPE

                            self.send_packet(header, CLIENT_ADDR)
                            self.SEQ_NO += 1
                        else:
                            print(f'[SERVER] PACKET DROPPED :{data[:32]} \t :{int(data[:32],2)}')

        except Exception as e:
            print(e)
            # print('huha')
            self.FILE_OUTPUT.close()
            if os.path.getsize(self.FILE_PATH) == 0 and self.COMPLETE:
                print(e)
                print('CONNECTION TIMED OUT')
                print("FILE DOWNLOAD FAILED")
            else:
                print('[SERVER] DOWNLOAD COMPLETE')
            self.sock.close()
        



if len(sys.argv) > 1:
    # FROM COMMAND LINE
    PORT = int(sys.argv[1])
    FILE_OUTPUT = sys.argv[2]
    PROB_LOSS_SERVICE = float(sys.argv[3])
else:
    PORT = 7735
    FILE_OUTPUT = 'output.txt'
    PROB_LOSS_SERVICE = 0.01

S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
S1.rdt_rcv()