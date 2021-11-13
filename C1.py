import Client as C
import pandas as pd

HOSTNAME = '127.0.0.2'
PORT = 8081



C1 = C.Client(HOSTNAME, PORT)
RFC = [
        [20, 'ASCII FORMAT FOR NETWORK INTERCHANGE'], 
        [42, 'MESSAGE DATA TYPES'], 
        [768, 'USER DATAGRAM PROTOCOL']
    ]

C1.Awake(RFC)

while True:
    interface = C1.Interface()
    if interface == False:
        continue
    if interface == "Quit":
        break

