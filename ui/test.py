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
    rect_3 = Rect(1, 12, 50, 50, outline=0xFFFFFF)
    Screen_1.append(rect_3)
    # string 4
    string_4 = label.Label(terminalio.FONT, text="Mode:", color=0xFFFFFF)
    string_4.x = 52
    string_4.y = 16
    Screen_1.append(string_4)
    # usb_cable_connected
    image_usb_cable_connected_tile = displayio.TileGrid(
    image_usb_cable_connected_bits,
    pixel_shader=image_usb_cable_connected_bits.pixel_shader,
    x=10,
    y=20
)
    Screen_1.append(image_usb_cable_connected_tile)
    # Lock
    image_Lock_tile = displayio.TileGrid(image_Lock_bits, pixel_shader=image_Lock_bits.pixel_shader, x=82, y=53)
    Screen_1.append(image_Lock_tile)
    # GameMode
    image_GameMode_tile = displayio.TileGrid(image_GameMode_bits, pixel_shader=image_GameMode_bits.pixel_shader, x=93, y=53)
    Screen_1.append(image_GameMode_tile)
    # Rpc_active
    image_Rpc_active_tile = displayio.TileGrid(image_Rpc_active_bits, pixel_shader=image_Rpc_active_bits.pixel_shader,x=107 ,y=53)
    Screen_1.append(image_Rpc_active_tile)
    # Alert
    image_Alert_tile = displayio.TileGrid(image_Alert_bits, pixel_shader=image_Alert_bits.pixel_shader, x=117, y=53)
    Screen_1.append(image_Alert_tile)
# [END lopaka generated]
    return Screen_1
