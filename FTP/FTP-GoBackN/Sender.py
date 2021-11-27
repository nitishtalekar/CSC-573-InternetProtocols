from client import Client
import socket
import sys

# RUN USING:  
# ->  python Sender.py <SERVER_HOST> 7735 data/input.txt <N> <MSS>
# Eg. python Sender.py Aayushs-MBP.lan 7735 data/input.txt 8 512

# # NORMAL GO_BACK_N
HOSTNAME = socket.gethostname()
PORT = 8081

if len(sys.argv) > 1:
    # FROM COMMAND LINE
    SERVER_HOST = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
    FILE_INPUT = sys.argv[3]
    N = int(sys.argv[4])
    MSS = int(sys.argv[5])
else:
    SERVER_HOST = socket.gethostname()
    SERVER_PORT = 7735
    FILE_INPUT = 'data/input.txt'
    N = 8
    MSS = 512

C1 = Client(HOSTNAME, PORT, SERVER_HOST, SERVER_PORT, FILE_INPUT, N, MSS)
print(C1)
C1.file_detail()
C1.rdt_send()


