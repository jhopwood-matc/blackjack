from xfn import get_name
from xfn import get_starting_wallet_value
from xfn import main_menu
from xfn import print_rules
from xfn import MAIN_MENU, GAME_START, RULES, send_message, VOTE_YES_MESSAGE, play_game

import socket

# Init
view: str = MAIN_MENU

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Main
running: bool = True
while running:

    if view == MAIN_MENU:
        view = main_menu()
        
    elif view == RULES:
        view = print_rules()

    elif view == GAME_START:
        view = play_game(sock)

