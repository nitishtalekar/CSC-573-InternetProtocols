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
        # print(f"{SERVER")

    def Active(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.HOST, self.PORT))
        
        run = True
        print(f"[SERVER] ACTIVELY LISTENING AT {self.HOST} ON {self.PORT}")


        while run:
            data, _ = self.sock.recvfrom(4096)
            # print(data)
            with open(self.FILE_OUTPUT, 'a+') as F_O:
                F_O.write(str(data.decode('utf-8')))


            # conn, addr = self.sock.recvfrom(1024)

            # thread = threading.Thread(target=self.ClientConnected, args=(conn, addr))
            # thread.start()
            # print(f"[ACTIVE CONNECTIONS]    {threading.activeCount() - 1}")
            

     
n = len(sys.argv)


# FROM COMMAND LINE
PORT = int(sys.argv[1])
FILE_OUTPUT = sys.argv[2]
PROB_LOSS_SERVICE = float(sys.argv[3])

# print(PORT, type(PORT))
# print(FILE_OUTPUT, type(FILE_OUTPUT))
# print(PROB_LOSS_SERVICE, type(PROB_LOSS_SERVICE))


S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
S1.Active()