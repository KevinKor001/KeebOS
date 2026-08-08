from kmk.keys import KC
from layout import get_mappings

mapping = get_mappings()

# KEYMAP MUST MATCH SIZE OF mapping[]
keymap = [
        # LEFT (PICO)
        KC.ESC,   KC.N1,   KC.N2,   KC.N3,   KC.N4, KC.N5 ,KC.GRAVE,
        KC.TAB,   KC.Q,   KC.W,   KC.E,   KC.R, KC.T,KC.LBRC,
        KC.LGUI,   KC.A,   KC.S,   KC.D,   KC.F, KC.G,KC.SCOLON,
        KC.LSHIFT,  KC.Z,  KC.X,  KC.C,  KC.V, KC.B,

        # LEFT THUMB CLUSTER
        KC.HOME,  KC.LCTRL, KC.LEFT, KC.UP, KC.DOWN,KC.RIGHT,  KC.CAPS,KC.SLASH,KC.NO,KC.NO,KC.NO,KC.NO,KC.SPC,KC.DEL,KC.HOME,

        # RIGHT (MCP)
        KC.LGUI,   KC.F11,   KC.F10,   KC.F9,   KC.DOT, KC.PSCR,KC.F2,
        KC.RCTRL,   KC.SCOLON,    KC.COMM,  KC.DOT,   KC.M, KC.N, KC.END,
        KC.RSHIFT,   KC.QUOTE,   KC.L, KC.K, KC.J, KC.H, KC.BSLASH,
        KC.MINUS,  KC.P,  KC.O,   KC.I,  KC.U, KC.Y, KC.RBRC,
        KC.EQUAL, KC.N0, KC.N9, KC.N8, KC.N7, KC.N6, KC.NO,KC.NO,KC.NO,KC.NO,KC.NO,KC.BSPC,KC.ENTER,

        # RIGHT THUMB CLUSTER
        KC.RALT, KC.RCTRL, KC.PGUP, KC.ENTER, KC.LBRC, KC.PGDN,
    ]
