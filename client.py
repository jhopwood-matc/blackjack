from connectionresult import ConnectionResult
from connectionthread import ConnectionThread
from menubuilder import MenuBuilder
from vecint import VecInt

from pygame import init, QUIT, quit, MOUSEBUTTONDOWN
from pygame.font import SysFont
from pygame.surface import Surface
from pygame.display import set_mode as pgd_set_mode
from pygame.display import set_caption as pgd_set_caption
from pygame.key import get_pressed as pgk_get_pressed
from pygame.event import get as pge_get
from pygame.mouse import get_pos as pgm_get_pos
from pygame.mouse import get_pressed as pgm_get_pressed
from pygame.display import flip as pgd_flip

from socket import socket, AF_INET, SOCK_STREAM
from sys import exit



# Initialize the TCP socket that will connect the game server
sock = socket(AF_INET, SOCK_STREAM)
# sock.setsockopt(socket.SO_REUSEADDR, ) TODO: FIX
sock.setblocking(False)

# Initialize an address for use when connecting with multiplayer
dest_srvr_addr: tuple[str, int] = ("", 0)

DEFAULT_PORT: int = 51721

# Initialize and empty result of a potential connection (for safety)
connection_result: ConnectionResult = ConnectionResult()

# Instantiate a multiplayer connection negotiation thread for later use
# (for safety)
connection_attempt: ConnectionThread

# Initialize Pygame Library
init()

# Initialize game's font
game_font = SysFont("ubuntumono", 24)

# ---- Initialize Window ---- 

# Declare the window properties and initialize window
window_width: int = 900
window_height: int = 600
window: Surface = pgd_set_mode((window_width, window_height))

# Change the window's title
pgd_set_caption("Blackjack")

# Views | More aptly "screens" on the client
# Refer to MVC (Model View Controller) architecture for more
MAIN_MENU:  str = "Main Menu"
RULES:      str = "Rules"
GAME_START: str = "Game Start"
GET_NAME:   str = "Get Name"
GET_SERVER: str = "Get Server"
CONNECTING: str = "Connecting"
CONNECTION_FAIL_NO_RESPONSE: str = "Connection Failed, No Response"
CONNECTION_FAIL_BAD_NAME:    str = "Connection Failed, Bad Name"

# Default view of the program on boot is the main menu
view: str = MAIN_MENU

# ---- Initialize Menus ----

# Main Menu
main_menu_builder: MenuBuilder = MenuBuilder(window, game_font)
main_menu_builder.add_text_line("Welcome to BlackJack 0.1.7")
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

# Get Server Menu
get_server_menu_builder: MenuBuilder = MenuBuilder(window, game_font)
get_server_menu_builder.add_text_line("Enter the IP address of the game server:")
get_server_menu_builder.add_text_input_field(21)
get_server_menu_builder.add_button("Connect")
get_server_menu_builder.add_button("Go Back")
get_server_menu_builder.center()

# Connecting Menu
connecting_menu_builder: MenuBuilder = MenuBuilder(window, game_font)
connecting_menu_builder.add_text_line("Connecting..")
connecting_menu_builder.add_button("Cancel")
connecting_menu_builder.center()

# Connection Fail Bad Name Menu
confailbadname_menu_builder: MenuBuilder = MenuBuilder(window, game_font)
confailbadname_menu_builder.add_text_line("Connection aborted! Bad name.")
confailbadname_menu_builder.add_button("Go Back")
confailbadname_menu_builder.center()

confailrefuse_menu_builder: MenuBuilder = MenuBuilder(window, game_font)
confailrefuse_menu_builder.add_text_line("Connection faild!")
confailrefuse_menu_builder.add_button("Go Back")
confailrefuse_menu_builder.center()


