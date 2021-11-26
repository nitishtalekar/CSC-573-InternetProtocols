from server import Server
import sys

# if len(sys.argv) > 1:
#     # FROM COMMAND LINE
#     PORT = int(sys.argv[1])
#     FILE_OUTPUT = sys.argv[2]
#     PROB_LOSS_SERVICE = float(sys.argv[3])
# else:
#     PORT = 7735
#     FILE_OUTPUT = 'output.txt'
#     PROB_LOSS_SERVICE = 0.01

# S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
# S1.rdt_rcv()


PORT = 7735
FILE_OUTPUT = 'output.txt'
PROB_LOSS_SERVICE = 0.05
for i in range(10):
    for j in range(5):
        print(f"RECIEVING FILE: ITERATION {i+1}")
        S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
        S1.rdt_rcv()
        S1.sock.close()
        print("\n\n\n")