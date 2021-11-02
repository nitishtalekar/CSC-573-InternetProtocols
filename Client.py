import socket

host = '127.0.0.1'
port = 60000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.connect((host, port))
s.sendall(b"HELLLOOOOOOOOO")


class Client:
    def __init__(self):
        self.RFC = {}
        self.status = True
        self.peer_id = ''

    def I_Am_Awake(self):
        self.status = True
        # Send To Server
        pass

    def I_Am_Asleep(self):
        self.status = False
        # Send To Server
        pass

    def HereIsMyList(self):
        pass

    def UpdateMyList(self):
        pass

    def Get_An_RFC_ID(self):
        pass

    def Ask_For_RFC(self):
        pass

    def Send_RFC(self):
        pass
