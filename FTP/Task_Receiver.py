from server import Server


# # TASK 1
def TASK_1():
    print("\n\n-------------TASK 1-------------\n\n")
    PORT = 7735
    FILE_OUTPUT = 'data/output.txt'
    PROB_LOSS_SERVICE = 0.05
    for i in range(11):
        for j in range(5):
            print(f"RECIEVING FILE: ITERATION {j+1}")
            S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
            S1.rdt_rcv()
            S1.sock.close()
            print("\n\n\n")

# # TASK 2
def TASK_2():
    print("\n\n-------------TASK 2-------------\n\n")
    PORT = 7735
    FILE_OUTPUT = 'data/output.txt'
    PROB_LOSS_SERVICE = 0.05
    for i in range(10):
        for j in range(5):
            print(f"RECIEVING FILE: ITERATION {j+1}")
            S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
            S1.rdt_rcv()
            S1.sock.close()
            print("\n\n\n")


# # TASK 3
def TASK_3():
    print("\n\n-------------TASK 3-------------\n\n")
    PORT = 7735
    FILE_OUTPUT = 'data/output.txt'
    PROB_LOSS_SERVICE_LIST = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    for PROB_LOSS_SERVICE in PROB_LOSS_SERVICE_LIST:
        for j in range(5):
            print(f"RECIEVING FILE: PROBLOSS {PROB_LOSS_SERVICE} {j+1}")
            S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
            S1.rdt_rcv()
            S1.sock.close()
            print("\n\n\n")


TASK_1()
TASK_2()
TASK_3()