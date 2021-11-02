import socket

host = '127.0.0.1'
port = 60000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.bind((host, port))
s.listen()

conn, addr = s.accept()

print("Connected by: ", addr)

while True:
    data = conn.recv(40000)
    print(data)
    if not data:
        break


class Server:
    def __init__(self):
        self.RFC_Table = {'Number': ['Title', 'Peer_list']}
        self.Active_Peers = {'name': 'Port'}

    def Active(self):
        pass

    def Inactive(self):
        pass

    def UpdateList(self):
        pass

    def LookUp_RFC_ID(self):
        pass

    def Send_List(self):
        pass
