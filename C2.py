import Client as C
import pandas as pd
import threading
import os
import socket

# HOSTNAME = '127.0.0.3'
HOSTNAME = socket.gethostname()
PORT = 5678
OS = "Mac OS 10.6"

C2 = C.Client(HOSTNAME,PORT,OS)
RFC = [
        ['783', 'THE TFTP PROTOCOL (REVISION 2)',"CONTENT CONTENT 783"], 
        ['792', 'INTERNET CONTROL MESSAGE PROTOCOL',"CONTENT CONTENT 792"], 
        ['854', 'TELNET PROTOCOL SPECIFICATION',"CONTENT CONTENT 854"]
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

