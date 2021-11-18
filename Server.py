import socket
import pandas as pd
import threading
import signal
import os
import time

host = '127.0.0.1'
port = 7734

class Server:
    def __init__(self):
        self.PORT = 7734
        self.RFC_Table = pd.DataFrame(columns = ["RFC", "TITLE", 'HOSTNAME',"PORT"])
        self.Peers = pd.DataFrame(columns = ['HOSTNAME', 'PORT'])
        self.errors = {200:"OK",400:"Bad Request",404:"Not Found",500:"P2PCI version not supported"}
        
    def signal_handler(sig, frame):
        os._exit(0)

    def Active(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()
        
        run = True
        while run:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.ClientConnected, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS]    {threading.activeCount() - 1}")
            
    def ClientConnected(self,conn,addr):
        while True:
            data = conn.recv(100000).decode("utf-8")
            if data == "Q":
                run_loop = False
                break
            commands = data.split("|")[:-1]
            resp = ""
            for comd in commands:
                cmd = comd.split("\n")
                if cmd[0] == 'ACTIVE':
                    print("[ACTIVE]     REQUEST")
                    resp = self.AddPeer(cmd)
                if cmd[0] == 'CLOSE':
                    print("[CLOSE]     REQUEST")   
                    resp = self.ClosePeer(cmd)                 
                if cmd[0].split(" ")[0] == "ADD":
                    print("[ADD]     REQUEST")
                    resp = self.AddRFC(cmd)
                    # print(resp)                
                if cmd[0].split(" ")[0] == "LOOKUP":
                    print("[LOOKUP]     REQUEST")
                    resp = self.LookUp(cmd)
                    # print(resp)            
                if cmd[0].split(" ")[0] == "LIST":
                    print("[LIST]     REQUEST")
                    resp = self.RFCList(cmd)
                    # print(resp)
                r_data = bytes(resp, 'utf-8')
                conn.sendall(r_data)
                print(comd)
                print()
        conn.close()
        
    def ClosePeer(self, cmd):
        h = cmd[1].split(":")[1]
        self.Peers = self.Peers[self.Peers.HOSTNAME != h]
        self.RFC_Table = self.RFC_Table[self.RFC_Table.HOSTNAME != h]
        code = 200
        resp = str(code) + " " + self.errors[code] + "\n"
        resp += "CONNECTION CLOSED"
        return resp
        
    def AddPeer(self, cmd):
        h = cmd[1].split(":")[1]
        p = cmd[2].split(":")[1]
        self.Peers.loc[len(self.Peers)] = [h,p]
        code = 200
        resp = str(code) + " " + self.errors[code] + "\n"
        resp += "CONNECTED TO SERVER"
        return resp
    
    def AddRFC(self,cmd):
        rfc = cmd[0].split(" ")[1].split("-")[1]
        v = cmd[0].split(" ")[2]
        h = cmd[1].split(":")[1]
        p = cmd[2].split(":")[1]
        title = cmd[3].split(":")[1]
        code = 200
        resp = v + " " + str(code) + " " + self.errors[code] + "\n"
        resp += "RFC " + str(rfc) + " " + str(title) + " " + str(h) + " " + str(p)
        self.RFC_Table.loc[len(self.RFC_Table)] = [rfc,title,h,p]
        return resp

    def LookUp(self,cmd):
        rfc = cmd[0].split(" ")[1].split("-")[1]
        v = cmd[0].split(" ")[2]
        h = cmd[1].split(":")[1]
        p = cmd[2].split(":")[1]
        lookup_rfc = self.RFC_Table.loc[self.RFC_Table['RFC'] == rfc]
        resp = ""
        if len(lookup_rfc) > 0:
            code = 200
            resp = v + " " + str(code) + " " + self.errors[code] + "\n"
            for row in lookup_rfc.values:
                 resp += "RFC " + str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + str(row[3]) + "\n"
        elif len(lookup_rfc) == 0:
            code = 404
            resp = v + " " + str(code) + " " + self.errors[code] + "\n"
        return resp

    def RFCList(self,cmd):
        lookup_rfc = self.RFC_Table
        v = cmd[0].split(" ")[2]
        if len(lookup_rfc) > 0:
            code = 200
            resp = v + " " + str(code) + " " + self.errors[code] + "\n"
            for row in lookup_rfc.values:
                 resp += "RFC " + str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + str(row[3]) + "\n"
        return resp


S1 = Server()
S1.Active()