import displayio


class Widget(displayio.Group):
    def __init__(self, *, scale: int = 1, x: int = 0, y: int = 0,width: int =1, height: int =1) -> None:
        super().__init__(scale=scale, x=x, y=y)
        self.width = width
        self.height = height
    def update(self):
        pass
