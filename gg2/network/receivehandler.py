import struct

import gg2.constants as gg2const
import gg2.network.util as net
from gg2.objects.player import Player
from gg2.objects.sentry import Sentry
from gg2.map.hud import HUD
import gg2.map.intel as intel
from gg2.game import game

class ReceiveHandler():

    def handle(self, header, socket):
        print("Handinling", header)
        
        if header == gg2const.PLAYER_JOIN:
            player = Player()
            player.name = net.receivestring(socket, 1)
            player.playerID = len(game.players)
            game.players.append(player)
            
            if player.playerID == game.playerID:
                game.myself = player
                
            return True
            
        if header == gg2const.PLAYER_LEAVE:
            print("PLAYER_LEAVE")
            playerID = net.read_ubyte(socket)
            game.players.pop(playerID)
            # TODO removePlayer(player)
            if playerID < game.playerID:
                game.playerID -= 1
            
            return True
            
        if header == gg2const.PLAYER_DEATH:
            print("PLAYER_DEATH")
            playerID = net.read_ubyte(socket)
            otherPlayerID = net.read_ubyte(socket)
            assistantPlayerID = net.read_ubyte(socket)
            causeOfDeath = net.read_ubyte(socket)
                  
            player = game.players[playerID]
            
            otherPlayer = None
            if otherPlayerID != 255:
                otherPlayer = game.players[otherPlayerID]
            
            assistantPlayer = None
            if assistantPlayerID != 255:
                assistantPlayer = game.players[assistantPlayerID]
            
            player.death(otherPlayer, assistantPlayer, causeOfDeath)
            return True
             
        if header == gg2const.BALANCE:
            print("BALANCE")
            balanceplayer = net.read_ubyte(socket)
            if balanceplayer == 255:
                #if !instance_exists(Balancer) instance_create(x,y,Balancer);
                #with(Balancer) notice=0;
                print("Balance notice")
            else:
                player = game.players[balanceplayer]
                player.clazz = net.read_ubyte(socket)
                if player.object is not None:
                    #with(player.object) {
                    #    instance_destroy();
                    #}
                    # TODO nothing to do?? Check
                    player.object = None
                    
                if player.team == gg2const.TEAM_RED:
                    player.team = gg2const.TEAM_BLUE
                else:
                    player.team = gg2const.TEAM_RED
                    
                #if !instance_exists(Balancer) instance_create(x,y,Balancer);
                #Balancer.name=player.name;
                #with (Balancer) notice=1;
                print("Balanced {}".format(player.name))
            return True
            
        if header == gg2const.PLAYER_CHANGETEAM:
            playerID = net.read_ubyte(socket)
            player = game.players[playerID]
            
            if player.object != None:
                player.object = None # TODO destroy
            player.team = net.read_ubyte(socket)
            return True
            
        if header == gg2const.PLAYER_CHANGECLASS:
            playerID = net.read_ubyte(socket)
            player = game.players[playerID]
            
            if player.object != None:
                player.object = None # TODO destroy
            player.clazz = net.read_ubyte(socket)
            return True     
        
        if header == gg2const.PLAYER_CHANGENAME:
            player = game.players[net.read_ubyte(socket)]
            player.name = net.receivestring(socket, 1)
            #if player = game.myself:
            #    game.playerName = player.name
            # TODO why ^
            return True
                 
        if header == gg2const.PLAYER_SPAWN:
            player = game.players[net.read_ubyte(socket)]
            player.spawn(net.read_ubyte(socket), net.read_ubyte(socket))
            return True
              
        if header == gg2const.CHAT_BUBBLE:
            player = game.players[net.read_ubyte(socket)]
            bubble_id = net.read_ubyte(socket)
            player.set_bubble(bubble_id)
            return True
             
        if header == gg2const.BUILD_SENTRY:
            player = game.players[net.read_ubyte(socket)]
            x = net.read_ushort(socket) / 5
            y = net.read_ushort(socket) / 5
            start_direction = net.read_byte(socket)
            
            if player.sentry is None:
                player.sentry = Sentry(player)
            
            player.sentry.x = x
            player.sentry.y = y
            player.sentry.start_direction = start_direction
            return True
              
        if header == gg2const.DESTROY_SENTRY:
            playerID = net.read_ubyte(socket)
            otherPlayerID = net.read_ubyte(socket)
            assistantPlayerID = net.read_ubyte(socket)
            causeOfDeath = net.read_ubyte(socket)
            
            player = game.players[playerID]
            if otherPlayerID == 255:
                player.sentry.destroy(None, None, causeOfDeath)
            else:
                otherPlayer = game.players[otherPlayerID]
                if assistantPlayerID == 255:
                    player.sentry.destroy(otherPlayer, None, causeOfDeath)
                else:
                    assistantPlayer = game.players[assistantPlayerID]
                    player.sentry.destroy(otherPlayer, assistantPlayer, causeOfDeath)
            return True
            
        if header == gg2const.JOIN_UPDATE:
            game.playerID = net.read_ubyte(socket)
            game.currentMapArea = net.read_ubyte(socket)
            return True
            
        if header == gg2const.CHANGE_MAP:
            game.currentMap = net.receivestring(socket, 1)
            game.currentMapMD5 = net.receivestring(socket, 1)
            game.hud = HUD.for_map(game.currentMap)
            return True
            
        if header == gg2const.FULL_UPDATE:
            tdmInvulnerabilityTicks = net.read_ushort(socket) #ushort
            nbPlayers = net.read_ubyte(socket)
            if nbPlayers != len(game.players):
                print("Wrong number of players while deserializing")
                print(socket.recv(1024))
                raise Exception("Wrong number of players while deserializing")
            for i in range(nbPlayers):
                player = game.players[i]
                player.deserialize(socket, gg2const.FULL_UPDATE)
            
            #    with(MovingPlatform)
            #event_user(11);
            
            #deserialize(IntelligenceRed);
            numInstances = net.read_ushort(socket)
            for i in range (numInstances):
                newInstance = intel.IntelligenceRed()
                newInstance.deserialize(socket, type)
                
            #deserialize(IntelligenceBlue);
            numInstances = net.read_ushort(socket)
            for i in range (numInstances):
                newInstance = intel.IntelligenceBlue()
                newInstance.deserialize(socket, type)

            game.caplimit = net.read_ubyte(socket)
            game.redCaps = net.read_ubyte(socket)
            game.blueCaps = net.read_ubyte(socket)
            game.Server_RespawntimeSec = net.read_ubyte(socket)
            game.Server_Respawntime = game.Server_RespawntimeSec * 30
                 
            # TODO HUD
            game.hud.deserialize(socket, gg2const.FULL_UPDATE)

            for a in range(10):
                game.classlimits[a] = net.read_ubyte(socket)
            return True
            
        if header == gg2const.QUICK_UPDATE:
            nbPlayers = net.read_ubyte(socket)
            if nbPlayers != len(game.players):
                print("Wrong number of players while deserializing")
                print(socket.recv(1024))
                raise Exception("Wrong number of players while deserializing")
            for i in range(nbPlayers):
                player = game.players[i]
                player.deserialize(socket, gg2const.QUICK_UPDATE)
            return True
            
        if header == gg2const.INPUTSTATE:
            nbPlayers = net.read_ubyte(socket)
            if nbPlayers != len(game.players):
                print("Wrong number of players while deserializing")
                print(socket.recv(1024))
                raise Exception("Wrong number of players while deserializing")
            for i in range(nbPlayers):
                player = game.players[i]
                player.deserialize(socket, gg2const.INPUTSTATE)
            return True
            
        if header == gg2const.CAPS_UPDATE:
            nbPlayers = net.read_ubyte(socket)
            if nbPlayers != len(game.players):
                print("Wrong number of players while deserializing")
                print(socket.recv(1024))
                raise Exception("Wrong number of players while deserializing")
            game.redCaps = net.read_ubyte(socket)
            game.blueCaps = net.read_ubyte(socket)
            game.Server_RespawntimeSec = net.read_ubyte(socket)
            game.Server_Respawntime = game.Server_RespawntimeSec * 30

            game.hud.deserialize(socket, gg2const.CAPS_UPDATE)
            return True   
            
        if header == gg2const.MESSAGE_STRING:
            msg = net.receivestring(socket, 1)
            print("Message string", msg)
            return True
        
        if header == gg2const.SENTRY_POSITION:
            player = game.players[net.read_ubyte(socket)]
            if player.sentry is not None:
                player.sentry.x = net.read_ushort(socket) / 5
                player.sentry.y = net.read_ushort(socket) / 5
                player.sentry.xprevious = player.sentry.x
                player.sentry.yprevious = player.sentry.y
                player.sentry.vspeed = 0
            return True
          
        if header == gg2const.WEAPON_FIRE:
            print("WEAPON_FIRE")
            player = game.players[net.read_ubyte(socket)]
            
            if player.object is not None:
                player.object.x = net.read_ushort(socket) / 5
                player.object.y = net.read_ushort(socket) / 5
                player.object.hspeed = net.read_byte(socket) / 8.5
                player.object.vspeed = net.read_byte(socket) / 8.5
                player.object.xprevious = player.object.x;
                player.object.yprevious = player.object.y;
                
                player.fire(net.read_ushort(socket))
            return True
            
        if header == gg2const.PLUGIN_PACKET:
            print("PLUGIN_PACKET")
            packetLen = net.read_ushort(socket)
            packetID = net.read_ubyte(socket)
            print("Len, ID:", packetLen, packetID)
            
            #// get packet data
            buf = socket.recv(packetLen - 1)
            print(buf)
            
            # success = _PluginPacketPush(packetID, buf, noone); #TODO
            #if not success:
            #    show_error("ERROR when reading plugin packet: no such plugin packet ID " + string(packetID), true);
            return True

            
        print("Failed to handle")
        return False