import Client as C
import pandas as pd
import threading
import signal
import os
import socket

# HOSTNAME = '127.0.0.2'
HOSTNAME = socket.gethostname()
PORT = 8081
OS = "Windows OS 11.6"

path = "C1"

C1 = C.Client(HOSTNAME, PORT, OS, path)
RFC = [
        ['20', 'ASCII FORMAT FOR NETWORK INTERCHANGE',os.path.join(path, "20.txt")], 
        ['42', 'MESSAGE DATA TYPES', os.path.join(path, "42.txt")], 
        ['768', 'USER DATAGRAM PROTOCOL', os.path.join(path, "768.txt")]
    ]

C1.Awake(RFC)

thread = threading.Thread(target=C1.RFC_listen, args=())
thread.start()

while True:
    interface = C1.Interface()
    if interface == False:
        continue
    if interface == "Quit":
        os._exit(1)
        break

