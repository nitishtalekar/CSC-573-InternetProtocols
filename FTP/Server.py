import sys
import socket
import pandas as pd
import threading
import signal
import os
import time

class Server:
    def __init__(self, PORT, FILE_OUTPUT, PROB_LOSS_SERVICE):
        self.HOST = socket.gethostname()
        self.PORT = PORT
        self.FILE_OUTPUT = FILE_OUTPUT
        self.PROB_LOSS_SERVICE = PROB_LOSS_SERVICE

    def carry_around_add(self, x, y):
        return ((x+y) & 0xffff) + ((x + y) >> 16)

    def checksum_computation(self, message):
        add = 0
        for i in range(0, len(message) - len(message) % 2, 2):
            message = str(message)
            w = ord(message[i]) + (ord(message[i + 1]) << 8)
            add = self.carry_around_add(add, w)
        return ~add & 0xffff

    def validate_data(self, data):
        pass

    def active(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST, self.PORT))
        
        run = True
        print(f"[SERVER] ACTIVELY LISTENING AT {self.HOST} ON {self.PORT}")
        try:
            while run:
                data, _ = self.sock.recvfrom(4096)

                with open(self.FILE_OUTPUT, 'a+') as F_O:
                    F_O.write(str(data.decode('utf-8')))


                # conn, addr = self.sock.recvfrom(1024)

                # thread = threading.Thread(target=self.ClientConnected, args=(conn, addr))
                # thread.start()
                # print(f"[ACTIVE CONNECTIONS]    {threading.activeCount() - 1}")
        except KeyboardInterrupt:
            print(f"[SERVER] CLOSING CONNECTION AT {self.HOST} ON {self.PORT}")

            self.sock.close()
            sys.exit()
            
    
     

n = len(sys.argv)

# FROM COMMAND LINE
PORT = int(sys.argv[1])
FILE_OUTPUT = sys.argv[2]
PROB_LOSS_SERVICE = float(sys.argv[3])

# print(PORT, type(PORT))
# print(FILE_OUTPUT, type(FILE_OUTPUT))
# print(PROB_LOSS_SERVICE, type(PROB_LOSS_SERVICE))


S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
S1.active()