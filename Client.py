import socket
import pandas as pd
import threading
import signal

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7734

class Client:
    def __init__(self, hostname, port,os):
        self.HOSTNAME = hostname
        self.PORT = port
        self.OS = os
        self.RFC_list = pd.DataFrame(columns = ["RFC", "TITLE"])
        self.status = False
        self.errors = {200:"OK",400:"Bad Request",404:"Not Found",500:"P2PCI version not supported"}

    def Awake(self, RFC):
        self.status = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((SERVER_HOST, SERVER_PORT))
        print("[STATUS]      CONNECTION MESSAGE SENT")
        
        s = "ACTIVE\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "|"
        print(s)
        print()
        data = bytes(s, 'utf-8')
        self.sock.sendall(data)

        self.RFC_list = pd.DataFrame(RFC, columns=self.RFC_list.columns)
        
        for row in self.RFC_list.values:
            self.Add(row[0],row[1],1.0)
            print("[INIT ADD]      RESPONSE")
            data = self.sock.recv(100000).decode("utf-8")
            print(data)

    def Interface(self):
        cmd = int(input("\n[INPUT] \n 1. LOOKUP | 2.LIST | 3.ADD | 4.GET | 5.QUIT\n  SELECT COMMAND:"))
        if cmd > 5 or cmd < 0:
            print("INVALID CHOICE")
            return False
        if cmd == 5:
            self.Logout()
            return "Quit"
        version = int(input("\n[INPUT] \n 1. P2PCI/1.0 | 2.P2PCI/2.0 | 3.P2PCI/3.0 \n  SELECT VERSION:"))
        if version > 3 or version < 0:
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
        if cmd == 4:
            rfc_no = int(input("\n[INPUT] \n ENTER RFC NUMBER:"))
            rfc_host = input("\n[INPUT] \n ENTER HOSTNAME:")
            rfc_port = int(input("\n[INPUT] \n ENTER PORT NUMBER:"))
            self.Get(rfc_no,rfc_host,rfc_port,version)
            print("HERE")
            data = self.get_sock.recv(100000).decode("utf-8")
            print()
            print("[GET]      RESPONSE")
            print(data)
        return True

    def Add(self, rfc_no , rfc_title , v):
        self.RFC_list.loc[len(self.RFC_list)] = [str(rfc_no),rfc_title]
        print(self.RFC_list)
        print("RFCLST")
        s = "ADD RFC-" + str(rfc_no) + " P2PCI/" + str(v) + "\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "\nTitle:" + str(rfc_title) + "|"
        print(s)
        print()
        data = bytes(s, 'utf-8')
        self.sock.sendall(data)

    def Lookup(self,rfc_no,v):
        s = "LOOKUP RFC-" + str(rfc_no) + " P2PCI/" + str(v) + "\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "|"
        print(s)
        data = bytes(s, 'utf-8')
        self.sock.sendall(data)
        
    def List(self,v):
        s = "LIST ALL" + " P2PCI/" + str(v) + "\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "|"
        print(s)
        data = bytes(s, 'utf-8')
        self.sock.sendall(data)
        
    
    def RFC_listen(self):
        self.sock_rfc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_rfc.bind((self.HOSTNAME, self.PORT))
        self.sock_rfc.listen()
        while True:
            conn, addr = self.sock_rfc.accept()
            thread = threading.Thread(target=self.Send, args=(conn, addr))
            thread.start()
            
        
    def Get(self,rfc_no,get_host,get_port,v):
        self.get_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.get_sock.connect((get_host, get_port))
        s = "GET RFC-" + str(rfc_no) + " P2PCI/" + str(v) + "\nHost:" + str(get_host) + "\nOS:" + str(self.OS) + "|"
        print(s)
        data = bytes(s, 'utf-8')
        self.get_sock.sendall(data)
        print("GET REQUEST SENT")
        # self.get_sock.close()

    def Logout(self):
        self.sock.close()

    def Send(self,conn,addr):
        data = conn.recv(100000).decode("utf-8")
        commands = data.split("|")
        for comd in commands[:-1]:
            cmd = comd.split("\n")   
            if cmd[0].split(" ")[0] == "GET":
                resp = self.SendRFC(cmd)
                print()
                print(resp)
                print("HIE")
                r_data = bytes(resp, 'utf-8')
                conn.sendall(r_data)
        print("CLOSE CONN")
        conn.close()
    
    def SendRFC(self,cmd):
        rfc = cmd[0].split(" ")[1].split("-")[1]
        v = cmd[0].split(" ")[2]
        h = cmd[1].split(":")[1]
        os = cmd[2].split(":")[1]
        send_rfc = self.RFC_list.loc[self.RFC_list['RFC'] == rfc]
        s_rfc = send_rfc.iloc[0]
        resp = ""
        if len(send_rfc) > 0:
            code = 200
            resp = v + " " + str(code) + " " + self.errors[code] + "\n"
            resp += "RFC " + str(s_rfc[0]) + " " + str(s_rfc[1]) + "\n"
        elif len(send_rfc) == 0:
            code = 404
            resp = v + " " + str(code) + " " + self.errors[code] + "\n"
        return resp
        
    

