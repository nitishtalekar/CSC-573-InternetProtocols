import socket
import pandas as pd

host = '127.0.0.1'
port = 7734




class Server:
    def __init__(self):
        self.PORT = 7734
        self.RFC_Table = pd.DataFrame(columns = ["RFC", "TITLE", 'HOSTNAME'])
        self.Peers = pd.DataFrame(columns = ['HOSTNAME', 'PORT'])

    def Active(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        run_loop = True
        while run_loop:
            self.sock.listen()
            conn, addr = self.sock.accept()

            print(f"[CONNECTION] HOST: {addr} Connected")

            while True:
                data = conn.recv(40000).decode("utf-8")
                if data == "Q":
                    run_loop = False
                    break
                data_s = data.split("|")

                if data_s[0] == 'ACTIVE':
                    self.AddPeer(data_s[1], data_s[2:])
        print(self.RFC_Table)
        self.sock.close()

                


    def AddPeer(self, hostport, rfcs):
        print("IN ADDPEER")
        self.Peers.append(hostport.split(','))
        for row in rfcs:
            print(row)
            new_rfc = row.split(',')
            self.RFC_Table.append([new_rfc[0], new_rfc[1], hostport.split(',')[0]])


    def UpdateList(self):
        pass

    def LookUp_RFC_ID(self):
        pass

    def Send_List(self):
        pass


S1 = Server()
S1.Active()