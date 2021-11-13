import socket
import pandas as pd
host = '127.0.0.1'
# port = 60000

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# s.connect((host, port))
# s.sendall(b"HELLLOOOOOOOOO")
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7734

class Client:
    def __init__(self, hostname, port):
        self.HOSTNAME = hostname
        self.PORT = port
        self.RFC = pd.DataFrame(columns = ["RFC", "TITLE"])
        self.status = False

    def Awake(self, RFC_New):
        self.status = True
        print(RFC_New)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((SERVER_HOST, SERVER_PORT))
        print("[STATUS]      CONNECTION MESSAGE SENT")
        # temp_df = pd.DataFrame.from_dict(RFC_New)
        # print(temp_df)
        self.RFC.concat(pd.DataFrame.from_dict(RFC_New), ignore_index=True)
        print(self.RFC)

        s = "ACTIVE|" + str(self.HOSTNAME) + "," + str(self.PORT) + "|"
        for row in self.RFC.values:
            s = str(row[0]) + "," + str(row[1]) + "|"
        s = s[:-1]
        print(s)
        data = bytes(s, 'utf-8')
        print("[STATUS]      SHARING RFC WITH SERVER")
        self.sock.sendall(data)

    def I_Am_Asleep(self):
        self.status = False
        # Send To Server
        pass

    def Add(self, RFC):
        pass

    def UpdateMyList(self):
        pass

    def Get_An_RFC_ID(self):
        pass

    def Ask_For_RFC(self):
        pass

    def Send_RFC(self):
        pass


