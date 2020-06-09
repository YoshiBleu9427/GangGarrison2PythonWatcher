
import gg2.network.util as net
import gg2.constants as gg2consts
from gg2.game import game

class Medigun():
    owner = None
    
    alarm = [0,0,0,0,0] #TODO
    
    def __init__(self, owner):
        self.owner = owner