# ---- Main ----
running: bool = True
while running:

    # At the beginning of each frame,
    # Stores the position of any mouse activity, initialized to 40k for safety
    click_x: int = 40000
    click_y: int = 40000
    click_location: VecInt = VecInt(click_x, click_y)

    # user key and mouse input events per frame
    pygame_events = pge_get()
    key_activity = pgk_get_pressed()

    # User input checking
    for event in pygame_events:

        # close the game if the X button is pressed
        if event.type == QUIT:
            running = False
            quit()
            exit()
        
        # get the position of click when a click happens
        if event.type == MOUSEBUTTONDOWN:
            if pgm_get_pressed()[0]:
                click_x, click_y = pgm_get_pos()
                click_location: VecInt = VecInt(click_x, click_y)

    # When in the Main Menu view...
    if view == MAIN_MENU:

        # Go to 'Rules' screen when [Rules] button is clicked
        if main_menu_builder.button_is_clicked("Rules", click_location):
            view = RULES
        
        # Go to 'Enter a name' screen when [Multiplayer] button is clicked
        if main_menu_builder.button_is_clicked("Multiplayer", click_location):
            view = GET_NAME

        # apply background color to window
        window.fill((175, 175, 160))
        # display the view's menu
        main_menu_builder.draw()
        # switch buffer
        pgd_flip()
        
    # When in the rules view    
    elif view == RULES:
        
        # Return to the main menu when the [Go Back] button is clicked 
        if rules_menu_builder.button_is_clicked("Go Back", click_location):
            view = MAIN_MENU

        # apply background color to window
        window.fill((175, 175, 160))
        # display the view's menu
        rules_menu_builder.draw()
        # switch buffer
        pgd_flip()

    # When in the 'get name' view...
    elif view == GET_NAME:

        # Accept the name submission and proceed to the "Enter a server address"
        # view when the [Accept] button is clicked
        if get_name_menu_builder.button_is_clicked("Accept", click_location):
            view = GET_SERVER

        # Return to the main menu when the [Go Back] button is clicked
        if get_name_menu_builder.button_is_clicked("Go Back", click_location):
            view = MAIN_MENU

        # update the textbox in the name field each from to show the user's typing
        for _, textbox in get_name_menu_builder.text_input_fields:
            textbox.update(pygame_events, key_activity)

        # apply background color to window
        window.fill((175, 175, 160))
        # display the view's menu
        get_name_menu_builder.draw()
        # switch buffer
        pgd_flip()

    elif view == GET_SERVER:

        # Return to 'enter a name' screen when [Go Back] button is clicked
        if get_server_menu_builder.button_is_clicked("Go Back", click_location):
            view = GET_NAME

        # Proceed to appropriate screen when [Connect] button is clicked
        # Either:
        # good ip address -> 'Connecting..' screen
        # bad ip address  -> 'Connection failed! Bad IP' screen
        if get_server_menu_builder.button_is_clicked("Connect", click_location):

            # Extract the destination server address from the text field that the user typed
            input_addr: str = get_server_menu_builder.text_input_fields[0][1].get_text()

            # split the address into the four octets
            split_input_addr: list[str] = input_addr.split(".")

            # Proceed with validation only if it four octets long
            if split_input_addr.__len__() == 4:
                try:
                    # proceed if each octect is a number between 0 and 255
                    for octet in split_input_addr:
                        if 0 <= int(octet) <= 255:
                            dest_srvr_addr = (input_addr, DEFAULT_PORT)
                            # Change over to the "Connecting..." view
                            view = CONNECTING
                            # Create & start a thread to make a connection to destination server
                            connection_attempt = ConnectionThread(sock, dest_srvr_addr, connection_result)
                            connection_attempt.start()
                        else:
                            view = CONNECTION_FAIL_BAD_NAME
                except ValueError:
                    view = CONNECTION_FAIL_BAD_NAME
            else:
                view = CONNECTION_FAIL_BAD_NAME 


        # Update the text field for what the user is typing
        for _, textbox in get_server_menu_builder.text_input_fields:
            textbox.update(pygame_events, key_activity)

        # Set the background color
        window.fill((175, 175, 160))
        # Show the menu for this screen
        get_server_menu_builder.draw()
        # switch the buffer
        pgd_flip()
        
    # When in the "Connecting..." view
    elif view == CONNECTING:

        # Return to "Enter a server Address" view and destroy connection negotiation
        # thread if the user clicks on the [Cancel] button
        if connecting_menu_builder.button_is_clicked("Cancel", click_location):
            # destroy the the connection thread..
            connection_attempt.join(0.1)
            view = GET_SERVER

        # Show the "Connection failed, no response" view if/when the connection 
        # thread stops and the result was a failure
        if not connection_attempt.is_alive() and connection_result.fail == True:
            view = CONNECTION_FAIL_NO_RESPONSE
            
        # Set the background color
        window.fill((175, 175, 160))
        # Show the menu for this screen
        connecting_menu_builder.draw()
        pgd_flip()

    # when in at the "Connection Failed" view...
    elif view == CONNECTION_FAIL_NO_RESPONSE:

        # Return to "Enter a server Address" view when the [Go Back] button is clicked
        if confailrefuse_menu_builder.button_is_clicked("Go Back", click_location):
            view = GET_SERVER

        # Set the background color
        window.fill((175, 175, 160))
        # Show the menu for this screen
        confailrefuse_menu_builder.draw()
        pgd_flip()

    # When in the "Bad address" view...
    elif view == CONNECTION_FAIL_BAD_NAME:

        # Return to "Enter a server Address" view when the [Go Back] button is clicked
        if confailbadname_menu_builder.button_is_clicked("Go Back", click_location):
            view = GET_SERVER

         # Set the background color
        window.fill((175, 175, 160))
        # Show the menu for this screen
        confailbadname_menu_builder.draw()

        pgd_flip()

    elif view == GAME_START:
        pass

