from kmk.keys import KC
import ui
import layout_exporter



STATE_IDLE = "IDLE"
STATE_WAIT_KEY = "WAIT_KEY"
STATE_WAIT_CODE = "WAIT_CODE"

class BindTool:
    def __init__(self):
        self.state = STATE_IDLE
        self.target_key_num = None

    def start(self):
        """Step 1: Open modal and wait for physical key press."""
        self.state = STATE_WAIT_KEY
        self.target_key_num = None
        ui.manager.show_cmd_modal()
        ui.manager.update_cmd_text("Press key to bind...")
        print("\n[Bind Tool]: Ready. Press any physical key on keyboard...")

    def on_key_detected(self, key_number):
        """Step 2: Key captured; prompt for new keycode name."""
        self.state = STATE_WAIT_CODE
        self.target_key_num = key_number
        ui.manager.update_cmd_text(f"K#{key_number} -> KC.")
        print(f"\n[Bind Tool]: Selected Key #{key_number}.")
        print("[Bind Tool]: Type KMK keycode (e.g., A, SPC, LSHIFT, ENTER) & hit ENTER:")

    def apply_bind(self, keyboard, keycode_str):
        if self.target_key_num is None:
            self.cancel()
            return

        clean_code = keycode_str.strip().upper().replace("KC.", "")

        if hasattr(KC, clean_code):
            new_key = getattr(KC, clean_code)

            # Update live runtime layer
            layer = list(keyboard.keymap[0])
            if 0 <= self.target_key_num < len(layer):
                layer[self.target_key_num] = new_key
                keyboard.keymap[0] = layer
                print(f"\n[Bind Tool SUCCESS]: Key #{self.target_key_num} rebound to KC.{clean_code}")
                
                # Auto-save changes to layouts/custom_layout.py
             #   layout_exporter.save_layout(keyboard, "custom")
            else:
                print(f"\n[Bind Tool ERROR]: Key #{self.target_key_num} out of bounds.")
        else:
            print(f"\n[Bind Tool ERROR]: Invalid keycode 'KC.{clean_code}'")

        self.cancel()

    def cancel(self):
        """Reset state and close UI modal."""
        self.state = STATE_IDLE
        self.target_key_num = None
        ui.manager.hide_cmd_modal()
        print("[Bind Tool]: Cancelled.")

bind_tool = BindTool()
