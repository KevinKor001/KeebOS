import sys
import layout_manager
import board
import digitalio
import supervisor
import microcontroller
from kmk.extensions import Extension
import Display
from kmk.keys import KC
import ui
import layout_exporter
import bind_tool
from bind_tool import STATE_WAIT_KEY, STATE_WAIT_CODE

# Physical GPIO Side-Buttons
buttons = {
    "up": digitalio.DigitalInOut(board.GP16),
    "down": digitalio.DigitalInOut(board.GP17),
    "hasthag": digitalio.DigitalInOut(board.GP18),
    "star": digitalio.DigitalInOut(board.GP19),
}

# Simple keycode to ASCII conversion map
KEY_MAP = {
    KC.A: "a", KC.B: "b", KC.C: "c", KC.D: "d", KC.E: "e", KC.F: "f",
    KC.G: "g", KC.H: "h", KC.I: "i", KC.J: "j", KC.K: "k", KC.L: "l",
    KC.M: "m", KC.N: "n", KC.O: "o", KC.P: "p", KC.Q: "q", KC.R: "r",
    KC.S: "s", KC.T: "t", KC.U: "u", KC.V: "v", KC.W: "w", KC.X: "x",
    KC.Y: "y", KC.Z: "z", KC.SPACE: " ", KC.N0: "0", KC.N1: "1",
    KC.N2: "2", KC.N3: "3", KC.N4: "4", KC.N5: "5", KC.N6: "6",
    KC.N7: "7", KC.N8: "8", KC.N9: "9",
}



for button in buttons.values():
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP


