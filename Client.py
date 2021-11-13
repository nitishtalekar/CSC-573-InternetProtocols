import socket
import pandas as pd

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7734

class Client:
    def __init__(self, hostname, port):
        self.HOSTNAME = hostname
        self.PORT = port
        self.RFC_list = pd.DataFrame(columns = ["RFC", "TITLE"])
        self.status = False

    def Awake(self, RFC):
        self.status = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((SERVER_HOST, SERVER_PORT))
        print("[STATUS]      CONNECTION MESSAGE SENT")
        
        s = "ACTIVE\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "|"
        print(s)
        print()
        data = bytes(s, 'utf-8')
        self.sock.send(data)

        self.RFC_list = pd.DataFrame(RFC, columns=self.RFC_list.columns)
        
        for row in self.RFC_list.values:
            self.Add(row[0],row[1],1.0)
            print("[INIT ADD]      RESPONSE")
            data = self.sock.recv(100000).decode("utf-8")
            print(data)

    def Interface(self):
        cmd = int(input("\n[INPUT] \n 1. LOOKUP | 2.LIST | 3.ADD | 4.QUIT\n  SELECT COMMAND:"))
        if cmd > 4 or cmd < 0:
            print("INVALID CHOICE")
            return False
        if cmd == 4:
            return "Quit"
        version = int(input("\n[INPUT] \n 1. P2PCI/1.0 | 2.P2PCI/2.0 | 3.P2PCI/3.0 \n  SELECT VERSION:"))
        if version > 4 or version < 0:
            print("INVALID CHOICE")
            return False
        if cmd == 1:
            rfc_no = int(input("\n[INPUT] \n ENTER RFC NUMBER:"))
            self.Lookup(rfc_no,version)
            data = self.sock.recv(100000).decode("utf-8")
            print()
            print("[LOOKUP REQ]      RESPONSE")
            print(data)
        if cmd == 2:
            self.List(version)
            data = self.sock.recv(100000).decode("utf-8")
            print()
            print("[LIST REQ]      RESPONSE")
            print(data)
        if cmd == 3:
            rfc_no = int(input("\n[INPUT] \n ENTER RFC NUMBER:"))
            rfc_title = input("\n[INPUT] \n ENTER RFC TITLE:")
            self.Add(rfc_no,rfc_title,version)
            data = self.sock.recv(100000).decode("utf-8")
            print()
            print("[ADD]      RESPONSE")
            print(data)
        return True

    def Add(self, rfc_no , rfc_title , v):
        s = "ADD RFC-" + str(rfc_no) + " P2PCI/" + str(v) + "\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "\nTitle:" + str(rfc_title) + "|"
        print(s)
        print()
        data = bytes(s, 'utf-8')
        self.sock.send(data)

    def Lookup(self,rfc_no,v):
        s = "LOOKUP RFC-" + str(rfc_no) + " P2PCI/" + str(v) + "\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "|"
        print(s)
        data = bytes(s, 'utf-8')
        self.sock.send(data)
        
    def List(self,v):
        s = "LIST ALL" + " P2PCI/" + str(v) + "\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "|"
        print(s)
        data = bytes(s, 'utf-8')
        self.sock.send(data)
        
        
    def Get_An_RFC_ID(self):
        pass

    def Ask_For_RFC(self):
        pass

    def Send_RFC(self):
        pass


