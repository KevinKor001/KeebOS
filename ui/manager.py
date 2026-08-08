
import builtins
import displayio
import terminalio
from adafruit_display_text import label
import i2cdisplaybus
import adafruit_displayio_ssd1306
from i2c_bus import i2c
from ui import test, tty

# --- Global Print Intercept ---
_orig_print = builtins.print

def oled_print(*args, **kwargs):
    # 1. Terminal print
    _orig_print(*args, **kwargs)
    
    # 2. Stream to OLED TTY screen
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")
    msg = sep.join(str(arg) for arg in args) + end
    tty.write_stream(msg)

builtins.print = oled_print

# --- Hardware Setup ---
displayio.release_displays()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
oled = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

root_container = displayio.Group()
window_container = displayio.Group()
modal_container = displayio.Group()

root_container.append(window_container)
root_container.append(modal_container)  # Modal renders on top of active window
oled.root_group = root_container

# --- Command Modal UI Elements ---
modal_label = label.Label(
    terminalio.FONT,
    text="> ",
    color=0xFFFFFF,
    x=4,
    y=54
)
modal_container.append(modal_label)
modal_container.hidden = True

# --- Window Router ---
windows = {
    "main": test.get_group,
    "tty": tty.get_group,
}

current_window = None

def show(window_name):
    """Switch active display view."""
    global current_window
    if window_name in windows:
        current_window = window_name
        while len(window_container) > 0:
            window_container.pop()
        window_container.append(windows[window_name]())
    else:
        _orig_print(f"[UI] Unknown window: {window_name}")

def show_cmd_modal():
    modal_container.hidden = False

def hide_cmd_modal():
    modal_container.hidden = True

def update_cmd_text(text_str):
    modal_label.text = f"> {text_str}"
