class Player:

    wallet_amount: float
    vote: bool
    hand: list[dict[str, str]]
     
    def __init__(self, starting_wallet_amount: float) -> None:
        self.wallet_amount = 100.0 * starting_wallet_amount
        self.vote = False
        self.hand = []