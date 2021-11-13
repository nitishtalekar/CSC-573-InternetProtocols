import Client as C
import pandas as pd

HOSTNAME = '127.0.0.1'
PORT = 8081



C1 = C.Client(HOSTNAME, PORT)
# RFC = [
#         [20, 'ASCII FORMAT FOR NETWORK INTERCHANGE'], 
#         [42, 'MESSAGE DATA TYPES'], 
#         [768, 'USER DATAGRAM PROTOCOL']
#     ]
RFC = { 
        "RFC" : [20,42,768],
        'TITLE': [
                    'ASCII FORMAT FOR NETWORK INTERCHANGE', 
                    'MESSAGE DATA TYPES',  
                    'USER DATAGRAM PROTOCOL']
        }
C1.Awake(RFC)


while True:
    cmd = input("[INPUT] Enter Command: ")
    data = bytes(cmd, 'utf-8')
    C1.sock.sendall(data)
    if data == b'Q':
        C1.sock.close()
        break

