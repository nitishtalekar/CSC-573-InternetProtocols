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

# TASK 1
print("\n\n-------------TASK 1-------------\n\n")
PORT = 7735
FILE_OUTPUT = 'output.txt'
PROB_LOSS_SERVICE = 0.05
for i in range(11):
    for j in range(5):
        print(f"RECIEVING FILE: ITERATION {j+1}")
        S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
        S1.rdt_rcv()
        S1.sock.close()
        print("\n\n\n")

# TASK 2
print("\n\n-------------TASK 2-------------\n\n")
PORT = 7735
FILE_OUTPUT = 'output.txt'
PROB_LOSS_SERVICE = 0.05
for i in range(10):
    for j in range(5):
        print(f"RECIEVING FILE: ITERATION {j+1}")
        S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
        S1.rdt_rcv()
        S1.sock.close()
        print("\n\n\n")


# TASK 3
print("\n\n-------------TASK 3-------------\n\n")
PORT = 7735
FILE_OUTPUT = 'output.txt'
PROB_LOSS_SERVICE_LIST = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
# PROB_LOSS_SERVICE = 0.05
for PROB_LOSS_SERVICE in PROB_LOSS_SERVICE_LIST:
    for j in range(5):
        print(f"RECIEVING FILE: PROBLOSS {PROB_LOSS_SERVICE} {j+1}")
        S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
        S1.rdt_rcv()
        S1.sock.close()
        print("\n\n\n")