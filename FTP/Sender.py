from Reciever import PROB_LOSS_SERVICE
from client import Client
import socket
import sys
import time
import matplotlib.pyplot as plt

HOSTNAME = socket.gethostname()
PORT = 8081

# NORMAL GO_BACK_N

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
# C1.file_detail()
# C1.rdt_send()


# TASK 1

SERVER_HOST = 'Aayushs-MBP.lan'
SERVER_PORT = 7735
FILE_INPUT = 'input.txt'
MSS = 500

average_delay = []
N_LIST = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
for N in N_LIST:
    delay = []
    for i in range(5):
        print(f"SEND FILE: ITERATION {i+1}")

        C1 = Client(HOSTNAME, PORT, SERVER_HOST, SERVER_PORT, FILE_INPUT, N, MSS)
        print(C1)
        C1.file_detail()

        start_time = time.time()
        C1.rdt_send()
        end_time = time.time()
        print(f"[SENDER] {N} : {end_time-start_time}")

        delay.append(end_time - start_time)
    print(f"{N}: {delay}")
    average_delay.append(sum(delay)/5)
print(average_delay)

canvas = plt.figure(figsize=(12,7))
plt.xlabel("N Value")
plt.ylabel("Data Transfer Delay")
plt.title("N vs Transfer Delay")
plt.plot(N_LIST, average_delay, color = "blue", marker = 'o')
plt.savefig('N vs Transfer Delay.png')


# # TASK 2

SERVER_HOST =  'Aayushs-MBP.lan'
SERVER_PORT = 7735
FILE_INPUT = 'input.txt'
N = 64

average_delay = []
MSS_LIST = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
for MSS in MSS_LIST:
    delay = []
    
    for i in range(5):
        print(f"SEND FILE: ITERATION {i+1}")

        C1 = Client(HOSTNAME, PORT, SERVER_HOST, SERVER_PORT, FILE_INPUT, N, MSS)
        print(C1)
        C1.file_detail()

        start_time = time.time()
        C1.rdt_send()
        end_time = time.time()
        print(f"[SENDER] {i+1} {MSS} : {end_time-start_time}")

        delay.append(end_time - start_time)
    print(delay)
    average_delay.append(sum(delay)/5)

print(average_delay)
# figure = plt.figure

canvas = plt.figure(figsize=(12,7))
plt.xlabel("MSS Value")
plt.ylabel("Data Transfer Delay")
plt.title("MSS vs Transfer Delay")
plt.plot(MSS_LIST, average_delay, color = "blue", marker = 'o')
plt.savefig('MSS vs Transfer Delay.png')



# # TASK 3

SERVER_HOST =  'Aayushs-MBP.lan'
SERVER_PORT = 7735
FILE_INPUT = 'input.txt'
N = 64
MSS = 500

average_delay = []
# N_LIST = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
# MSS_LIST = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
PROB_LOSS_SERVICE_LIST = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
for i in PROB_LOSS_SERVICE_LIST:
    delay = []
    for j in range(5):
        print(f"SEND FILE: PROBLOSS {i} {j+1}")
        C1 = Client(HOSTNAME, PORT, SERVER_HOST, SERVER_PORT, FILE_INPUT, N, MSS)
        print(C1)
        C1.file_detail()

        start_time = time.time()
        C1.rdt_send()
        end_time = time.time()

        delay.append(end_time - start_time)

    print(delay)
    average_delay.append(sum(delay)/5)

print(average_delay)

canvas = plt.figure(figsize=(12,7))
plt.xlabel("PROB_LOSS Value")
plt.ylabel("Data Transfer Delay")
plt.title("PROB_LOSS vs Transfer Delay")
plt.plot(PROB_LOSS_SERVICE, average_delay, color = "blue", marker = 'o')
plt.savefig('PROB_LOSS vs Transfer Delay.png')