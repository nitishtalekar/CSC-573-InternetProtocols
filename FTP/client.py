import socket
import time
import os

class Client:
    def __init__(self, HOSTNAME, PORT, SERVER_HOST, SERVER_PORT, FILE_INPUT, N, MSS):
        self.HOSTNAME = HOSTNAME
        self.PORT = PORT
        self.SERVER_HOST = SERVER_HOST
        self.SERVER_PORT = SERVER_PORT
        self.FILE_PATH = FILE_INPUT
        self.N = N
        self.MSS = MSS
        self.BUFFER = []
        self.DATA_TYPE = '0101010101010101'
        self.ACK_TYPE = '1010101010101010'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.FILE_INPUT = open(self.FILE_PATH, "rb")
        except:
            print('FILE NOT FOUND')
        self.SEQ_NO = 0
        self.WINDOW = []
        self.WINDOW_SIZE = N
        self.WINDOW_TIMEOUT = []
        self.TIMEOUT = 3

    def __str__(self):
        return f'[CLIENT] {self.HOSTNAME} running on Port: {self.PORT} \n[CLIENT] Transmitting File:{self.FILE_INPUT}\n[CLIENT] To Server: {self.SERVER_HOST}:{self.SERVER_PORT}\n'
    
    def file_detail(self):
        print(f'[CLIENT] SENDING FILE: {self.FILE_PATH} of SIZE: {os.path.getsize(self.FILE_PATH)} Bytes\n\n')
    
    def carry_around_add(self, x, y):
        return ((x+y) & 0xffff) + ((x + y) >> 16)

    def checksum_computation(self, message):
        add = 0
        for i in range(0, len(message) - len(message) % 2, 2):
            message = str(message)
            w = ord(message[i]) + (ord(message[i + 1]) << 8)
            add = self.carry_around_add(add, w)
        return ~add & 0xffff

    def send_packet(self, data):
        self.sock.sendto(str.encode(data), (self.SERVER_HOST, self.SERVER_PORT))

    def retransmit(self):
        # print("RETRANSMITTING WINDOW")
        self.WINDOW_TIMEOUT = []
        for data in self.WINDOW:
            # print(f"Resending : {data[:32]}\t :{int(data[:32],2)}")
            self.send_packet(data)
            self.WINDOW_TIMEOUT.append(time.time())

    def rdt_send(self):
        data = self.FILE_INPUT.read(self.MSS)
        while data or len(self.WINDOW) != 0:
            if data and len(self.WINDOW) < self.WINDOW_SIZE :
                h_seq_no = str(f'{self.SEQ_NO:032b}')
                h_type = str(self.DATA_TYPE)
                h_checksum = self.checksum_computation(h_seq_no + h_type + data.decode())
                h_checksum = str(f'{h_checksum:016b}')
                header = h_seq_no + h_checksum + h_type

                # print(h_seq_no + h_type + data.decode())
                # print("SENDING")
                # print(f'SEQUENCE NO: {h_seq_no}')
                # print(f'HEADER CHECKSUM: {h_checksum}')
                # print(f'HEADER TYPE: {h_type}')
                # print(f'DATA: {data.decode()}')

                data = header + data.decode()

                self.send_packet(data)
                self.WINDOW.append(data)
                self.WINDOW_TIMEOUT.append(time.time())
                self.SEQ_NO += 1
                data = self.FILE_INPUT.read(self.MSS)
            
            self.sock.settimeout(1)
            try:
                ACK, addr = self.sock.recvfrom(1024)
                # print(f'ACK: {ACK}')
                self.sock.settimeout(0.01)
            except Exception as e:
                # print(e)
                if len(self.WINDOW_TIMEOUT) > 0:
                    # print("RETRANSMITTING 1")

                    if (time.time() - self.WINDOW_TIMEOUT[0]) > self.TIMEOUT:
                        packet_timed_out = self.WINDOW[0]
                        # seq_no = packet_timed_out
                        print(f'[CLIENT] Packet Timeout: {int(packet_timed_out[:32], 2)}')
                        # print("RETRANSMITTING 2")
                        self.retransmit()
                continue

            try:
                # print(f"MUST RECIEVE ACK for Packet: {int(self.WINDOW[0][:32], 2)}")
                ACK = ACK.decode()
                # print(ACK[48:64])
                if ACK[48:64] == self.ACK_TYPE:
                    # while len(self.WINDOW) > 0 and self.WINDOW[0][:32] <= ACK[:32]:
                    if self.WINDOW[0][:32] == ACK[:32]:
                        # print(f'\n\n{self.WINDOW}')
                        self.WINDOW.remove(self.WINDOW[0])
                        # print(self.WINDOW)
                        self.WINDOW_TIMEOUT.remove(self.WINDOW_TIMEOUT[0])
            except:
                continue
        
        data = "EOF"
        self.send_packet(data)
        print("\n[CLIENT] FILE TRANSFER COMPLETED")
        self.sock.close()
        self.FILE_INPUT.close()




# HOSTNAME = socket.gethostname()
# PORT = 8081

# if len(sys.argv) > 1:
#     # FROM COMMAND LINE
#     SERVER_HOST = sys.argv[1]
#     SERVER_PORT = int(sys.argv[2])
#     FILE_INPUT = sys.argv[3]
#     N = int(sys.argv[4])
#     MSS = int(sys.argv[5])
# else:
#     SERVER_HOST = 'Aayushs-MBP.lan'
#     SERVER_PORT = 7735
#     FILE_INPUT = 'input.txt'
#     N = 8
#     MSS = 512

# C1 = Client(HOSTNAME, PORT, SERVER_HOST, SERVER_PORT, FILE_INPUT, N, MSS)
# print(C1)
# C1.rdt_send()