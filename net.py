from socket import socket
from player import Player

# https://pypi.org/project/msgpack/
import msgpack



    
            

# -----------------------------------## NETWORK COMMUNICATION ##-----------------------------------

# Our Netwoork Message Format:
#     '<[Two Letter Action]:[Relevant Data]>'
#     Example '<VS:1>' for Vote Start = True

VOTE_ACTION: str = "VS"
VOTE_NO_MESSAGE: str = "<VS:0>"
VOTE_YES_MESSAGE: str = "<VS:1>"
    
def send_message(sock: socket, message: str):
    """ Send msg block. """
    pack = msgpack.packb(message)
    sock.send(pack)

def receive_message(sock: socket) -> str:
    """ Receive a msg block. """
    pack = sock.recv(1024)
    message = msgpack.unpackb(pack)
    return message

def process_client_message(connection: socket, message: str, connected_players: {socket, Player}): # TODO
    """ Processes an incoming message from a player client. """
    print(message)

    # Check that the message is in the correct format. 
    if message[0] == "<" and message[-1] == ">" and message[3] == ":":
        pass
    else:
        return
    
    # Vote Messages
    if message == VOTE_NO_MESSAGE:
        connected_players[connection].vote = False
    elif message == VOTE_YES_MESSAGE:
        connected_players[connection].vote = True
        print(connected_players[connection].vote)


def process_server_message(): # TODO
    """ Processes an incoming message from the game server. """    
    pass
    
    
