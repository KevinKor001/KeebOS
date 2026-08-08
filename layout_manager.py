import layouts.base_layout as base

# Dynamically import custom layout if it exists
try:
    import layouts.custom_layout as custom
except ImportError:
    custom = None

layouts = {
    "base": base,
}
if custom:
    layouts["custom"] = custom

def load(name):
    return layouts.get(name)

def apply_layout(keyboard, name):
    layout_mod = load(name)
    if layout_mod and hasattr(layout_mod, "keymap"):
        keyboard.keymap = [layout_mod.keymap]
        return True
    return False