class CommandReceiver(Extension):
    def during_bootup(self, keyboard):
        # Guarantee state variables exist on KMK boot
        self.keyboard = keyboard
        self.last_state = {name: True for name in buttons}
        self.input_buffer = ""
        self.modal_active = False
        self.handled_keys = set()

        ui.show("main")

    def after_matrix_scan(self, sandbox): pass
    def after_hid_send(self, sandbox): pass
    def on_powersave_enable(self, sandbox): pass
    def on_powersave_disable(self, sandbox): pass

    def before_matrix_scan(self, sandbox):
        microcontroller.watchdog.feed()

        # Serial Command Listener
        if supervisor.runtime.serial_bytes_available:
            char = sys.stdin.read(1)
            sys.stdout.write(char)
            if char in ('\r', '\n'):
                self.process_command(self.input_buffer.strip().lower())
                self.input_buffer = ""
            else:
                self.input_buffer += char

        # Side Button Checks
        if hasattr(self, 'last_state'):
            for name, pin in buttons.items():
                current_btn = pin.value
                if not current_btn and self.last_state[name]: 
                    print(f'\nBUTTON: {name} pressed!')
                self.last_state[name] = current_btn

    def before_hid_send(self, sandbox):
        if not getattr(self, 'keyboard', None) or not hasattr(self.keyboard, 'keys_pressed'):
            return

        if not hasattr(self, 'handled_keys'):
            self.handled_keys = set()

        # --- BIND TOOL PHASE 1: Wait for Physical Key Press ---
        if bind_tool.bind_tool.state == STATE_WAIT_KEY:
            # Matrix event lives inside sandbox, not keyboard
            event = getattr(sandbox, 'matrix_update', None)
            if event and getattr(event, 'pressed', False):
                bind_tool.bind_tool.on_key_detected(event.key_number)

            self.keyboard.keys_pressed.clear()
            return

        pressed_keys = list(self.keyboard.keys_pressed)
        if not pressed_keys:
            self.handled_keys.clear()
            return

        # 1. Trigger Check: LGUI + SPACE (Only when modal/bind is inactive)
        if not getattr(self, 'modal_active', False) and bind_tool.bind_tool.state == bind_tool.STATE_IDLE:
            has_gui = any(k in (KC.LGUI, KC.RGUI) for k in pressed_keys)
            has_space = any(k == KC.SPACE for k in pressed_keys)

            if has_gui and has_space:
                if KC.SPACE.code not in self.handled_keys:
                    self.toggle_modal()
                    self.handled_keys.add(KC.SPACE.code)
                self.keyboard.keys_pressed.clear()
                return

        # 2. Intercept Typing (Normal Modal OR Bind Tool Phase 2)
        is_bind_typing = (bind_tool.bind_tool.state == STATE_WAIT_CODE)
        if getattr(self, 'modal_active', False) or is_bind_typing:
            for key in pressed_keys:
                code = getattr(key, 'code', None)
                if not code or code in self.handled_keys:
                    continue

                self.handled_keys.add(code)

                if key in KEY_MAP:
                    self.input_buffer += KEY_MAP[key]
                    if is_bind_typing:
                        ui.manager.update_cmd_text(f"K#{bind_tool.bind_tool.target_key_num} -> {self.input_buffer}")
                    else:
                        ui.manager.update_cmd_text(self.input_buffer)

                elif key == KC.BSPC:
                    self.input_buffer = self.input_buffer[:-1]
                    if is_bind_typing:
                        ui.manager.update_cmd_text(f"K#{bind_tool.bind_tool.target_key_num} -> {self.input_buffer}")
                    else:
                        ui.manager.update_cmd_text(self.input_buffer)

                elif key == KC.ENTER:
                    typed_val = self.input_buffer.strip()
                    self.input_buffer = ""
                    
                    if is_bind_typing:
                        bind_tool.bind_tool.apply_bind(self.keyboard, typed_val)
                    else:
                        self.toggle_modal()
                        self.process_command(typed_val)

                elif key == KC.ESC:
                    if is_bind_typing:
                        bind_tool.bind_tool.cancel()
                    else:
                        self.toggle_modal()

            self.keyboard.keys_pressed.clear()
    def toggle_modal(self):
        print("Toggling Modal")
        self.modal_active = not getattr(self, 'modal_active', False)
        self.input_buffer = ""
        print("cleared, Showing overlay")
        # Ensure main screen is loaded if oled.root_group is empty
        if ui.oled.root_group is None:
            ui.show("main")

        if self.modal_active:
            ui.manager.show_cmd_modal()
            ui.manager.update_cmd_text("")
            print("[UI Modal]: OPEN")
        else:
            ui.manager.hide_cmd_modal()
            print("[UI Modal]: CLOSED") 
    def process_command(self, cmd):
      print(f"\n[Command Executed]: '{cmd}'")
      key = cmd.strip().split()
      
    def process_command(self, cmd):
      print(f"\n[Command Executed]: '{cmd}'")
      key = cmd.strip().split()

      if not key:
          return

      action = key[0]
      args = key[1:]

      if action == "modal":
          print("Entering Modal Mode")
          self.toggle_modal()

      elif action == "ping":
          print("Pong!")

      elif action == "menu":
          ui.show(args[0] if args else None)

      elif action in ("exit", "quit", "rb"):
          if args and args[0] == "h":
              print("[HARD RESET]")
              microcontroller.reset()
          else:
              print("Scheduling system reset")
              supervisor.reload()
      elif action == "layout":
            target_layout = args[0] if args else "base"
            if layout_manager.apply_layout(self.keyboard, target_layout):
                print(f"[Layout Loaded]: {target_layout}")
            else:
                print(f"[Layout Error]: Layout '{target_layout}' not found")
      
      elif action == "bind":
          bind_tool.bind_tool.start()
      elif action == "save":
            layout_name = args[0] if args else "custom"
            layout_exporter.save_layout(self.keyboard, layout_name)
      elif action == "mount":
            mode = args[0].lower() if args else "status"

            if mode in ("w", "rw", "write"):
                microcontroller.nvm[0] = 1
                print("[Mount]: Code write-access enabled. Rebooting...")
                microcontroller.reset()

            elif mode in ("r", "ro", "read"):
                microcontroller.nvm[0] = 0
                print("[Mount]: USB write-access enabled. Rebooting...")
                microcontroller.reset()

            else:
                status = "WRITE (Code-Write)" if microcontroller.nvm[0] == 1 else "READ (USB-Write)"
                print(f"[Mount Status]: Currently set to {status}")

      else:
          print(f"Unknown command: {action}")
