from kmk.keys import KC

OBJ_MAP = {}
CODE_MAP = {}

# 1. Standard KMK key names to index
COMMON_KEYS = (
    "NO", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "N0",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
    "ENTER", "ESC", "BSPC", "TAB", "SPC", "MINUS", "EQUAL", "LBRC", "RBRC", "BSLASH",
    "SCOLON", "QUOTE", "GRAVE", "COMM", "DOT", "SLASH", "CAPS",
    "LCTRL", "LSHIFT", "LALT", "LGUI", "RCTRL", "RSHIFT", "RALT", "RGUI",
    "UP", "DOWN", "LEFT", "RIGHT", "HOME", "END", "PGUP", "PGDN", "DEL", "INS", "PSCR"
)

# 2. USB HID code fallback table
HID_FALLBACK = {
    4: "KC.A", 5: "KC.B", 6: "KC.C", 7: "KC.D", 8: "KC.E", 9: "KC.F", 10: "KC.G",
    11: "KC.H", 12: "KC.I", 13: "KC.J", 14: "KC.K", 15: "KC.L", 16: "KC.M", 17: "KC.N",
    18: "KC.O", 19: "KC.P", 20: "KC.Q", 21: "KC.R", 22: "KC.S", 23: "KC.T", 24: "KC.U",
    25: "KC.V", 26: "KC.W", 27: "KC.X", 28: "KC.Y", 29: "KC.Z",
    30: "KC.N1", 31: "KC.N2", 32: "KC.N3", 33: "KC.N4", 34: "KC.N5",
    35: "KC.N6", 36: "KC.N7", 37: "KC.N8", 38: "KC.N9", 39: "KC.N0",
    40: "KC.ENTER", 41: "KC.ESC", 42: "KC.BSPC", 43: "KC.TAB", 44: "KC.SPC",
    45: "KC.MINUS", 46: "KC.EQUAL", 47: "KC.LBRC", 48: "KC.RBRC", 49: "KC.BSLASH",
    51: "KC.SCOLON", 52: "KC.QUOTE", 53: "KC.GRAVE", 54: "KC.COMM", 55: "KC.DOT",
    56: "KC.SLASH", 57: "KC.CAPS",
    58: "KC.F1", 59: "KC.F2", 60: "KC.F3", 61: "KC.F4", 62: "KC.F5", 63: "KC.F6",
    64: "KC.F7", 65: "KC.F8", 66: "KC.F9", 67: "KC.F10", 68: "KC.F11", 69: "KC.F12",
    70: "KC.PSCR", 74: "KC.HOME", 75: "KC.PGUP", 76: "KC.DEL", 77: "KC.END",
    78: "KC.PGDN", 79: "KC.RIGHT", 80: "KC.LEFT", 81: "KC.DOWN", 82: "KC.UP"
}

def _init_maps():
    global OBJ_MAP, CODE_MAP
    if OBJ_MAP:
        return

    # Index explicit KMK key objects
    for name in COMMON_KEYS:
        try:
            k_obj = getattr(KC, name, None)
            if k_obj is not None:
                OBJ_MAP[k_obj] = f"KC.{name}"
                code = getattr(k_obj, "code", None)
                if code is not None:
                    CODE_MAP[code] = f"KC.{name}"
        except Exception:
            pass

def key_to_str(key_obj):
    """Converts any active KMK Key object back to its 'KC.NAME' string representation."""
    if not key_obj:
        return "KC.NO"

    _init_maps()

    # Match exact key object
    if key_obj in OBJ_MAP:
        return OBJ_MAP[key_obj]

    # Match by key code
    code = getattr(key_obj, "code", None)
    if code in CODE_MAP:
        return CODE_MAP[code]
    if code in HID_FALLBACK:
        return HID_FALLBACK[code]

    return "KC.NO"

def save_layout(keyboard, layout_name="custom"):
    """Serializes active keymap layer into a layout Python file."""
    if not keyboard.keymap or not keyboard.keymap[0]:
        print("[Exporter Error]: Keymap is empty.")
        return False

    layer = keyboard.keymap[0]
    keys_str = [key_to_str(k) for k in layer]

    # Format into clean rows of 7 keycodes
    rows = []
    for i in range(0, len(keys_str), 7):
        chunk = keys_str[i:i+7]
        rows.append("    " + ", ".join(chunk) + ",")

    file_content = f"""# Automatically generated layout: {layout_name}
from kmk.keys import KC
from layout import get_mappings

mapping = get_mappings()

keymap = [
{chr(10).join(rows)}
]
"""

    filepath = f"layouts/{layout_name}.py"
    try:
        with open(filepath, "w") as f:
            f.write(file_content)
        print(f"\n[Layout Saved]: Successfully exported to '{filepath}'")
        return True
    except Exception as e:
        print(f"\n[Layout Save Failed]: {e}")
        return False
