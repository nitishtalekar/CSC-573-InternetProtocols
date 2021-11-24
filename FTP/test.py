import socket
import pandas as pd
import threading
import signal
from datetime import datetime, date
import os
import sys
import time
import random
import struct

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
        self.BUFFER_LENGTH = 64
        self.WINDOW = []
        self.TRACK_PACKET = pd.DataFrame()
        self.SEQUENCE_NUMBER = 0

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
                
    # def checksum(self, raw_data):
    #     checksum = 0
    #     data_len = len(raw_data)
    #     # print(type(raw_data))
    #     if (data_len % 2):
    #         data_len += 1
    #         # print(type(struct.pack('!B', 0)))
    #         raw_data += struct.pack('!B', 0)
        
    #     for i in range(0, data_len, 2):
    #         w = (raw_data[i] << 8) + (raw_data[i + 1])
    #         checksum += w

    #     checksum = (checksum >> 16) + (checksum & 0xFFFF)
    #     checksum = ~checksum & 0xFFFF
    #     return f'{checksum:016b}'

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

        print(data)
        return data

    def create_window(self):
        while True:
            if len(self.WINDOW) < self.N and len(self.BUFFER) >= self.MSS:
                packet = self.BUFFER[:self.MSS]
                self.BUFFER = self.BUFFER[self.MSS:]
                packet = "".join(packet)
                packet = self.pack_packet(packet)
                self.WINDOW.append(packet)
                print(f"CREATING WINDOW PACKET - {self.WINDOW}")

    def checkTime():
        pass

    def socket_send(self,packet):
        respone_wait = random.choice([1,1,3])
        # if respone_wait<=2:
        time.sleep(respone_wait)
        return random.choice([True,False])

    def send_packet(self):
        i = 0
        # print(f"IN SEND")
        while True:
            if len(self.WINDOW) > 0:
                # print(f"IN SEND")
                try:
                    # print(f"SENDING PACKET FROM WINDOW - {self.WINDOW}")
                    # print(self.WINDOW[0], end="")
                    packet_to_send = self.WINDOW.pop(0)
                    # print(f'PACKET SENT = {packet_to_send}')
                    thread_acks = threading.Thread(target=self.socket_send,args=(packet_to_send,))
                    thread_acks.start()

                    # print(f"SENT PACKET FROM WINDOW - {self.WINDOW}")
                    # self.BUFFER = self.BUFFER[self.MSS:]
                    # print(f"SENT PACKET FROM WINDOW (BUFFER)- {self.BUFFER}")
                    # time.sleep(1)
                    i = i + 1
                except Exception:
                    continue


    def gobackn_client(self):
        self.rdts = self.rdt_send()
        thread_maintain_buffer = threading.Thread(target=self.maintain_buffer)
        thread_maintain_buffer.start()

        thread_create_window = threading.Thread(target=self.create_window)
        thread_create_window.start()

        thread_send_packet = threading.Thread(target=self.send_packet)
        thread_send_packet.start()


            


    

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

     
        
        
    

