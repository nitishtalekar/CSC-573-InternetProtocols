import socket
import pandas as pd
import threading
import signal
from datetime import datetime, date


# SERVER_HOST = "127.0.0.1"
SERVER_HOST = socket.gethostname()
SERVER_PORT = 7734

class Client:
    def __init__(self, hostname, port,os):
        self.HOSTNAME = hostname
        self.PORT = port
        self.OS = os
        self.RFC_list = pd.DataFrame(columns = ["RFC", "TITLE","CONTENT","MODIFY","LENGTH","TYPE","VERSION"])
        self.status = False
        self.errors = {200:"OK",400:"Bad Request",404:"Not Found",500:"P2PCI version not supported"}

    def Awake(self, RFC):
        self.status = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((SERVER_HOST, SERVER_PORT))
        print("[ACTIVE]      CONNECTION MESSAGE SENT")
        
        s = "ACTIVE\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "|"
        print(s)
        print()
        data = bytes(s, 'utf-8')
        self.sock.sendall(data)
        print("[ACTIVE]      RESPONSE")
        data = self.sock.recv(100000).decode("utf-8")
        print(data)
        print()
        
        for row in RFC:
            mod = datetime.now().strftime("%a, %d %b %Y %H:%M:%S") + " GMT"
            self.Add(row[0],row[1],row[2],mod,len(row[2]),"text/text",1.0)
            print("[ADD]      RESPONSE")
            data = self.sock.recv(100000).decode("utf-8")
            print(data)
            print()

    def Interface(self):
        cmd = int(input("\n[INPUT] \n 1. LOOKUP | 2.LIST | 3.ADD | 4.GET | 5.QUIT\n  SELECT COMMAND:"))
        if cmd > 5 or cmd < 0:
            print()
            print("INVALID CHOICE")
            return False
        if cmd == 5:
            print('[CLOSE]      REQUEST SENT')
            self.Logout()
            data = self.sock.recv(100000).decode("utf-8")
            print()
            print("[CLOSE]      RESPONSE")
            print(data)
            self.sock.close()
            return "Quit"
        version = int(input("\n[INPUT] \n 1.P2PCI/1.0 | 2.P2PCI/2.0 | 3.P2PCI/3.0 \n  SELECT VERSION:"))
        if version > 3 or version < 0:
            print()
            print("INVALID CHOICE PLEASE TRY AGAIN")
            return False
        if cmd == 1:
            rfc_no = int(input("\n[INPUT] \n ENTER RFC NUMBER:"))
            self.Lookup(rfc_no,version)
            print('[LOOKUP]      REQUEST SENT')
            data = self.sock.recv(100000).decode("utf-8")
            print()
            print("[LOOKUP]      RESPONSE")
            print(data)
        if cmd == 2:
            self.List(version)
            print('[LIST]      REQUEST SENT')
            data = self.sock.recv(100000).decode("utf-8")
            print()
            print("[LIST]      RESPONSE")
            print(data)
        if cmd == 3:
            rfc_no = int(input("\n[INPUT] \n ENTER RFC NUMBER:"))
            rfc_title = input("\n[INPUT] \n ENTER RFC TITLE:")
            rfc_content = input("\n[INPUT] \n ENTER RFC CONTENT:")
            self.Add(rfc_no,rfc_title,rfc_content,mod,len(rfc_content),"text/text",version)
            print('[ADD]      REQUEST SENT')
            data = self.sock.recv(100000).decode("utf-8")
            print()
            print("[ADD]      RESPONSE")
            print(data)
        if cmd == 4:
            rfc_no = int(input("\n[INPUT] \n ENTER RFC NUMBER:"))
            rfc_host = input("\n[INPUT] \n ENTER HOSTNAME:")
            rfc_port = int(input("\n[INPUT] \n ENTER PORT NUMBER:"))
            self.Get(rfc_no,rfc_host,rfc_port,version)
            print('[GET]      REQUEST SENT')
            data = self.get_sock.recv(100000).decode("utf-8")
            print()
            print("[GET]      RESPONSE")
            print(data)
            rfc_no,rfc_title,rfc_content,mod,rfc_length,rfc_type,version = self.AddGet(data)
            self.Add(rfc_no,rfc_title,rfc_content,mod,rfc_length,rfc_type,version)
            print('[ADD]      REQUEST SENT')
            data = self.sock.recv(100000).decode("utf-8")
            print()
            print("[ADD]      RESPONSE")
            print(data)
        return True

    def Add(self, rfc_no , rfc_title , rfc_content, mod,  rfc_length, rfc_type, v):
        self.RFC_list.loc[len(self.RFC_list)] = [str(rfc_no),rfc_title,rfc_content,mod,str(rfc_length),rfc_type,v]
        s = "ADD RFC-" + str(rfc_no) + " P2PCI/" + str(v) + "\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "\nTitle:" + str(rfc_title) + "|"
        # print(s)
        # print()
        data = bytes(s, 'utf-8')
        self.sock.sendall(data)

    def Lookup(self,rfc_no,v):
        s = "LOOKUP RFC-" + str(rfc_no) + " P2PCI/" + str(v) + "\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "|"
        # print(s)
        data = bytes(s, 'utf-8')
        self.sock.sendall(data)
        
    def List(self,v):
        s = "LIST ALL" + " P2PCI/" + str(v) + "\nHost:" + str(self.HOSTNAME) + "\nPort:" + str(self.PORT) + "|"
        # print(s)
        data = bytes(s, 'utf-8')
        self.sock.sendall(data)
        
    def Get(self,rfc_no,get_host,get_port,v):
        self.get_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.get_sock.connect((get_host, get_port))
        s = "GET RFC-" + str(rfc_no) + " P2PCI/" + str(v) + "\nHost:" + str(get_host) + "\nOS:" + str(self.OS) + "|"
        # print(s)
        data = bytes(s, 'utf-8')
        self.get_sock.sendall(data)
        # self.get_sock.close()
    
    def Logout(self):
        s = "CLOSE\nHost:" + str(self.HOSTNAME) + "|"
        data = bytes(s, 'utf-8')
        try:
            self.sock.sendall(data)
        except:
            return
        
    def RFC_listen(self):
        self.sock_rfc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_rfc.bind((self.HOSTNAME, self.PORT))
        self.sock_rfc.listen()
        while True:
            conn, addr = self.sock_rfc.accept()
            thread = threading.Thread(target=self.Send, args=(conn, addr))
            thread.start()

    def Send(self,conn,addr):
        data = conn.recv(100000).decode("utf-8")
        commands = data.split("|")
        for comd in commands[:-1]:
            cmd = comd.split("\n")   
            if cmd[0].split(" ")[0] == "GET":
                resp = self.SendRFC(cmd)
                # print()
                # print(resp)
                r_data = bytes(resp, 'utf-8')
                conn.sendall(r_data)
        conn.close()
        # print()
        # print("\n[INPUT] \n 1. LOOKUP | 2.LIST | 3.ADD | 4.GET | 5.QUIT\n  SELECT COMMAND:")
    
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
            resp += "Date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S") + " GMT" + "\n"
            resp += "OS: " + self.OS + "\n"
            resp += "Last-Modified: " + str(s_rfc[3]) + "\n"
            resp += "Content-Length: " + str(s_rfc[4]) + "\n"
            resp += "Content-Type: " + str(s_rfc[5]) + "\n"
            resp += "DATA: RFC " + str(s_rfc[0]) + " / " + str(s_rfc[1]) + "|\n"
            resp += "{" + str(s_rfc[2]) + "}"
        elif len(send_rfc) == 0:
            code = 404
            resp = v + " " + str(code) + " " + self.errors[code] + "\n"
        return resp
    
    def AddGet(self,data):
        data = data.split("\n")
        v = data[0].split(" ")[0].split("/")[1]
        mod = data[1].split(":",1)[1][1:]
        rfc_length = data[4].split(":",1)[1][1:]
        rfc_type = data[5].split(":",1)[1][1:]
        rfc_no = data[6].split(":",1)[1].split(" / ")[0][1:].split(" ")[1]
        rfc_title = data[6].split(":",1)[1].split(" / ")[1]
        rfc_content = data[7][1:-1]
        self.RFC_list.loc[len(self.RFC_list)] = [str(rfc_no),rfc_title,rfc_content,mod,str(rfc_length),rfc_type,v]
        print("[ADD]    RFC ADDED TO SYSTEM")
        return rfc_no,rfc_title,rfc_content,mod,rfc_length,rfc_type,v
        
        
        
        
        
    

