import sys
import board
import digitalio
import displayio
import i2cdisplaybus
import vectorio
import supervisor
import microcontroller
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from terminalio import FONT
from kmk.extensions import Extension
from i2c_bus import i2c

# 1. OLED Hardware Initialization
displayio.release_displays()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
oled = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

main_group = displayio.Group()
oled.root_group = main_group

palette = displayio.Palette(1)
palette[0] = 0xFFFFFF


# 3. Drawing Helpers
def addBox(x, y, width, height):
    rect = vectorio.Rectangle(pixel_shader=palette, width=width, height=height, x=x, y=y)
    main_group.append(rect)
    return rect

def addCircle(x, y, radius):
    circle = vectorio.Circle(pixel_shader=palette, radius=radius, x=x, y=y)
    main_group.append(circle)
    return circle

def addText(x, y, text_str):
    text_area = label.Label(FONT, text=text_str, color=0xFFFFFF, x=x, y=y)
    main_group.append(text_area)
    return text_area

def clear():
    while len(main_group) > 0:
        main_group.pop()

# 4. KMK Extension Class
class DisplayController(Extension):
    def __init__(self) -> None:
        self.last_state = {name: True for name in buttons}
        self.input_buffer = ""

    # KMK Lifecycle Stubs
    def during_bootup(self, keyboard): pass
    def after_matrix_scan(self, keyboard): pass
    def before_hid_send(self, keyboard): pass
    def after_hid_send(self, keyboard): pass
    def on_powersave_enable(self, keyboard): pass
    def on_powersave_disable(self, keyboard): pass

    def before_matrix_scan(self, keyboard):
        # Watchdog reset
        microcontroller.watchdog.feed()

        # Non-blocking Serial Listener
        if supervisor.runtime.serial_bytes_available:
            char = sys.stdin.read(1)
            sys.stdout.write(char)
            if char in ('\r', '\n'):
                cmd = self.input_buffer.strip().lower()
                self.process_command(cmd)
                self.input_buffer = ""
            else:
                self.input_buffer += char

        # Check GPIO Buttons
        for name, pin in buttons.items():
            current_btn = pin.value
            if not current_btn and self.last_state[name]: 
                print(f'\nBUTTON: {name} pressed!')
            self.last_state[name] = current_btn

    def process_command(self, cmd):
        print(f"\n[Received]: '{cmd}'")
        if cmd == "box":
            addBox(x=10, y=10, width=30, height=30)
        elif cmd == "circle":
            addCircle(x=64, y=32, radius=15)
        elif cmd.startswith("text "):
            addText(x=5, y=50, text_str=cmd[5:])
        elif cmd == "clear":
            clear()
        else:
            print(f"Unknown command: '{cmd}'")
