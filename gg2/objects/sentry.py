
import gg2.network.util as net
import gg2.constants as gg2consts

from gg2.objects.weapon import Weapon

class Sentry():
    ownerPlayer = None
    team = None
    x = 0
    y = 0
    start_direction = 0
    
    alarm = [0,0,0,0,0] #TODO
    
    def __init__(self, player):
        self.ownerPlayer = player
        self.team = player.team

        player.object.nutsNBolts -= 100 #TODO check if right place
        
    def destroy(self, killer, assistant, damageSource):
        if killer is not None and killer != self.ownerPlayer:
            killer.stats["DESTRUCTION"] += 1
            killer.roundStats["DESTRUCTION"] += 1
            killer.stats["POINTS"] += 1
            killer.roundStats["POINTS"] += 1
            # recordDestructionInLog(self.ownerPlayer, killer, healer, damageSource) # TODO
            # self.ownerPlayer.setBubble(60) # TODO
        elif damageSource == gg2consts.DAMAGE_SOURCES["GENERATOR_EXPLOSION"]:
            pass
            # recordDestructionInLog(self.ownerPlayer, None, None, damageSource) # TODO
            # self.ownerPlayer.setBubble(60) # TODO
            
        self.ownerPlayer.sentry = None #TODO check if right place
        
    def deserialize(self, socket, type):
        print("Sentry deserialize")
        if type == gg2consts.FULL_UPDATE:
            self.start_direction = net.read_byte(socket)
            self.x = net.read_ushort(socket)/5
            self.y = net.read_ushort(socket)/5
            self.xprevious = self.x;
            self.yprevious = self.y;
            
        if type == gg2consts.QUICK_UPDATE or type == gg2consts.FULL_UPDATE:
            tbyte = net.read_byte(socket)
            self.built = ((tbyte & 0x80) != False)
            self.hp = tbyte & 0x7F
            if type == gg2consts.FULL_UPDATE and not self.built:
                self.vspeed = net.read_byte(socket)
                
            if self.built:
                self.vspeed = 0