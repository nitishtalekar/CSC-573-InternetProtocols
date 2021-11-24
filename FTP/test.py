import socket
import pandas as pd
import threading
import signal
from datetime import datetime, date
import os
import sys
import time
import random

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
        self.ACKS = []

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
                    break               # end of file

    def maintain_buffer(self):
        flag = 0
        while True:
            if len(self.BUFFER) < self.BUFFER_LENGTH and flag == 0:
                # data = self.rdt_send()
                # print(len([data for data in self.rdt_send()]))
                try:
                    self.BUFFER.append(next(self.rdts))
                except StopIteration:
                    while len(self.BUFFER) != self.BUFFER_LENGTH:
                        self.BUFFER.append(" ")
                    break
                # print(f"ADDING BYTE TO BUFFER - {self.BUFFER}")
                

    def create_window(self):
        while True:
            if len(self.WINDOW) < self.N and len(self.BUFFER) >= self.MSS:
                
                packet = self.BUFFER[:self.MSS]
                self.BUFFER = self.BUFFER[self.MSS:]
                packet = "".join(packet)
                self.WINDOW.append(packet)
                self.ACKS.append(True)
                # print(f"CREATING WINDOW PACKET - {self.WINDOW}")

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
                    print(f"SENDING PACKET FROM WINDOW - {self.WINDOW}")
                    # print(self.WINDOW[0], end="")
                    packet_to_send = self.WINDOW.pop(0)
                    print(f'PACKET SENT = {packet_to_send}')
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
        # self.maintain_buffer()
        self.rdts = self.rdt_send()
        thread_maintain_buffer = threading.Thread(target=self.maintain_buffer)
        thread_maintain_buffer.start()

        thread_create_window = threading.Thread(target=self.create_window)
        thread_create_window.start()

        thread_send_packet = threading.Thread(target=self.send_packet)
        thread_send_packet.start()

        # buffer = []
        # window = []
        # while True:
        #     while len(buffer) < 1024:
        #         buffer.append(self.rdt_send())

        #     while len(window) < self.N:




        #     for packet in self.rdt_send():
        #         print((self.SERVER_HOST, self.SERVER_PORT))
        #         self.sock.sendto(packet, (self.SERVER_HOST, self.SERVER_PORT))

            


    

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

     
        
        
    

