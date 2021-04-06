# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 02:07:03 2020

@author: nikol
"""


import threading 
import socket
import sys
import time
import platform  
import speech_recognition as sr



global levo_desno_osa
levo_desno_osa=0

global napred_nazad_osa
napred_nazad_osa=0


host = ''
port = 9000
locaddr = (host,port) 


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(locaddr)

#-----------------Pocetak RTH----------------------
# Definisanje funkcija koriscenih za RTH

def go_forward(vrednost):
    global napred_nazad_osa
    napred_nazad_osa=napred_nazad_osa+vrednost

def go_back(vrednost):
    global napred_nazad_osa
    napred_nazad_osa=napred_nazad_osa-vrednost

def go_right(vrednost):
    global levo_desno_osa
    levo_desno_osa=levo_desno_osa+vrednost
    
def go_left(vrednost):
    global levo_desno_osa
    levo_desno_osa=levo_desno_osa-vrednost

def RTH():
    global levo_desno_osa
    global napred_nazad_osa
    try: 
        
        if napred_nazad_osa<0:
            fb='forward '+str(-napred_nazad_osa)
        else:
            fb='back '+str(napred_nazad_osa)
        
        print(fb)    
        fb = fb.encode(encoding="utf-8") 
        sent = sock.sendto(fb, tello_address)
        time.sleep(3)
        if levo_desno_osa<0:
            lr='right '+str(-levo_desno_osa)
        else:
            lr='left '+str(levo_desno_osa)
        
        print(lr)
        lr = lr.encode(encoding="utf-8") 
        sent = sock.sendto(lr, tello_address)
        time.sleep(3)
        print('Zapoceo RTH')
        landing='land'
        landing = landing.encode(encoding="utf-8") 
        sent = sock.sendto(landing, tello_address)
        
        levo_desno_osa=0
        napred_nazad_osa=0
 
    except KeyboardInterrupt:
       print ('\n . . .\n')
       sock.close() 
            
#--------------------KRAJ RTH--------------------------



def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


print ('\r\n\r\nTello Python3 Demo.\r\n')

print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

print ('end -- quit demo.\r\n')


#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()


while True: 
    try:
        python_version = str(platform.python_version())
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
        
      
        broj_reci=0
        for word in msg.split():
            broj_reci=broj_reci+1
            
            if word.isdigit():
                broj=int(word);
                print(broj);
            else :
                komanda=word;
                
        
        #Odredjivanje koja  je komanda u pitanju
        #nema svrhe u koliko nema vise od jedne reci
        if broj_reci>1:
            
            if komanda=='forward':
                go_forward(broj)
                
            if komanda=='back':
                go_back(broj)
                
            if komanda=='right':
                go_right(broj)
                
            if komanda=='left':
                go_left(broj)
                
        if komanda=='RTH':
            RTH()
        else: # Send data
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  
        break



# =============================================================================
# 
# while True:
#     try:
#         msg = input("Unesi komandu sad:  ");
#         #msg = msg.encode(encoding="utf-8") 
#         print(msg);
#         broj_reci=0
#         for word in msg.split():
#             broj_reci=broj_reci+1
#             if word.isdigit():
#                 broj=int(word);
#                 print(broj);
#         
#         if broj_reci>1:
#             print("tacno")
#             
#     except KeyboardInterrupt:
#         print ('\n . . .\n')
#         # Ovime se prekida veza
#         break
# =============================================================================
