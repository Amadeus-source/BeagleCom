#!/usr/bin/env python3
from threading import Thread
import socket,os
import Adafruit_BBIO.GPIO as GPIO
import time

LED = "P9_11"

os.chdir("../../recfil")

a=os.getcwd()
#print(a)

clients = []
buff = 4096

# implementing one server thread per client class

class Server(Thread):
    
    # initializing the socket
    # with needed parameters
    
    def __init__(self, name, socket, file = None):
        super().__init__(daemon=True)
        self.socket = socket
        self.name = name
        self.file = file
        
    # cleaning everything up after the job is done
        
    def _close(self):
        clients.remove(self.socket)
        self.socket.close()
        self.toggle()
        print(self.name + ' disconnected')
        
        
    # resolving the name for the file
    # if file with the same name already exists there
    
    def get_name(self, file_name):
        k = 1
        name1 = file_name.split('.')[0]
        name2 = file_name.split('.')[1]
        
        # incrementally trying out new names
        # until we bump on the name of the file
        # that does not exist yet
        
        while True:
            new_name = "{}_copy{}.{}".format(name1, k, name2)
            try:
                file = open(new_name, "r")
                file.close()
                k += 1
            except FileNotFoundError:
                return new_name
    
    # describing the actions for a running thread
        
    def run(self):
        while True:
            
            # receive a file name and sending it back
            # as an acknowledgement
            
            file_name = self.socket.recv(buff).decode()
            if file_name:
                self.socket.send(file_name.encode())
                
            # trying to open a file with recieved name
            # and if this file already exists
            # then we need ro resolve a new name for it
                
            try:
                self.file = open(file_name, "r")
                self.file.close()
                file_name = self.get_name(file_name) 
                
            # if file with recieved name doesnt exist
            # then we may use the recieved name and 
            # instantiate a file
            
            except FileNotFoundError:
                pass
                
            # instantiating the file
            
            self.file = open(file_name, "wb")
            
            # receive the file content
            # until its fully recieved
            
            msg = self.socket.recv(buff)
            while msg:
                self.file.write(msg)
                msg = self.socket.recv(buff)
                
            # cleaning everyhting up after the job is done
            # and finishing the thread
                
            self.file.close()
            #os.system('python dl.py')
            self._close()
            

            return
            
    def toggle(self):
        GPIO.setup(LED, GPIO.OUT)
        for i in range(2):
            GPIO.output(LED, 1)
            time.sleep(1)
            GPIO.output(LED, 0)
            time.sleep(1)

def main():
    
    # initializing variable for user counting
    
    next_name = 1
    
    # setting up the port number and buffer size
    
    server_port = int(input('Enter port : '))
    buff = 4096
    
    # initalizing the socket on IPv4 TCP protocol

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # binding server to the socket and listening to all
    # incomming traffic on a specified port

    s.bind((input('Enter host (ex:localhost): ').strip('()'), server_port))
    s.listen()
    print("Listening on port {}".format(server_port))
    
    # continuously receive file from different users
    
    while True:
        
        # getting information about the incoming client

        client_socket, client_address = s.accept()
        clients.append(client_socket)
        
        # assignming a name for the client
        
        name = "User {}".format(next_name)
        next_name += 1
        print("{} has connected as {}".format(client_address, name))
        
        # starting the thread that will recieve the file from the client
        
        Server(name, client_socket).start()
        
if __name__ == "__main__":
    main()

