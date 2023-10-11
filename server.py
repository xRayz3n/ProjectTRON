import socket
import threading
import multiprocessing
import class_game
import player
import packets
import os
import time
playerConnection_queue = multiprocessing.Queue()
playerList = []

maxplayers = 4

def OpenConnections(): #keeps the connection open
    server_socket.listen()
    print("Opening server...")
    while True:
        client_socket, client_addr = server_socket.accept()
        print(f'New connection from {client_addr}')
        threading.Thread(group=None, target=GetPlayers,args=[client_socket,client_addr]).start()


def GetPlayers(client_socket, client_addr): #acquire player info

    #nickname = client_socket.recv(16).decode("utf-8") #receive player nickname, 16 char max
    nickname = packets.Packets.receive(client_socket)[1]
    print(f"Ip {client_addr} named to {nickname}")
    playerInfo = player.Player(client_socket, client_addr,nickname)
    playerList.append(playerInfo)

    message = f"{playerInfo.name} is the player {playerList.index(playerInfo) + 1}, "
    Broadcast_ToAllPlayers(message)

    while True:
        type, status = packets.Packets.receive(client_socket)
        

        match status:
            case "disconnect":
                print(f"Connection lost from {playerInfo.name}")
                playerList.remove(playerInfo)
                client_socket.close()
                break
            case "ready":
                playerInfo.state = "ready"
                print(f"{playerInfo.name} is now ready")
            case "unready":
                playerInfo.state = "unready"
                print(f"{playerInfo.name} is now unready")

        if all(x.state=="ready" for x in playerList) and len(playerList)>1:
            message = ('All players are ready, starting in')
            Broadcast_ToAllPlayers(message)
            for i in range(3,0,-1):
                Broadcast_ToAllPlayers(f"\n{i}...")
                time.sleep(1)
            Broadcast_ToAllPlayers("Game started!")

        print(f"{playerInfo.name} wrote {status}")

def Broadcast_ToAllPlayers(message):
    for playerInfo in playerList:
        packet = packets.Packets(message, package_type="I")
        packet.send(playerInfo.client_socket)






if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))
    threading.Thread(group=None, target=OpenConnections).start()