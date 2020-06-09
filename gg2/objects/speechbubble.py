
import gg2.network.util as net
import gg2.constants as gg2consts

from gg2.objects.weapon import Weapon

class SpeechBubble():
    image_index = 0
    alpha = 0
    
    def __init__(self, player):
        self.ownerPlayer = player
        