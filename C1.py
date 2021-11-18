import Client as C
import pandas as pd
import threading
import signal
import os

HOSTNAME = '127.0.0.2'
PORT = 8081
OS = "Windows OS 11.6"



C1 = C.Client(HOSTNAME, PORT,OS)
RFC = [
        ['20', 'ASCII FORMAT FOR NETWORK INTERCHANGE',"CONTENT CONTENT 20"], 
        ['42', 'MESSAGE DATA TYPES',"CONTENT CONTENT 42"], 
        ['768', 'USER DATAGRAM PROTOCOL',"CONTENT CONTENT 768"]
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

