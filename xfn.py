
from typing import Callable
import socket

import pygame

# https://pypi.org/project/msgpack/
import msgpack


class Player:

    wallet_amount: float
    vote: bool
     
    def __init__(self, starting_wallet_amount: float) -> None:
        self.wallet_amount = 100.0 * starting_wallet_amount
        self.vote = False

class VecInt:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        assert isinstance(x, int), "x value of vector is not an integer"
        assert isinstance(y, int), "y value of vector is not an integer"
        self.x = x
        self.y = y
    
class Button:

    window: pygame.surface.Surface          # Window the button is rendered in
    location: VecInt                        # Screen coordinates of button in the window
    text: str                               # What the button says
    font: pygame.font.Font                  # font object that dictates the button's text's style
    rendered_text: pygame.surface.Surface   # actual image of the text that gets displayed
    border_thickness: int                   # space between button text and button's edge
    height: int                             # height of button
    width: int                              # width of button

    def __init__(self, window: pygame.surface.Surface, location: VecInt, text: str, font: pygame.font.Font) -> None:
        assert isinstance(window, pygame.surface.Surface), "window is not a Surface"
        assert isinstance(location, VecInt), "`location` is not a VecInt"
        assert isinstance(text, str), "`text` is not a str"
        assert isinstance(font, pygame.font.Font), "font is not a Font"
        
        self.window = window
        self.text = text
        self.location = location
        self.font = font

        self.rendered_text = self.font.render(self.text, True, (0, 0, 0))

        BORDER_RATIO_VALUE: float = 0.20

        # Derive the size (dimensions) of the text field box from the size of the font
        self.width, self.height = self.font.size(self.text)
        self.border_thickness = BORDER_RATIO_VALUE * self.height
        # adjust the dimensions to add the extra space between the letters and 
        # the edge of the text box
        self.width += (2 * self.border_thickness)
        self.height += (2 * self.border_thickness)

    def get_width(self):
        return self.width

    def set_location(self, location: VecInt):
        assert isinstance(location, VecInt), "location is not a VecInt"
        self.location = location    

    def is_clicked(self, click_location: VecInt) -> bool:
        assert isinstance(click_location, VecInt), "Location of click is in correct format"
        clicked_x = self.location.x <= click_location.x <= (self.location.x + self.width)
        clicked_y = self.location.y <= click_location.y <= (self.location.y + self.height)
        if clicked_x and clicked_y:
            return True
    
    def draw(self):
        pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(self.location.x, self.location.y, self.width, self.height))
        self.window.blit(self.rendered_text, (self.location.x + self.border_thickness, self.location.y + self.border_thickness))

class RenderedText:
    """
    Graphical text that is for the screen
    """
    window: pygame.surface.Surface # Window the text is renedered in
    text: str                      # What the text says
    font: pygame.font.Font         # Font object that dictates its style
    location: VecInt               # Screen coordinates in the window
    render: pygame.surface.Surface # (The rendered image of the text is stored here)

    def __init__(self, window: pygame.surface.Surface, text: str, font: pygame.font.Font, location: VecInt) -> None:
        """
        Create a new RenederedText!
        """
        # TODO asserting
        self.window = window
        self.text = text
        self.font = font
        self.location = location
        self.render = self.font.render(self.text, True, (0, 0, 0))    

    def get_width(self):
        return self.render.get_width()
    
    def set_location(self, location: VecInt):
        """
        Define or redefine the screen coordinate location of the RenderedText
        """
        assert isinstance(location, VecInt), "location is not a VecInt"
        self.location = location

    def draw(self):
        """
        Procedure displays RenderedText visually in window
        """
        self.window.blit(self.render, (self.location.x, self.location.y))



keymap = {
    pygame.K_a: "a",
    pygame.K_b: "b",
    pygame.K_c: "c",
    pygame.K_d: "d",
    pygame.K_e: "e",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_m: "m",
    pygame.K_n: "n",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_s: "s",
    pygame.K_t: "t",
    pygame.K_u: "u",
    pygame.K_v: "v",
    pygame.K_w: "w",
    pygame.K_x: "x",
    pygame.K_y: "y",
    pygame.K_z: "z",
    pygame.K_SPACE: " ",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",
    pygame.K_0: "0",
    pygame.K_PERIOD: ".",
    pygame.K_SEMICOLON: ";",
    pygame.K_COMMA: ",",
}

letters = "abcdefghijklmnopqrstuvwxyz"



