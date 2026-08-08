import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.rect import Rect



image_Alert_bits = displayio.OnDiskBitmap("/ui/textures/Alert.bmp")
image_GameMode_bits = displayio.OnDiskBitmap("/ui/textures/GameMode.bmp")
image_Lock_bits = displayio.OnDiskBitmap("/ui/textures/Lock.bmp")
image_Rpc_active_bits = displayio.OnDiskBitmap("/ui/textures/Rpc_active.bmp")
image_usb_cable_connected_bits = displayio.OnDiskBitmap("/ui/textures/usb_cable_connected.bmp")


def get_group():
    Screen_1 = displayio.Group() 
    # line 1
    line_1 = Line(0, 10, 128, 10, color=0xFFFFFF)
    Screen_1.append(line_1)
    # string 2
    string_2 = label.Label(terminalio.FONT, text="EDIOS v2", color=0xFFFFFF)
    string_2.x = 1
    string_2.y = 4
    Screen_1.append(string_2)
    # rect 3
    return Screen_1
