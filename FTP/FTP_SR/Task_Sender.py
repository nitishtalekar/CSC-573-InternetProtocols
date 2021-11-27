import matplotlib.pyplot as plt
import time
from client import Client
import socket
import csv

# TASK 1
def TASK_1():
    print("\n\n-------------TASK 1-------------\n\n")

    HOSTNAME = socket.gethostname()
    PORT = 8081
    SERVER_HOST = socket.gethostname()
    SERVER_PORT = 7735
    FILE_INPUT = 'data/input.txt'
    MSS = 500

    average_delay = []
    list_of_delays = {}
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

        list_of_delays[N] = delay
        average_delay.append(sum(delay)/5)

    print(f"\nList of Delays: \n{list_of_delays}")
    print(f"Average Delays : {average_delay}")

    list_of_delays["Average"] = average_delay
    with open('N_Delay.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in list_of_delays.items():
            writer.writerow([key, value])

    canvas = plt.figure(figsize=(12,7))
    plt.xlabel("N Value")
    plt.ylabel("Data Transfer Delay")
    plt.title("N vs Transfer Delay")
    plt.plot(N_LIST, average_delay, color = "blue", marker = 'o')
    plt.savefig('output/N vs Transfer Delay.png')


# # # TASK 2
def TASK_2():
    print("\n\n-------------TASK 2-------------\n\n")

    HOSTNAME = socket.gethostname()
    PORT = 8081
    SERVER_HOST =  socket.gethostname()
    SERVER_PORT = 7735
    FILE_INPUT = 'data/input.txt'
    N = 64

    average_delay = []
    list_of_delays = {}
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

        list_of_delays[MSS] = delay
        average_delay.append(sum(delay)/5)

    print(f"\nList of Delays: \n{list_of_delays}")
    print(f"Average Delays : {average_delay}")

    list_of_delays["Average"] = average_delay
    with open('MSS_Delay.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in list_of_delays.items():
            writer.writerow([key, value])


    canvas = plt.figure(figsize=(12,7))
    plt.xlabel("MSS Value")
    plt.ylabel("Data Transfer Delay")
    plt.title("MSS vs Transfer Delay")
    plt.plot(MSS_LIST, average_delay, color = "blue", marker = 'o')
    plt.savefig('output/MSS vs Transfer Delay.png')



# # # TASK 3
def TASK_3():
    print("\n\n-------------TASK 3-------------\n\n")

    HOSTNAME = socket.gethostname()
    PORT = 8081
    SERVER_HOST =  socket.gethostname()
    SERVER_PORT = 7735
    FILE_INPUT = 'data/input.txt'
    N = 64
    MSS = 500

    average_delay = []
    list_of_delays = {}
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

        list_of_delays[i] = delay
        average_delay.append(sum(delay)/5)

    print(f"\nList of Delays: \n{list_of_delays}")
    print(f"Average Delays : {average_delay}")
    list_of_delays["Average"] = average_delay
    with open('ProbLoss_Delay.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in list_of_delays.items():
            writer.writerow([key, value])

    canvas = plt.figure(figsize=(12,7))
    plt.xlabel("PROB_LOSS Value")
    plt.ylabel("Data Transfer Delay")
    plt.title("PROB_LOSS vs Transfer Delay")
    plt.plot(PROB_LOSS_SERVICE_LIST, average_delay, color = "blue", marker = 'o')
    plt.savefig('output/PROB_LOSS vs Transfer Delay.png')



TASK_1()
TASK_2()
TASK_3()