class TextInputField:
    """
    A `TextInputField` is used when the developer intends to have a user input text with
    the GUI. It displays as an empty box that will automatically pick up keyboard typing
    and dynamially update to display what the user is typing. 
    """

    window: pygame.surface.Surface          # Window the text is renedered in
    location: VecInt                        # Screen coordinates in the window
    text: str                               # stores the text that is input
    font: pygame.font.Font                  # Font object that dictates its style
    rendered_text: pygame.surface.Surface   # (The rendered image of the text is stored here)
    char_limit: int                         # max length of text a user can type (in characters)
    border_thickness: int                   # space between the letters and field's border in pixels
    height: int                             # height of text field graphical box
    width: int                              # width of text field graphical box

    def __init__(self, window: pygame.surface.Surface, location: VecInt, font: pygame.font.Font, char_limit: int) -> None:
        assert isinstance(char_limit, int), "char_limit is not an int"
        assert isinstance(window, pygame.surface.Surface), "window is not a Surface"
        assert isinstance(location, VecInt), "`location` is not a VecInt"
        assert isinstance(font, pygame.font.Font), "font is not a Font"
        
        self.window = window
        self.location = location
        self.text = ""
        self.font = font
        self.char_limit = char_limit

        # Initilize the rendered text image to nothing
        self.rendered_text = self.font.render(" ", 1, (255,255,255))

        BORDER_RATIO_VALUE: float = 0.20

        # Derive the size (dimensions) of the text field box from the size of the font
        self.width, self.height = self.font.size("_" * self.char_limit)
        self.border_thickness = BORDER_RATIO_VALUE * self.height
        # adjust the dimensions to add the extra space between the letters and 
        # the edge of the text box
        self.width += (2 * self.border_thickness)
        self.height += (2 * self.border_thickness)

    def set_location(self, location: VecInt):
        """
        Change the location of the text field
        """
        assert isinstance(location, VecInt), "location is not a VecInt"
        self.location = location
    
    def update_text(self, more_text: str, backspace: bool = False):
        """
        Update the text displayed in the input field. This can handle both appending
        text and deleteing (backspacing) text. 
        """
        if backspace == True: # Backspacing
            self.text = self.text[0:-1:1]
            self.rendered_text = self.font.render(self.text, 1, (255,255,255))

        else: # Typing text
            if self.text.__len__() >= self.char_limit: # Exceedeing character limit
                pass                                   # No more typing!
            else: # Not exceeding character limit (appending letters to text)
                self.text = self.text + more_text
                self.rendered_text = self.font.render(self.text, 1, (255,255,255))

    def get_text(self):
        """
        Use this to obtain the text input that a user has put into the text field box. 
        """
        return self.text
    
    def get_width(self):
        return self.width
    
    def update(self, pygame_events: list[pygame.event.Event], key_activity: pygame.key.ScancodeWrapper):
        """
        This function accepts a list of user input (pygame_events) and keypress states (key_activity).
        From these information, it changes the state of the TextInputField to reflect what the user
        is inputing -i.e. typing.

        Call this function onces per frame to make the TextInputField typing functionality work. 
        """
        #TODO: ASSERTS
        for event in pygame_events:
            if event.type == pygame.KEYDOWN:
                for pg_key in keymap:
                    is_pressed: bool = event.key == pg_key
                    is_lshift_active: bool = key_activity[pygame.K_LSHIFT]
                    is_letter: bool = keymap[pg_key] in letters

                    if is_pressed and is_lshift_active and is_letter:
                        self.update_text(keymap[pg_key].upper())
                    elif is_pressed and is_lshift_active and pg_key == pygame.K_SEMICOLON:
                        self.update_text(":")
                    elif is_pressed:
                        self.update_text(keymap[pg_key])
                if event.key == pygame.K_BACKSPACE:
                    self.update_text("", True)

    def draw(self):
        """
        Display the text input field box graphically on the screen for a frame.
        """
        # Graphical box that represents the field on the screen
        pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(self.location.x, self.location.y, self.width, self.height))
        # Rendered text within the field
        self.window.blit(self.rendered_text, (self.location.x + self.border_thickness, self.location.y + self.border_thickness))



CENTER: int = 0
LEFT: int = 1



