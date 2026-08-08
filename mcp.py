import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
from kmk.scanners import Scanner

class MCP23017Matrix(Scanner):
    def __init__(self, i2c, address, cols, rows, diode_orientation):
        self.mcp = MCP23017(i2c, address=address)

        self.cols = [self.mcp.get_pin(c) for c in cols]
        self.rows = [self.mcp.get_pin(r) for r in rows]

        # Set columns as outputs (idle HIGH)
        for c in self.cols:
            c.switch_to_output(value=True)

        # Rows as inputs with pull-ups
        for r in self.rows:
            r.switch_to_input(pull=digitalio.Pull.UP)

        # Save total number of keys
        self.keyscan_count = len(self.cols) * len(self.rows)

        # Internal previous state
        self.prev = [0] * self.keyscan_count

        self.diode_orientation = diode_orientation

    def scan_for_changes(self):
        events = []
        idx = 0

        for ci, c in enumerate(self.cols):
            # Activate one column at a time
            c.value = False  # drive LOW

            for ri, r in enumerate(self.rows):
                pressed = (not r.value)

                if pressed != self.prev[idx]:
                    # KMK expects: (pressed_bool, key_number_int)
                    events.append((pressed, idx))
                    self.prev[idx] = pressed

                idx += 1

            c.value = True  # return HIGH

        return events or None
