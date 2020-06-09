
import gg2.network.util as net
import gg2.constants as gg2consts
from gg2.game import game
from gg2.objects.projectiles.mine import Mine

class Minegun():
    owner = None
    
    alarm = [0,0,0,0,0] #TODO
    mines = []
    
    def __init__(self, owner):
        self.owner = owner
        
    def deserialize(self, socket, type):
        super.deserialize(socket, type)
        print("Minegun deserialize")
        self.lobbed = net.read_ubyte(socket)
        
        self.mines.clear()
        
        for i in range(lobbed):
            mine = Mine(self.owner)
            mine.deserialize(socket, type)
            self.mines.append(mine)