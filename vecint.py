class VecInt:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        assert isinstance(x, int), "x value of vector is not an integer"
        assert isinstance(y, int), "y value of vector is not an integer"
        self.x = x
        self.y = y