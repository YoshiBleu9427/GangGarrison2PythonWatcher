
import gg2.network.util as net
import gg2.constants as gg2consts

class Mine():
    owner = None
    
    alarm = [0,0,0,0,0] #TODO
    
    def __init__(self, owner):
        self.owner = owner
        self.team = owner.player.team
        
    def deserialize(self, socket, type):
        print("Mine deserialize")
        if type == gg2consts.QUICK_UPDATE or type == gg2consts.FULL_UPDATE:
            self.x = net.read_ushort(socket)/5
            self.y = net.read_ushort(socket)/5
            self.hspeed = net.read_byte(socket)/5
            self.vspeed = net.read_byte(socket)/5
            self.stickied = net.read_ubyte(socket)