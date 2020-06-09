import socket
import time
import datetime
import sys
import subprocess
import binascii
import select

import gg2.constants as gg2const
import gg2.network.util as net
from gg2.network.receivehandler import ReceiveHandler
from gg2.game import game

class GG2Connector():
    joined = False
    playerID = None
    
    clazz = None
    team = None
    
    recv_handler = ReceiveHandler()
    
    def connect(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(3)
        self.socket.connect((ip, port))
        
    def close(self):
        self.joined = False
        self.playerID = None
        self.socket.close()
        
    def send_hello(self):
        self.socket.send(gg2const.MAGIC_HELLO)
        return self.socket.recv(1024)
        
    def reserve_slot(self, name=""):
        name_bytes = bytearray(name, "utf-8")
        
        self.socket.send(bytes([gg2const.RESERVE_SLOT]))
        self.socket.send(bytes([len(name_bytes)]))
        self.socket.send(name_bytes)
        
        return self.socket.recv(1024)
        
    def join(self):
        self.socket.send(bytes([gg2const.PLAYER_JOIN]))
        header = net.read_ubyte(self.socket)
        self.joined = True
        self.recv_handler.handle(header, self.socket)
        
    def change_team(self, team):
        self.socket.send(bytes([gg2const.PLAYER_CHANGETEAM]))
        self.socket.send(bytes([team]))
        
    def change_class(self, clazz):
        self.socket.send(bytes([gg2const.PLAYER_CHANGECLASS]))
        self.socket.send(bytes([clazz]))
        
    def receive_update(self):
        r, w, err = select.select([self.socket], [], [])
        if r:
            header = net.read_ubyte(self.socket)
            print("GG2Connector Received", header)
            
            if not self.recv_handler.handle(header, self.socket):
                print("GG2Connector recv_handler handle failed")
                data = self.socket.recv(65535) # discard rest
                print(data)