import Client as C
import pandas as pd
import threading
import os
import socket

# HOSTNAME = '127.0.0.3'
HOSTNAME = socket.gethostname()
PORT = 5678
OS = "Mac OS 10.6"
PATH = "C2"

C2 = C.Client(HOSTNAME,PORT,OS,PATH)
RFC = [
        ['783', 'THE TFTP PROTOCOL (REVISION 2)', os.path.join(PATH, "783.txt"),"2"], 
        ['792', 'INTERNET CONTROL MESSAGE PROTOCOL', os.path.join(PATH, "792.txt"),"2"], 
        ['854', 'TELNET PROTOCOL SPECIFICATION', os.path.join(PATH, "854.txt"),"2"]
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

