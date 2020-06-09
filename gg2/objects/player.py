
import gg2.network.util as net
import gg2.constants as gg2consts
import gg2.objects.character as character
import gg2.objects.weapon as weapon
from gg2.game import game
from gg2.objects.sentry import Sentry
from gg2.objects.speechbubble import SpeechBubble

class Player():
    name = None
    playerID = None
    team = None
    clazz = gg2consts.CLASS_SCOUT
    object = None
    sentry = None
    stats = {
        "KILLS" : 0,
        "DEATHS" : 0,
        "CAPS": 0,
        "ASSISTS" : 0,
        "DESTRUCTION" : 0,
        "STABS" : 0,
        "HEALING": 0,
        "DEFENSES" : 0,
        "INVULNS" : 0,
        "BONUS" : 0,
        "POINTS" : 0
    }
    roundStats = {
        "KILLS" : 0,
        "DEATHS" : 0,
        "CAPS": 0,
        "ASSISTS" : 0,
        "DESTRUCTION" : 0,
        "STABS" : 0,
        "HEALING": 0,
        "DEFENSES" : 0,
        "INVULNS" : 0,
        "BONUS" : 0,
        "POINTS" : 0
    }
    dominations = {} # could be a list but it's mapped by playerID -> killCount, and playerID may go above ours
    
    bubble = None
    
    def __init__(self):
        self.bubble = SpeechBubble(self)
    
    def set_bubble(self, bubble_id):
        self.bubble.image_index = bubble_id
        self.bubble.alpha = 1
        
    def spawn(self, spawnpointId, spawnGroup):
        #if self.team == TEAM_RED:
        #    spawnX = ds_list_find_value(global.spawnPointsRed[0,spawnGroup], spawnpointId)
        #    spawnY = ds_list_find_value(global.spawnPointsRed[1,spawnGroup], spawnpointId)
        #else:
        #    spawnX = ds_list_find_value(global.spawnPointsBlue[0,spawnGroup], spawnpointId)
        #    spawnY = ds_list_find_value(global.spawnPointsBlue[1,spawnGroup], spawnpointId)
            
        spawnX = 0
        spawnY = 0 #TODO

        new_char = character.from_class(self.clazz)
        if new_char is None:
            print("Spawning a player did not succeed because his class and/or team were invalid.")
            exit()

        if self.object is not None:
            #self.object.destroy()
            self.object = None

        self.object = new_char(self)
        self.object.x = spawnX
        self.object.y = spawnY

        #if (instance_exists(RespawnTimer)) {
        #    with(RespawnTimer)
        #        done = true

        # playsound(spawnX, spawnY, RespawnSnd)
        
    def death(self, killer, assistant, damageSource):
        # recordKillInLog(victim, killer, assistant, damageSource); # TODO

        self.stats["DEATHS"] += 1
        if killer is not None:
            if (damageSource == gg2consts.DAMAGE_SOURCES["KNIFE"] or damageSource == gg2consts.DAMAGE_SOURCES["BACKSTAB"]):
                killer.stats["STABS"] += 1
                killer.roundStats["STABS"] += 1
                killer.stats["POINTS"] += 1
                killer.roundStats["POINTS"] += 1
            
            if (self.object.weaponType == weapon.Medigun):
                if (self.object.currentWeapon.uberReady):
                    killer.stats["BONUS"] += 1
                    killer.roundStats["BONUS"] += 1
                    killer.stats["POINTS"] += 1
                    killer.roundStats["POINTS"] += 1
                
            if (killer != self):
                killer.stats["KILLS"] += 1
                killer.roundStats["KILLS"] += 1
                killer.stats["POINTS"] += 1
                killer.roundStats["POINTS"] += 1
                if (self.object.intel):
                    killer.stats["DEFENSES"] += 1
                    killer.roundStats["DEFENSES"] += 1
                    killer.stats["POINTS"] += 1
                    killer.roundStats["POINTS"] += 1
                    #recordEventInLog(4, killer.team, killer.name, global.myself == killer) # TODO

        if assistant is not None:
            assistant.stats["ASSISTS"] += 1
            assistant.roundStats["ASSISTS"] += 1
            assistant.stats["POINTS"] += .5
            assistant.roundStats["POINTS"] += .5
            
    def fire(self, seed):
        self.object.currentWeapon.fire()
    
    def deserialize(self, socket, type):
        print("Player deserialize {} {}".format(self.playerID, self.name))
        if (type == gg2consts.FULL_UPDATE):
            self.stats["KILLS"] = net.read_ubyte(socket)
            self.stats["DEATHS"] = net.read_ubyte(socket)
            self.stats["CAPS"] = net.read_ubyte(socket)
            self.stats["ASSISTS"] = net.read_ubyte(socket)
            self.stats["DESTRUCTION"] = net.read_ubyte(socket)
            self.stats["STABS"] = net.read_ubyte(socket)
            self.stats["HEALING"] = net.read_ushort(socket)
            self.stats["DEFENSES"] = net.read_ubyte(socket)
            self.stats["INVULNS"] = net.read_ubyte(socket)
            self.stats["BONUS"] = net.read_ubyte(socket)
            self.stats["POINTS"] = net.read_ubyte(socket)
            self.queueJump = net.read_ubyte(socket)
            self.rewards = net.receivestring(socket, 2)
            
            # Deserialize the domination kill table (number of kills for each player except self)
            # expect len(game.players)-1 bytes
            for i in range(len(game.players)):
                if i == self.playerID:
                    continue
                self.dominations[i] = net.read_ubyte(socket)
     
        charObj = None
        subobjects = net.read_ubyte(socket)
        
        # If the player has a character object on the server
        if (subobjects & 0x01) != 0:
            if (self.object == None) :
                charObj = character.from_class(self.clazz)
                if(charObj != None) :
                    self.object = charObj(self)
                else:
                    show_message("Invalid player object while deserializing")
                
            self.object.deserialize(socket, type)
        else:
            if(self.object != -1):
                self.object = None # TODO destroy
            self.object = None
        
        # If the player has a sentry object on the server
        if subobjects & 0x02:
            if not self.sentry:
                self.sentry = Sentry(self)
                self.sentry.startDirection = 1#self.image_xscale # TODO
                self.sentry.image_xscale = 1#self.image_xscale
                
            self.sentry.deserialize(socket, type)
        else:
            self.sentry = None # TODO destroy