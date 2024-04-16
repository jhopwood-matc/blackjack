
from xfn import (
    send_message,
    VOTE_YES_MESSAGE,
    Button,
    VecInt,
    MenuBuilder,
    TextInputField,
    keymap,
    letters,
    )
import socket
import pygame
import sys

# Initialize the TCP socket that will connect the game server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialize Pygame Library
pygame.init()

# Initialize game's font
game_font = pygame.font.SysFont("ubuntumono", 24)

# ---- Initialize Window ---- 

# Declare the window
window_width: int = 900
window_height: int = 600
window: pygame.surface.Surface = pygame.display.set_mode((window_width, window_height))

# Change the window's title
pygame.display.set_caption("Blackjack")

# Views
MAIN_MENU:  str = "Main Menu"
RULES:      str = "Rules"
GET_NAME:   str = "Get Name"
GAME_START: str = "Game Start"

view: str = MAIN_MENU

# ---- Initialize Menus ----

# Main Menu
main_menu_builder: MenuBuilder = MenuBuilder(window, game_font)
main_menu_builder.add_text_line("Welcome to BlackJack 0.1.1.")
main_menu_builder.add_button("Multiplayer")
main_menu_builder.add_button("Rules")
main_menu_builder.center()

# Rules Menu
rules_menu_builder: MenuBuilder = MenuBuilder(window, game_font)
rules_menu_builder.set_location(VecInt(20, 20))
rules_menu_builder.add_button("Go Back")

# Get Name Menu
get_name_menu_builder: MenuBuilder = MenuBuilder(window, game_font)
get_name_menu_builder.add_text_line("Give yourself a name:")
get_name_menu_builder.add_text_input_field(25)
get_name_menu_builder.add_button("Accept")
get_name_menu_builder.add_button("Go Back")
get_name_menu_builder.center()


# ---- Main ----
running: bool = True
while running:

    # Stores the position of any mouse activity, initialized to 40k for safety
    click_x: int = 40000
    click_y: int = 40000
    click_location: VecInt = VecInt(click_x, click_y)

    # user key and mouse input events per frame
    pygame_events = pygame.event.get()
    key_activity = pygame.key.get_pressed()

    # User input checking
    for event in pygame_events:

        # Handle clicking the [X] button on the window to shutdown the program
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        # Handle getting the postion of clicking when the user clicks.  
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                click_x, click_y = pygame.mouse.get_pos()
                click_location: VecInt = VecInt(click_x, click_y)

    if view == MAIN_MENU:

        # Handle an event that the Main Menu 'Rules' button being pressed
        if main_menu_builder.button_is_clicked("Rules", click_location):
            view = RULES
        
        # Handle an event that the Main Menu 'Multiplayer' button being pressed
        if main_menu_builder.button_is_clicked("Multiplayer", click_location):
            view = GET_NAME

        window.fill((175, 175, 160))
        main_menu_builder.draw()
        pygame.display.flip()

        # view = main_menu()
        
    if view == RULES:
        # Handle an event that the Rules Menu 'Go Back' button being pressed
        # Bring us back to the Main Menu screen
        if rules_menu_builder.button_is_clicked("Go Back", click_location):
            view = MAIN_MENU

        window.fill((175, 175, 160))
        rules_menu_builder.draw()
        pygame.display.flip()

    if view == GET_NAME:

        if get_name_menu_builder.button_is_clicked("Go Back", click_location):
            view = MAIN_MENU

        for _, textbox in get_name_menu_builder.text_input_fields:
            textbox.update(pygame_events, key_activity)

        window.fill((175, 175, 160))
        get_name_menu_builder.draw()
        pygame.display.flip()

    if view == GAME_START:
        
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
    
        # get name
        ## welcome_text


