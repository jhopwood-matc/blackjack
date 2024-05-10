#!/usr/bin/ python3.10
from socket import socket, AF_INET, SOCK_STREAM, create_server

from net import send_message, receive_message, process_client_message, Player

## BOOT AND INITIALIZE ##
connected_players: {socket, Player} = {}
whose_turn: int
starting_wallet_amount: float

# Start TCP server on localhost on port 51721
server_address: tuple[str, int] = ("127.0.0.1", 51721)
sock = socket(AF_INET, SOCK_STREAM)
sock.bind(server_address)

addr = ("", 51721)
s = create_server(addr, )

# Begin listening
sock.listen(5)
sock.setblocking(False)

## GET PLAYERS CONNECTED INTO LOBBY ##
waiting_for_connections: bool = True
while waiting_for_connections:

    # Connect new players
    try:
        # Check for new connections and accept them    
        connection, client_address = sock.accept()

        # Create a player in the lobby for the connection
        connected_players[connection] = Player(0)

    except BlockingIOError:
        # (There were no new connections this loop-through)
        pass

    # Listen for votes from players
    for connection in connected_players:
        message = receive_message(connection)
        process_client_message(connection, message, connected_players)

    # If the vote is unanimous, lets start
    total_votes: int = 0
    total_yes_votes: int = 0
    for connection in connected_players:
        total_votes += 1
        if connected_players[connection].vote == True:
            total_yes_votes += 1
    if total_votes == total_yes_votes and total_votes != 0:
        waiting_for_connections = False

## PLAYING BLACKJACK ##
game_is_running: bool = True
while game_is_running:
    
    # Receive updates over network from players
    for connection in connected_players:

        # Grab update from TCP socket
        new_message = receive_message(connection)

        # Update internal state of game from update # TODO
        process_client_message(new_message) # TODO

    # Update the game based on its own state

    # TODO Send out new state to clients
    msg: str = "Hello"
    send_message(msg) # TODO

    pass