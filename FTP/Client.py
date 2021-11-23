import socket
import pandas as pd
import threading
import signal
from datetime import datetime, date
import os


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

    def Awake(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        

    def rdt_send(self):
        # GET MSS SIZE DATA
        packets = []
        with open(self.FILE_INPUT, "rb") as in_file:
            # print(in_file.read(5))
            i = 0
            while True:
                # print("HELLO", self.MSS)
                piece = in_file.read(self.MSS)
                # print("\n\n", piece)
                i = i+1
                if piece == b'':
                    break # end of file
                packets.append(piece)
        print(packets)
        self.gobackn_client(packets)

    def gobackn_client(self, packets):
        for packet in packets:
            print((self.SERVER_HOST, self.SERVER_PORT))
            self.sock.sendto(packet, (self.SERVER_HOST, self.SERVER_PORT))


    
        
        
        
    

