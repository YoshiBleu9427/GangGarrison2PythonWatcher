
import gg2.network.util as net
import gg2.constants as gg2consts

class Intelligence():
    team = gg2consts.TEAM_SPECTATOR
    locked = False
    
    alarm = [0] #TODO
        
    def deserialize(self, socket, type):
        print("Intelligence")
        self.x = net.read_ushort(socket) / 5
        self.y = net.read_ushort(socket) / 5
        self.alarm[0] = net.read_ushort(socket) # / global.delta_factor #TODO

class IntelligenceRed(Intelligence):
    pass

class IntelligenceBlue(Intelligence):
    pass