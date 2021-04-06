# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:47:05 2021

@author: nikol
"""

import socket
import threading
import cv2

class Tello:
    def __init__(self):
        self.flag=True
        host = ''
        port = 9000
        locaddr = (host,port) 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(locaddr)
        
        self.video=cv2.VideoCapture("udp://@0.0.0.0:11111")
        print("Inicijalizovan")
        
    def terminate(self):
        self.flag=False
        self.sock.close()
        self.video.release()
        cv2.destroyAllWindows()
        
        
    def receive(self):
        while self.flag:
            try:
                data,server= self.sock.recvfrom(1024)
                print(data.decode(encoding="utf-8"))
            except Exception:
                print('\n Greska u primanju poruke!')

    def video_stream(self):
        while self.flag:
            try:
                ret, frame=self.video.read()
                if ret:
                    print('Usao')
                    height, width=frame.shape
                    new_h=int(height/2)
                    new_w=int(width/2)
                    
                    new_frame=cv2.resize(frame,(new_w,new_h))
                    cv2.imshow('Tello',new_frame)
                    cv2.waitKey(1)
            except Exception:
                print('\n Greska u video prenosu!')
                
    def send(self, command):
        tello_address = ('192.168.10.1', 8889)
        command=command.encode(encoding="utf-8")
        self.sock.sendto(command,tello_address)
            
t=Tello()
recvThread=threading.Thread(target=t.receive)
videoThread=threading.Thread(target=t.video_stream)

recvThread.start()
videoThread.start()

while True:
    try:
        msg=input()
        t.send(msg)
        
        
        if msg=="kill":
            t.teriminate()
            recvThread.join()
            videoThread.join()
            print("Kraj")
            break
    except KeyboardInterrupt:
        t.terminate()
        recvThread.join()
        videoThread.join()
        break
            
        
    