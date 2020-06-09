import socket
import time
import datetime
import sys
import subprocess
import binascii

class AutoRestarter():
    SERVER_IP = 'localhost' # shouldn't need to change this
    SERVER_PORT = 8190		 # this is your gg2 port
        
    def run(self):
        self.bots = []
        prev_team = GG2Connector.TEAM_BLUE
        for i in range(self.BOT_COUNT):
            print("[{}] Check".format(i))
            gg2connector = GG2Connector()
            gg2connector.connect(self.SERVER_IP, self.SERVER_PORT)
            data = gg2connector.send_hello()
            print("   Sent hello {}".format(data))
            data = gg2connector.reserve_slot("bot{}".format(i))
            print("   Reserved {}".format(binascii.hexlify(data)))
            if data == GG2Connector.SERVER_FULL:
                print("   Couldn't reserve, was full.")
                gg2connector.close()
                break
            else:
                data = gg2connector.join()
                print("   Joined {}".format(data))
                playerID = gg2connector.playerID
                if prev_team == GG2Connector.TEAM_BLUE:
                    next_team = GG2Connector.TEAM_RED
                else:
                    next_team = GG2Connector.TEAM_BLUE
                prev_team = next_team
                gg2connector.change_team(next_team)
            self.bots.append(gg2connector)
        
        
class Client():
    MAGIC_HELLO = bytearray.fromhex('006d20cbb64ead822125a12ec1ca982037')
    SERVER_FULL = bytearray.fromhex('0b')
    RESERVE_SLOT = bytearray.fromhex('3c')
    PLAYER_JOIN = bytearray.fromhex('01')
    PLAYER_CHANGETEAM = bytearray.fromhex('03')
    PLAYER_CHANGECLASS = bytearray.fromhex('04')
    
    TEAM_RED = bytearray.fromhex('00')
    TEAM_BLUE = bytearray.fromhex('01')
    TEAM_SPECTATOR = bytearray.fromhex('02')
    TEAM_ANY = bytearray.fromhex('03')
    CLASS_SCOUT = bytearray.fromhex('00')
    CLASS_SOLDIER = bytearray.fromhex('01')
    CLASS_SNIPER = bytearray.fromhex('02')
    CLASS_DEMOMAN = bytearray.fromhex('03')
    CLASS_MEDIC = bytearray.fromhex('04')
    CLASS_ENGINEER = bytearray.fromhex('05')
    CLASS_HEAVY = bytearray.fromhex('06')
    CLASS_SPY = bytearray.fromhex('07')
    CLASS_PYRO = bytearray.fromhex('08')
    CLASS_QUOTE = bytearray.fromhex('09')
    
    joined = False
    playerID = None
    
    clazz = None
    team = None
    
    
    def connect(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(3)
        self.socket.connect((ip, port))
        
    def close(self):
        self.joined = False
        self.playerID = None
        self.socket.close()
        
    def send_hello(self):
        self.socket.send(self.MAGIC_HELLO)
        return self.socket.recv(1024)
        
    def reserve_slot(self, name=""):
        name_bytes = bytearray(name, "utf-8")
        bytelen = bytes([len(name_bytes)])
        
        self.socket.send(self.RESERVE_SLOT)
        self.socket.send(bytelen)
        self.socket.send(name_bytes)
        
        return self.socket.recv(1024)
        
    def join(self):
        self.socket.send(self.PLAYER_JOIN)
        data = self.socket.recv(1024)
        self.joined = True
        self.playerID = data[1]
        return data
        
    def change_team(self, team):
        self.socket.send(self.PLAYER_CHANGETEAM)
        self.socket.send(team)
        
    def change_class(self, clazz):
        self.socket.send(self.PLAYER_CHANGECLASS)
        self.socket.send(clazz)

if __name__ == "__main__":
    print("Auto relauncher started.")
    ar = AutoRestarter()
    ar.run()