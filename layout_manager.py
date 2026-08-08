import layouts.base_layout as base

# Load optional custom layout
try:
    import layouts.custom_layout as custom
except ImportError:
    custom = None

layouts = {
    "base": base,
}
if custom:
    layouts["custom"] = custom

# Global runtime state for layers
active_layout_name = "base"
layer_registry = {"base": 0}  # Map: "layer_name" -> index
edit_layer_idx = 0            # Target layer index for bind commands

def load(name):
    """Retrieve layout module by name."""
    return layouts.get(name)

def apply_layout(keyboard, name):
    """Loads a layout into KMK runtime and builds its layer registry."""
    global active_layout_name, layer_registry, edit_layer_idx

    layout_mod = load(name)
    if not layout_mod or not hasattr(layout_mod, "keymap"):
        return False

    raw_map = layout_mod.keymap

    # Ensure keymap is a 2D list: [ [layer_0], [layer_1], ... ]
    if isinstance(raw_map[0], list):
        keyboard.keymap = raw_map
    else:
        keyboard.keymap = [raw_map]

    # Rebuild layer registry
    layer_registry.clear()
    saved_registry = getattr(layout_mod, "layer_registry", None)

    if saved_registry and isinstance(saved_registry, dict):
        layer_registry.update(saved_registry)
    else:
        # Fallback registry generation
        for idx in range(len(keyboard.keymap)):
            layer_name = "base" if idx == 0 else f"layer_{idx}"
            layer_registry[layer_name] = idx

    active_layout_name = name
    edit_layer_idx = 0
    return True

def get_layer_index(layer_name_or_idx):
    """Resolves a layer name or string index into a valid integer index."""
    if isinstance(layer_name_or_idx, int):
        return layer_name_or_idx

    # Check named registry
    name_clean = str(layer_name_or_idx).strip().lower()
    if name_clean in layer_registry:
        return layer_registry[name_clean]

    # Check numeric string
    if name_clean.isdigit():
        idx = int(name_clean)
        if 0 <= idx < 32:
            return idx

    return None

def add_layer(keyboard, name, source_layout_name=None):
    """Adds a new layer by copying layer 0 OR importing another layout's base layer."""
    name_clean = str(name).strip().lower()

    if name_clean in layer_registry:
        print(f"[Layer Error]: Layer '{name_clean}' already exists.")
        return False

    new_layer_data = None

    # Option 1: Import base layer from another layout file
    if source_layout_name:
        src_mod = load(source_layout_name)
        if src_mod and hasattr(src_mod, "keymap") and len(src_mod.keymap) > 0:
            # Grab base layer from source layout
            src_layer = src_mod.keymap[0] if isinstance(src_mod.keymap[0], list) else src_mod.keymap
            new_layer_data = list(src_layer)
            print(f"[Layer Import]: Imported base layer from layout '{source_layout_name}'")
        else:
            print(f"[Layer Warning]: Source layout '{source_layout_name}' not found. Defaulting to base copy.")

    # Option 2: Default copy of active layer 0
    if not new_layer_data:
        new_layer_data = list(keyboard.keymap[0])

    keyboard.keymap.append(new_layer_data)
    new_idx = len(keyboard.keymap) - 1
    layer_registry[name_clean] = new_idx
    print(f"[Layer Added]: '{name_clean}' at index {new_idx}")
    return True
