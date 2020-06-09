
import gg2.network.util as net
import gg2.constants as gg2consts

from gg2.objects.weapon import Weapon

class Character():
    player = None
    x = 0
    y = 0
    
    alarm = [0,0,0,0,0] #TODO
    
    def __init__(self, player):
        self.player = player
        self.currentWeapon = Weapon(self) #TODO remove
        
    def deserialize(self, socket, type):
        print("Character deserialize")
        self.keyState = net.read_ubyte(socket)
        self.aimDirection = net.read_ushort(socket)*360/65536
        self.aimDistance = net.read_ubyte(socket)*2
        
        temp = None
        newIntel = None
        
        if(type == gg2consts.QUICK_UPDATE) or (type == gg2consts.FULL_UPDATE):
            self.x = net.read_ushort(socket)/5
            self.y = net.read_ushort(socket)/5
            self.hspeed = net.read_ubyte(socket)/8.5
            self.vspeed = net.read_ubyte(socket)/8.5
            self.xprevious = self.x
            self.yprevious = self.y
            
            self.hp = net.read_ubyte(socket)
            self.currentWeapon.ammoCount = net.read_ubyte(socket)
            
            temp = net.read_ubyte(socket)
            self.cloak = (temp & 0x01 != 0)
            self.moveStatus = (temp >> 1) & 0x07
        
        if type == gg2consts.FULL_UPDATE:
            self.animationOffset = net.read_ubyte(socket)
            
            # class specific syncs
            if gg2consts.CLASS_SPY == self.player.clazz:
                self.cloakAlpha = net.read_ubyte(socket) / 255
                
            elif gg2consts.CLASS_MEDIC == self.player.clazz:
                self.currentWeapon.uberCharge = net.read_ubyte(socket)*2000/255
                
            elif gg2consts.CLASS_ENGINEER == self.player.clazz:
                self.nutsNBolts = net.read_ubyte(socket)
                
            elif gg2consts.CLASS_SNIPER == self.player.clazz:
                self.currentWeapon.t = net.read_ubyte(socket)
                if(self.currentWeapon.t):
                    self.zoomed = True
                
            else:
                net.read_ubyte(socket)
                
            self.alarm[1] = net.read_ushort(socket) # / global.delta_factor
            if (self.alarm[1] != 0):
                self.canGrabIntel = False
            self.intel = net.read_ubyte(socket)
            self.intelRecharge = net.read_ushort(socket)
            self.currentWeapon.deserialize(socket, type)
           
            
        #event_user(1)