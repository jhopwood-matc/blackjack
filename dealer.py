
from requests import request, Response
from player import Player

class Dealer:

    deck_info: dict[str, str]   # metadata about deck that dealer is using
    deck_id: str                # id of deck for use by api
    limit: int                  # number at which the dealer will stop taking hits
    hand: list[dict[str,str]]   # the dealers hand of cards
    
    def __init__(self) -> None:

        self.limit = 17
        self.hand = []

        # Get 3 decks worth of cards as deck
        deck_count: str = "3"
        url: str = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=" + deck_count
        payload = {}
        headers = {}

        # request deck from website
        response: Response = request("GET", url, headers=headers, data=payload)

        self.deck_info = response.json()
        self.deck_id = self.deck_info["deck_id"]

    def draw_card(self) -> dict[str,str]:
        url: str = "http://deckofcardsapi.com/api/deck/" + self.deck_id + "/draw/?count=1"
        payload = {}
        headers = {}
        # request info with card from website
        response: Response = request("GET", url, headers=headers, data=payload)
        info = response.json()
        # extract card from info
        card: dict[str,str] = info['cards'][0]

        return card

    def deal_cards(self, players: list[Player]) -> None:

        # Dealer gets one card (face up)
        self.hand.append(self.draw_card())

        # Players each get two cards
        for player in players:
            player.hand.append(self.draw_card())
            player.hand.append(self.draw_card())

        # Dealer gets last card (face down)
        self.hand.append(self.draw_card())
        
    
    def count_cards(self, hand: list[dict[str,str]]) -> int:

        total = 0
        big_ace_count = 0

        for card in hand:

            if card['value'] == 'JACK':
                total += 10
            elif card['value'] == 'QUEEN':
                total += 10
            elif card['value'] == 'KING':
                total += 10
            elif card['value'] == 'ACE':
                total += 11
                big_ace_count += 1
            else:
                total += int(card['value'])

            while total > 21 and big_ace_count > 0:
                total -= 10
                big_ace_count -= 1

        return total
        
dealer: Dealer = Dealer()

player1: Player = Player(100.0)
player2: Player = Player(100.0)

list_of_players: list[Player] = [player1, player2]

dealer.deal_cards(list_of_players)

for player in list_of_players:
    print(f"Total is {dealer.count_cards(player.hand)}")
    for card in player.hand:
        print(card["value"])
