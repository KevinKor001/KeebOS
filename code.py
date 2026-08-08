import board
from adafruit_mcp230xx.mcp23017 import MCP23017
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.digitalio import MatrixScanner
from kmk.scanners import DiodeOrientation
from i2c_bus import i2c
from layout_manager import load as load_layout
from command_receiver import CommandReceiver 
# 1. Initialize KMK Keyboard
keyboard = KMKKeyboard()
keyboard.verbose = False

keyboard.debug_enabled = False
scanners = []

# 2. Setup Scanners
# Left Half (Pico)
scanners.append(
    MatrixScanner(
        cols=(board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8),
        rows=(board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14),
        diode_orientation=DiodeOrientation.COL2ROW,
        offset=0,
    )
)

# Right Half (MCP23017 Expander)
try:
    mcp = MCP23017(i2c, address=0x20)
    scanners.append(
        MatrixScanner(
            cols=(mcp.get_pin(7), mcp.get_pin(6), mcp.get_pin(5),
                  mcp.get_pin(4), mcp.get_pin(3), mcp.get_pin(2), mcp.get_pin(1)),
            rows=(mcp.get_pin(8), mcp.get_pin(9), mcp.get_pin(10),
                  mcp.get_pin(11), mcp.get_pin(12), mcp.get_pin(13)),
            diode_orientation=DiodeOrientation.COL2ROW,
            offset=42,
        )
    )
    print("MCP OK")
except Exception as e:
    print(f"NO MCP → single-half mode ({e})")

keyboard.matrix = scanners

# 3. Add Display Extension & Keymap
keyboard.extensions.append(CommandReceiver())
current_layout = load_layout("base")
keyboard.keymap = [current_layout.keymap]

# 4. Run Loop
if __name__ == '__main__':
    keyboard.go()
