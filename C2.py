import Client as C
import pandas as pd

HOSTNAME = '127.0.0.3'
PORT = 5678



C2 = C.Client(HOSTNAME, PORT)
RFC = [
        [783, 'THE TFTP PROTOCOL (REVISION 2)'], 
        [792, 'INTERNET CONTROL MESSAGE PROTOCOL'], 
        [854, 'TELNET PROTOCOL SPECIFICATION']
    ]

C2.Awake(RFC)


while True:
    interface = C2.Interface()
    if interface == False:
        continue
    if interface == "Quit":
        break

