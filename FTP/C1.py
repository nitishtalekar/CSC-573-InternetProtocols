import Client as C
import pandas as pd
import threading
import signal
import os
import socket
import sys

# HOSTNAME = '127.0.0.2'
HOSTNAME = socket.gethostname()
PORT = 8081

# FROM COMMAND LINE
SERVER_HOST = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
FILE_INPUT = sys.argv[3]
N = int(sys.argv[4])
MSS = int(sys.argv[5])

C1 = C.Client(HOSTNAME, PORT, SERVER_HOST, SERVER_PORT, FILE_INPUT, N, MSS)
C1.Awake()
C1.rdt_send()






# thread = threading.Thread(target=C1.RFC_listen, args=())
# thread.start()

# while True:
#     interface = C1.Interface()
#     if interface == False:
#         continue
#     if interface == "Quit":
#         os._exit(1)
#         break