class MenuBuilder:
    """
    The text lines and buttons WILL display in order with respect to which the order that they
    were added in. Keep this in mind.
    """

    window: pygame.surface.Surface                  # window the menu is in
    font: pygame.font.Font                          # font of the menu's text
    location: VecInt                                # coordinates of menu in window
    rendered_text_lines: list[(int, RenderedText)]  # list of actual images of menu text
    buttons: dict[str, (int, Button)]               # list of menus buttons
    text_input_fields: list[(int, TextInputField)]  # list of places for user to type text
    line_id_counter: int                            # counts and assigns menu elements line numbers (IDs)
    space_between_elements: int                     # vertical space in pixels between menu element LOCATIONS!
    justification: int                              # style of menu justification
    longest_line_length: int                        # length of longest menu element in pixels (used for justification)

    def __init__(self, window: pygame.surface.Surface, font: pygame.font.Font, justification: int = 0) -> None:
        """
        Create a new Menu!

        justification guide
        0 = center
        1 = left
        """
        assert isinstance(window, pygame.surface.Surface), "window is not a pygame.surface.Surface!"
        assert isinstance(font, pygame.font.Font), "font is not a pygame.font.Font!"

        self.window = window
        self.font = font
        self.location = VecInt(0, 0)
        self.rendered_text_lines = []
        self.buttons = {}
        self.text_input_fields = []
        self.line_id_counter = 0

        BORDER_RATIO_VALUE: float = 0.20
        self.space_between_elements = int(self.font.get_height() * (1 + 3 * BORDER_RATIO_VALUE))

        self.justification = justification
        self.longest_line_length = 0

    def update_component_locations(self):
        """
        Called internally by when the location of the menu is redefined
        with .set_location() or when a new element is added. 
        """

        # Check for center justification style
        if self.justification == CENTER:

            # Find the length of the longest element
            for _, text in self.rendered_text_lines:
                length: int = text.get_width()
                if length > self.longest_line_length:
                    self.longest_line_length = length
            for key in self.buttons:
                length: int = self.buttons[key][1].get_width()
                if length > self.longest_line_length:
                    self.longest_line_length = length
            for _, box in self.text_input_fields:
                length: int = box.get_width()
                if length > self.longest_line_length:
                    self.longest_line_length = length

            for id, text in self.rendered_text_lines:
                offset: int = int((self.longest_line_length - text.get_width()) / 2)
                pos: VecInt = VecInt(self.location.x + offset, id * self.space_between_elements + self.location.y)
                text.set_location(pos)
            for key in self.buttons:
                offset: int = int((self.longest_line_length - self.buttons[key][1].get_width()) / 2)
                pos: VecInt = VecInt(self.location.x + offset, self.buttons[key][0] * self.space_between_elements + self.location.y)
                self.buttons[key][1].set_location(pos)
            for id, box in self.text_input_fields:
                offset: int = int((self.longest_line_length - box.get_width()) / 2)
                pos: VecInt = VecInt(self.location.x + offset, id * self.space_between_elements + self.location.y)
                box.set_location(pos)

        # TODO LEFT JUSTIFCATION
        # Check for left justification style
        elif self.justification == LEFT:
            pos: VecInt = VecInt(self.location.x, self.line_id_counter * self.space_between_elements + self.location.y)
            for id, text in self.rendered_text_lines:
                pos: VecInt = VecInt(self.location.x, id * self.space_between_elements + self.location.y)
                text.set_location(pos)
            for key in self.buttons:
                pos: VecInt = VecInt(self.location.x, self.buttons[key][0] * self.space_between_elements + self.location.y)
                self.buttons[key][1].set_location(pos)
            # TODO Text fields

    def set_location(self, location: VecInt):
        """
        Define or redefine the window coordinate location of the menu
        """
        assert isinstance(location, VecInt), "location is not a VecInt"
        self.location = location
        self.update_component_locations()
        return self
    
    def center(self):
        """
        puts the menu in the mathematical near-perfect center of the screen. Call this last, as it does
        not update dynamically when more elements are added to the menu.
        """
        x: int = (self.window.get_width() - self.longest_line_length) / 2
        y: int = (self.window.get_height() - self.line_id_counter * self.space_between_elements) / 2
        pos: VecInt = VecInt(int(x), int(y))
        self.set_location(pos)
        self.update_component_locations()

    def add_text_line(self, text: str):
        """
        Add a line of text to the menu
        """
        assert isinstance(text, str), "text is not a str"
        self.rendered_text_lines.append((self.line_id_counter, RenderedText(self.window, text, self.font, VecInt(0,0))))
        self.line_id_counter+=1
        self.update_component_locations()
        return self
    
    def add_button(self, name: str):
        """
        Add a button to a menu.
        """
        assert isinstance(name, str), "name is not a str"
        # create a button without a specific location
        button: Button = Button(self.window, VecInt(0,0), name, self.font)

        # Add button to menu's button catalog    
        self.buttons[name] = (self.line_id_counter, button)

        self.update_component_locations()

        # Increase the line (element) count
        self.line_id_counter+=1
        return self
    
    def add_text_input_field(self, char_limit: int):
        """
        Add a space for users to type things in to the menu
        """
        assert isinstance(char_limit, int), "char_limit is not an int!"
        self.text_input_fields.append((self.line_id_counter, TextInputField(self.window, VecInt(0,0), self.font, char_limit)))

        self.update_component_locations()

        self.line_id_counter+=1
        return self
    
    def button_is_clicked(self, button_name: str, click_location: VecInt):
        """
        Wrapper Function to that will return True when a menu button is clicked.
        Written to eliminate complexity.
        """
        # TODO: Assert statements
        if self.buttons[button_name][1].is_clicked(click_location):
            return True

    def draw(self) -> None:
        """
        Display the menu visually in the window/ on the screen. 
        """
        for _, rt in self.rendered_text_lines:
            rt.draw()
        for b in self.buttons:
            self.buttons[b][1].draw()
        for _, f in self.text_input_fields:
            f.draw()
            

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
    
    
