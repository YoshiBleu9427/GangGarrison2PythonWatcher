
import gg2.network.util as net
import gg2.constants as gg2consts
        
from gg2.game import game
from gg2.objects.projectiles.mine import Mine

class Weapon():
    owner = None
    
    alarm = [0,0,0,0,0]
    
    display_fired_last = 0
    
    def __init__(self, owner):
        self.owner = owner
        
    def fire_hold(self):
        pass
        
    def fire_special(self):
        pass
        
    def fire(self):
        self.display_fired_last = 3
        
    def deserialize(self, socket, type):
        print("Weapon deserialize")
        self.readyToShoot = net.read_ubyte(socket)
        self.alarm[0] = net.read_ubyte(socket) #/global.delta_factor;
        
        
class Scattergun(Weapon):
    pass
        
class Flamethrower(Weapon):
    pass
        
class Rocketlauncher(Weapon):
    pass
        
class Minigun(Weapon):
    pass

class Minegun(Weapon):
    mines = []
    lobbed = 0
        
    def deserialize(self, socket, type):
        super().deserialize(socket, type)
        print("Minegun deserialize")
        self.lobbed = net.read_ubyte(socket)
        
        self.mines.clear()
        
        for i in range(self.lobbed):
            mine = Mine(self.owner)
            mine.deserialize(socket, type)
            self.mines.append(mine)
        
        
class Medigun(Weapon):
    healTarget = None
    uberReady = False
    def deserialize(self, socket, type):
        print("Medigun deserialize")
        healTargetId = net.read_ubyte(socket)
        if healTargetId != 255:
            self.healTarget = game.players[healTargetId]
        else:
            self.healTarget = None
        
class Shotgun(Weapon):
    pass
        
class Revolver(Weapon):
    pass
        
class Rifle(Weapon):
    pass
        
class Blade(Weapon):
    pass