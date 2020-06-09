
import gg2.network.util as net
import gg2.constants as gg2consts
import gg2.map.cp as gg2cp
import gg2.map.gen as gg2gen

class HUD():
    @classmethod
    def for_map(self, mapname):
        if mapname.startswith("pony_destination"): # hack
            return CTFHUD()
        if mapname.startswith("ctf"):
            return CTFHUD()
        if mapname.startswith("cp"):
            return CPHUD()
        if mapname.startswith("3cp"):
            result = CPHUD()
            result.cps.pop(4)
            result.cps.pop(3)
            return result
        if mapname.startswith("koth"):
            return KothHUD()
        if mapname.startswith("dkoth"):
            return DKothHUD()
        if mapname.startswith("arena"):
            return ArenaHUD()
        if mapname.startswith("gen"):
            return GeneratorHUD()
        if mapname.startswith("tdm"):
            return DeathmatchHUD()
            
class CTFHUD(HUD):
    def deserialize(self, socket, type):
        print("CTFHUD")
        self.timeLimitMins = net.read_ubyte(socket)
        self.timeLimit = self.timeLimitMins *30 *60
        self.timer = net.read_uint(socket)
            
class CPHUD(HUD):
    cps = [
        gg2cp.ControlPoint(),
        gg2cp.ControlPoint(),
        gg2cp.ControlPoint(),
        gg2cp.ControlPoint(),
        gg2cp.ControlPoint()
    ] #TODO
    def deserialize(self, socket, type):
        print("CPHUD")
        self.timeLimitMins = net.read_ubyte(socket)
        self.timeLimit = self.timeLimitMins *30 *60
        self.timer = net.read_uint(socket)
        self.setupTimer = net.read_ushort(socket)
        for cp in self.cps:
            cp.deserialize(socket, type)

class KothHUD(HUD):
    cp = gg2cp.KothControlPoint() #TODO
    def deserialize(self, socket, type):
        print("KothHUD")
        self.cpUnlock = net.read_ushort(socket)
        self.redTimer = net.read_ushort(socket)
        self.blueTimer= net.read_ushort(socket)
        self.cp.deserialize(socket, type)
        if self.cpUnlock == 0 and self.cp.locked:
            self.doEventUnlockCP() #TODO
            
class DKothHUD(HUD):
    cp_red = gg2cp.KothRedControlPoint() #TODO
    cp_blue = gg2cp.KothBlueControlPoint() #TODO
    def deserialize(self, socket, type):
        print("DKothHUD")
        self.cpUnlock = net.read_ushort(socket)
        self.redTimer = net.read_ushort(socket)
        self.blueTimer= net.read_ushort(socket)
        self.cp_red.deserialize(socket, type)
        self.cp_blue.deserialize(socket, type)
            
class ArenaHUD(HUD):
    cp = gg2cp.ArenaControlPoint() # TODO
    def deserialize(self, socket, type):
        print("ArenaHUD")
        self.timeLimitMins = net.read_ubyte(socket)
        self.timeLimit = self.timeLimitMins *30 *60
        self.timer = net.read_uint(socket)
        self.cpUnlock = net.read_ushort(socket)
        self.roundStart = net.read_ubyte(socket) * 2
        
        self.cp.deserialize(socket, type)

class GeneratorHUD(HUD):
    gen_red = gg2gen.GeneratorRed()   #TODO
    gen_blue = gg2gen.GeneratorBlue() #TODO 
    def deserialize(self, socket, type):
        print("GeneratorHUD")
        self.timeLimitMins = net.read_ubyte(socket)
        self.timeLimit = self.timeLimitMins *30 *60
        self.timer = net.read_uint(socket)
        self.gen_red.deserialize(socket, type)
        self.gen_blue.deserialize(socket, type)
            
class DeathmatchHUD(HUD):
    def deserialize(self, socket, type):
        print("DeathmatchHUD")
        self.timeLimitMins = net.read_ubyte(socket)
        self.timeLimit = self.timeLimitMins *30 *60
        self.timer = net.read_uint(socket)
        self.killLimit = net.read_ushort(socket)