from gg2.network.gg2connector import GG2Connector
from gg2.game import game
import gg2.constants as gg2consts
import binascii, sys, time

import sys, pygame
pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

screen = pygame.display.set_mode(size)

pygame.font.init()

SERVER_IP = 'localhost' # shouldn't need to change this
SERVER_PORT = 8196		 # this is your gg2 port
    

running = True
allowed_ticks = 60000


#connecting
print("[{}] Check")
gg2connector = GG2Connector()
gg2connector.connect(SERVER_IP, SERVER_PORT)
data = gg2connector.send_hello()
print("   Sent hello {}".format(data))
data = gg2connector.reserve_slot("botwatcher")
print("   Reserved {}".format(binascii.hexlify(data)))
if data == gg2consts.SERVER_FULL:
    print("   Couldn't reserve, was full.")
    gg2connector.close()
else:
    data = gg2connector.join()
    print("   Joined {}".format(data))
    playerID = gg2connector.playerID
    #gg2connector.change_team(gg2consts.TEAM_ANY)


bg_value = 0
bg_color = (bg_value, bg_value, bg_value)
red = (232, 16, 16)
blu = (16, 16, 232)

def loadmap(map):
    img = pygame.image.load("../Maps/{}.png".format(map))
    return img
    
prevMap = None
mapimg = None

# loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    gg2connector.receive_update()
    screen.fill(bg_color)
    
    if game.currentMap != prevMap:
        prevMap = game.currentMap
        mapimg = loadmap(game.currentMap)
        pygame.display.set_caption(game.currentMap)
        
        if mapimg is not None:
            imagerect = mapimg.get_rect()
            print("Replace screen")
            screen = pygame.display.set_mode(mapimg.get_size())

    if mapimg is not None:
        imagerect = mapimg.get_rect()
        screen.blit(mapimg, imagerect)
        
    for p in game.players:
        if p.object is not None:
            
            if p.object.currentWeapon.display_fired_last > 0:
                color = (80 * p.object.currentWeapon.display_fired_last, 80 * p.object.currentWeapon.display_fired_last, 0)
                p.object.currentWeapon.display_fired_last -= 1
            else:
                color = red
                if p.team == gg2consts.TEAM_BLUE:
                    color = blu
                
            x = int(p.object.x / 6)
            y = int(p.object.y / 6)
            
            pygame.draw.circle(screen, color, (x, y), 2) 

    pygame.display.flip()

    time.sleep(1./60.)
    allowed_ticks -= 1
    running = (allowed_ticks > 0)
    print("TICK")
    sys.stdout.flush()
