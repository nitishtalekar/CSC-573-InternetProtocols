import signal
import sys

def signal_handler(sig, frame):
    print("HELLLO")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

x = 0
while True:
    x += 1
print('Press Ctrl+C')