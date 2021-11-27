from server import Server
import sys

# RUN USING:  
# ->  python Reciever.py 7735 data/output.txt <PROB_LOSS>
# Eg. python Reciever.py 7735 data/input.txt 0.01

if len(sys.argv) > 1:
    # FROM COMMAND LINE
    PORT = int(sys.argv[1])
    FILE_OUTPUT = sys.argv[2]
    PROB_LOSS_SERVICE = float(sys.argv[3])
else:
    PORT = 7735
    FILE_OUTPUT = 'data/output.txt'
    PROB_LOSS_SERVICE = 0.01

S1 = Server(PORT, FILE_OUTPUT, PROB_LOSS_SERVICE)
S1.rdt_rcv()
