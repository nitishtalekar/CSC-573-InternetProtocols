import socket
import pandas as pd
import threading
import signal
from datetime import datetime, date
import os
import sys
import time
import warnings
warnings.filterwarnings("ignore")

# SERVER_HOST = "127.0.0.1"
SERVER_HOST = socket.gethostname()
SERVER_PORT = 7734

class Client:
    def __init__(self, HOSTNAME, PORT, SERVER_HOST, SERVER_PORT, FILE_INPUT, N, MSS):
        self.HOSTNAME = HOSTNAME
        self.PORT = PORT
        self.SERVER_HOST = SERVER_HOST
        self.SERVER_PORT = SERVER_PORT
        self.FILE_INPUT = FILE_INPUT
        self.N = N
        self.MSS = MSS
        self.BUFFER = []
        self.BUFFER_LENGTH =24
        # self.WINDOW = []
        self.SEQUENCE_NUMBER = 0
        self.WINDOW = pd.DataFrame(columns = ["PACKET", "SEQ_NO", "SENT", "SENT_TS"])
        self.NEXT_ACK_EXPECTED = 0
        self.OUTGONE_PACKETS = pd.DataFrame(columns = ["PACKET", "SEQ_NO", "SENT", "SENT_TS"])

    def __str__(self):
        return f'{self.HOSTNAME},{self.PORT},{self.SERVER_HOST},{self.SERVER_PORT},{self.FILE_INPUT},{self.N},{self.MSS}'

    def Awake(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        

    def rdt_send(self):
        # GET MSS SIZE DATA
        with open(self.FILE_INPUT, "rb") as in_file:
            while True:
                piece = in_file.read(1)
                yield piece.decode('utf-8')     # RETURN 1Byte Read
                if piece == b'':
                    break                       # end of file

    def maintain_buffer(self):
        flag = 0
        while True:
            if len(self.BUFFER) < self.BUFFER_LENGTH and flag == 0:
                try:
                    self.BUFFER.append(next(self.rdts))
                except StopIteration:
                    while len(self.BUFFER) != self.BUFFER_LENGTH:
                        self.BUFFER.append(" ")
                    break
                # print(f"ADDING BYTE TO BUFFER - {self.BUFFER}")
                # print("".join(self.BUFFER))

    def carry_around_add(self, x, y):
        return ((x+y) & 0xffff) + ((x + y) >> 16)

    def checksum_computation(self, message):
        add = 0
        for i in range(0, len(message) - len(message) % 2, 2):
            message = str(message)
            w = ord(message[i]) + (ord(message[i + 1]) << 8)
            add = self.carry_around_add(add, w)
        return ~add & 0xffff
    
    def pack_packet(self, packet):
        data = ""
        data += str(f'{self.SEQUENCE_NUMBER}') + "|"        # {self.SEQUENCE_NUMBER:032b}
        self.SEQUENCE_NUMBER += 1
        data += str(f'0101010101010101') + "|"
        data += str(packet)

        ch = self.checksum_computation(data)

        data = ""
        data += str(f'{self.SEQUENCE_NUMBER:032b}') + "|"
        data += str(f'{ch:016b}') + "|"
        data += str(f'0101010101010101') + "|"
        data += str(packet)

        # print(data)
        return data, self.SEQUENCE_NUMBER - 1

    def create_window(self):
        while True:
            if len(self.WINDOW) + len(self.OUTGONE_PACKETS) < self.N and len(self.BUFFER) >= self.MSS:
                data = self.BUFFER[:self.MSS]
                self.BUFFER = self.BUFFER[self.MSS:]

                packet = "".join(data)
                packet, seq = self.pack_packet(packet)

                self.WINDOW.loc[len(self.WINDOW)] = [packet, seq, False, 0]
                # print(f"CREATING WINDOW PACKET - {self.WINDOW}")
                print("".join(data))



    def send_packet(self):
        while True:
            if len(self.WINDOW) > 0 and len(self.OUTGONE_PACKETS) < self.N:
                pass
                # print()
                # packet_to_send = self.WINDOW.iloc[0, :].values
                # packet = packet_to_send[0]
                

                # packet_series = pd.Series(packet_to_send, index = self.OUTGONE_PACKETS.columns)
                # # print(packet_series)
                # self.OUTGONE_PACKETS = self.OUTGONE_PACKETS.append(packet_series, ignore_index=True)
                # self.WINDOW = self.WINDOW[self.WINDOW.SEQ_NO != packet_to_send[1]]
                # self.WINDOW.reset_index(drop = True)
                # print(self.OUTGONE_PACKETS)
                # df = df[df.line_race != 0]


                # self.sock.sendto(str.encode(), (self.SERVER_HOST, self.SERVER_PORT))


    def checkTime(self):
        pass

    def gobackn_client(self):
        self.rdts = self.rdt_send()
        thread_maintain_buffer = threading.Thread(target=self.maintain_buffer)
        thread_maintain_buffer.start()

        thread_create_window = threading.Thread(target=self.create_window)
        thread_create_window.start()

        thread_send_packet = threading.Thread(target=self.send_packet)
        thread_send_packet.start()

        while True:
            


            


    

HOSTNAME = socket.gethostname()
PORT = 8081

# FROM COMMAND LINE
SERVER_HOST = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
FILE_INPUT = sys.argv[3]
N = int(sys.argv[4])
MSS = int(sys.argv[5])

C1 = Client(HOSTNAME, PORT, SERVER_HOST, SERVER_PORT, FILE_INPUT, N, MSS)
print(f'Client1={C1}')
C1.Awake()
C1.gobackn_client()

     
        
        
    

