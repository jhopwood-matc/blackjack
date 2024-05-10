class ConnectionResult:
    fail: bool
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail