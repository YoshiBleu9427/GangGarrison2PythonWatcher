
import gg2.network.util as net
import gg2.constants as gg2consts

class ControlPoint():
    team = gg2consts.TEAM_SPECTATOR
    locked = False
    
    def capture(self, team):
        self.team = team
        
    def deserialize(self, socket, type):
        print("ControlPoint")
        new_team = net.read_byte(socket)
        self.capping_team = net.read_byte(socket)
        self.capping = net.read_ushort(socket)
        if self.team != new_team:
            self.capture(new_team)

class ArenaControlPoint(ControlPoint):
    pass

class KothControlPoint(ControlPoint):
    pass

class KothRedControlPoint(KothControlPoint):
    pass

class KothBlueControlPoint(KothControlPoint):
    pass