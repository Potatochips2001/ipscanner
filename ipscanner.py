#!/usr/bin/env python3
import socket
import threading
import math
import sys

openAddresses = []

if len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
    exit(f"{__file__} [first 3 octets] [port] [timeout (ms)]")

if len(sys.argv) >= 2:
    ipRange = sys.argv[1]
    ipPort = int(sys.argv[2])
    ipTimeout = int(sys.argv[3])
else:
    ipRange = input("First 3 octets of IPv4: ")
    ipPort = int(input('Port: '))
    ipTimeout = int(input('Time to wait for connection (ms): '))

if ipRange.endswith('.') == False:
    ipRange += '.'


def scan(currentRange, _timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        currentAddress = f'{ipRange}{currentRange}'
        sock.settimeout(_timeout/1000)
        sock.connect((f'{currentAddress}', ipPort))
        print(f'{currentAddress}:{ipPort} OPEN')
        openAddresses.append(currentAddress)
    except KeyboardInterrupt:
        print('\nTerminating script.')
        exit(openAddresses)
    except:
        print(f'{currentAddress}:{ipPort} CLOSED')


_threads = []
for i in range(256):
    t = threading.Thread(target=scan, daemon=True, args=[i, ipTimeout])
    _threads.append(t)
for i in range(256):
    _threads[i].start()
for i in range(256):
    _threads[i].join()

percentageOpen = math.floor(len(openAddresses)/256*100)

print('\nPrinting open addresses\n\n')

print(', '.join(openAddresses))

print(f'\n({percentageOpen}%)\n')
