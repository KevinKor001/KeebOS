for display buttons:

# Physical GPIO Side-Buttons
buttons = {
    "up": digitalio.DigitalInOut(board.GP16),
    "down": digitalio.DigitalInOut(board.GP17),
    "hasthag": digitalio.DigitalInOut(board.GP18),
    "star": digitalio.DigitalInOut(board.GP19),
}


