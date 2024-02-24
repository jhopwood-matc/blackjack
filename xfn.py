
from typing import Callable
import socket

# https://pypi.org/project/msgpack/
import msgpack


class Player:

    wallet_amount: float
    vote: bool
     
    def __init__(self, starting_wallet_amount: float) -> None:
        self.wallet_amount = 100.0 * starting_wallet_amount
        self.vote = False

# -----------------------------------## CLIENT ##-----------------------------------  

# Views
MAIN_MENU: str = "Main Menu"
RULES: str = "Rules"
GAME_START: str = "Game Start"
            
def get_name() -> str:
    """ TODO Doc Comment 
        TODO Section comments """
    waiting_for_name: bool = True
    min_name_len: int = 3
    while waiting_for_name:
        name = input("Enter your name: ")
        stripped_name: str = name.strip()
        if len(stripped_name) < min_name_len:
            print("Name must be 3 characters or longer.\n")
            continue
        elif len(stripped_name) >= min_name_len:
            waiting_for_name = False
            return name
        else:
            print("Unexpected input. Please try again.\n")
            continue

def get_starting_wallet_value() -> int:
    """ TODO Doc Comment 
        TODO Section comments """
    waiting_for_starting_wallet_amount: bool = True
    max_starting_wallet_amount: float = 1000000.00
    min_starting_wallet_amount: float = 0.0
    while waiting_for_starting_wallet_amount:
        try:
            starting_wallet_amount = float(input("Enter the starting pot amount: $"))
            if min_starting_wallet_amount <= starting_wallet_amount <= max_starting_wallet_amount:
                waiting_for_starting_wallet_amount = False
                return starting_wallet_amount
            elif starting_wallet_amount < min_starting_wallet_amount:
                print("Cannot have a negative starting pot value. Try again.\n")
                continue
            elif starting_wallet_amount > max_starting_wallet_amount:
                print(f"Cannot exceed ${max_starting_wallet_amount} starting value! Try again.\n")
                continue
            else:
                print("Undefined behavior! Try again.\n")
        except ValueError:
            print("Please enter a valid number.\n")
            continue
  
def print_rules() -> str:
    """ TODO Doc Comment 
        TODO Section comments """
    
    RULES: str = "These are the rules."
    print(RULES)
    input("\nPress [Enter] to return to the main menu.. ")
    return MAIN_MENU

def play_game(sock: socket.socket):
    """ TODO Doc Comment 
        TODO Section comments """
    
    # Get game server address from user
    dest_srvr_addr: str = input("\nPlease enter the address of the game server: ")
    dest_srvr_addr: tuple[str, int] = (dest_srvr_addr, 51721)

    # Attempt a connection
    try:
        sock.settimeout(7.5)
        print(f"Connecting to {dest_srvr_addr[0]}:{dest_srvr_addr[1]}")
        sock.connect(dest_srvr_addr)
        sock.settimeout(None)
    except TimeoutError:
        print("Connection Failed!")
    
    name: str = get_name()
    print(name)

    welcome_text: str = f"Welcome to the casino, {name}! I am your dealer, Darwin." \
                        f" You have chosen to have CHANGE computer player(s)." \
                        f" The starting pot begins at $CHANGE."
    print(welcome_text)

def main_menu() -> str:
    """ TODO Doc Comment 
        TODO Section comments """
    
    menu_options: {str, str} = {
        "Play Multiplayer" : "play",
        "Show Rules"       : "rules"
    }
    print(f"\nWelcome to BlackJack 0.0.1.")
    selecting: bool = True
    while selecting:
        print("Please select an action from the list below.")
        for key in menu_options:
            print(f"{key:<20} : type '{menu_options[key]}'")
    
        user_selection: str = input("> ").strip().lower()

        # TODO: Regex
        if user_selection == menu_options["Play Multiplayer"]:
            selecting = False
            return GAME_START
        elif user_selection == menu_options["Show Rules"]:
            selecting = False
            return RULES
        else:
            print("Unrecognized option! Try again.\n")

# -----------------------------------## NETWORK COMMUNICATION ##-----------------------------------

# Our Netwoork Message Format:
#     '<[Two Letter Action]:[Relevant Data]>'
#     Example '<VS:1>' for Vote Start = True

VOTE_ACTION: str = "VS"
VOTE_NO_MESSAGE: str = "<VS:0>"
VOTE_YES_MESSAGE: str = "<VS:1>"
    
def send_message(sock: socket.socket, message: str):
    """ Send msg block. """
    pack = msgpack.packb(message)
    sock.send(pack)

def receive_message(sock: socket.socket) -> str:
    """ Receive a msg block. """
    pack = sock.recv(1024)
    message = msgpack.unpackb(pack)
    return message

def process_client_message(connection: socket.socket, message: str, connected_players: {socket.socket, Player}): # TODO
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
    
    
