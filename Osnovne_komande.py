# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 13:22:40 2020

@author: nikol
"""


import threading 
import socket
import sys
import time
import platform  

# formiranje adrese ovog kompjutera
host = ''
port = 9000
locaddr = (host,port) 

# formiranje adrese Tello drona
tello_address = ('192.168.10.1', 8889)

# Stvaranje veze pravljenjem objekta sock klase socket 
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# definisanje adrese servera na koji ce se kasnije povezati klijent
sock.bind(locaddr)

# fja recv
def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518) # vraca string,adresa
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


print ('\r\n\r\nTello Python3 Demo.\r\n')

print ('Tello: command takeoff land flip forward back left right \r\n  up down cw ccw speed speed?\r\n')

print ('end -- quit demo.\r\n')


#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

while True: 
    try:
        # Ovde se ispisuje koja je verzija Pythona u pitanju, kod mene je 3.7.3
        python_version = str(platform.python_version())
        # Odvaja se od ovog stringa samo pocetni broj i on se uzima, to je 3
        version_init_num = int(python_version.partition('.')[0]) 
       # print (version_init_num)
        if version_init_num == 3:
            msg = input("");
        elif version_init_num == 2:
            msg = raw_input("");
        
        if not msg:
            break  

        if 'end' in msg:
            print ('...')
            sock.close()  
            break

        # Send data
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print ('\n . . .\n')
        # Ovime se prekida veza 
        sock.close()  
        break
