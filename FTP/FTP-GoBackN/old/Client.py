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

    def __str__(self):
        return f'{self.HOSTNAME},{self.PORT},{self.SERVER_HOST},{self.SERVER_PORT},{self.FILE_INPUT},{self.N},{self.MSS}'

    def Awake(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        

    # def rdt_send(self):
    #     # GET MSS SIZE DATA
    #     packets = []
    #     with open(self.FILE_INPUT, "rb") as in_file:
    #         # print(in_file.read(5))
    #         i = 0
    #         while True:
    #             # print("HELLO", self.MSS)
    #             piece = in_file.read(self.MSS)
    #             # print("\n\n", piece)
    #             i = i+1
    #             if piece == b'':
    #                 break # end of file
    #             packets.append(piece)
    #     # print(packets)
    #     self.gobackn_client(packets)

    # def gobackn_client(self, packets):
    #     for packet in packets:
    #         print((self.SERVER_HOST, self.SERVER_PORT))
    #         self.sock.sendto(packet, (self.SERVER_HOST, self.SERVER_PORT))

    def rdt_send(self):
        # GET MSS SIZE DATA
        window = [['']]*self.N
        packet_of_size_MSS = ['']*self.MSS
        with open(self.FILE_INPUT, "rb") as in_file:
            counter_for_window,counter_for_packet = 0,0
            while True:
                byte = in_file.read(1)
                if byte == b'':
                    break # end of file
                packet_of_size_MSS[counter_for_packet]=byte
                counter_for_window+=1
                if counter_for_packet==self.MSS:
                    window[counter_for_window]=packet_of_size_MSS.copy() # club the bytes to form MSS packet
                    counter_for_window+=1                          # packet has been added to window, increment counter
                    packet_of_size_MSS = ['']*self.MSS          # reinitialize packet
                    counter_for_packet=0                        # reinitialize packet counter
                    if counter_for_window==self.N:
                        # Resend window if False is returned, dont move ahead.
                        while not self.gobackn_client(packet_of_size_MSS):
                            self.gobackn_client(window)
                        window = [['']]*self.N                  # reinitialize window
                        counter_for_packet=0                    # reinitialize window counter

    def gobackn_client(self, packet_of_size_MSS):
        # Return True for success of all packets in window
        # Return False for failure
        self.sock.sendto(packet_of_size_MSS, (self.SERVER_HOST, self.SERVER_PORT))
            


    
        
        
        
    

