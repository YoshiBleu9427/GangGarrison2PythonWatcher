
import gg2.network.util as net
import gg2.constants as gg2consts

class Generator():
    team = gg2consts.TEAM_SPECTATOR
        
    def deserialize(self, socket, type):
        self.hp = net.read_ushort(socket)
        self.shieldHp = net.read_ushort(socket)

class GeneratorRed(Generator):
    team = gg2consts.TEAM_RED
    
class GeneratorBlue(Generator):
    team = gg2consts.TEAM_BLUE