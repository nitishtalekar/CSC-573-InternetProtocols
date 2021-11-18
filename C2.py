import Client as C
import pandas as pd
import threading
import sys
import os

HOSTNAME = '127.0.0.3'
PORT = 5678
OS = "Mac OS 10.6"

C2 = C.Client(HOSTNAME, PORT,OS)
RFC = [
        ['783', 'THE TFTP PROTOCOL (REVISION 2)'], 
        ['792', 'INTERNET CONTROL MESSAGE PROTOCOL'], 
        ['854', 'TELNET PROTOCOL SPECIFICATION']
    ]

C2.Awake(RFC)

thread = threading.Thread(target=C2.RFC_listen, args=())
thread.start()

while True:
    interface = C2.Interface()
    if interface == False:
        continue
    if interface == "Quit":
        os._exit(1)
        break

