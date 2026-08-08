import displayio
import terminalio
from adafruit_display_text import label

MAX_LINES = 5
MAX_CHARS = 21

line_buffer = ["--- SERIAL CONSOLE ---"]
partial_line = ""
tty_label = None

def get_group():
    global tty_label
    group = displayio.Group()

    tty_label = label.Label(
        terminalio.FONT,
        text="\n".join(line_buffer),
        color=0xFFFFFF,
        x=0,
        y=5,
        line_spacing=0.85
    )
    group.append(tty_label)
    return group

def write_stream(buf):
    """Processes raw stdout text from print() calls."""
    global line_buffer, partial_line, tty_label

    for char in str(buf):
        if char == '\n':
            _push_line(partial_line)
            partial_line = ""
        elif char == '\r':
            pass
        else:
            partial_line += char
            if len(partial_line) >= MAX_CHARS:
                _push_line(partial_line)
                partial_line = ""

    # Refresh label if active on screen
    if tty_label:
        render_text = line_buffer.copy()
        if partial_line:
            render_text.append(partial_line)
            render_text = render_text[-MAX_LINES:]
        tty_label.text = "\n".join(render_text)

def _push_line(line):
    global line_buffer
    line_buffer.append(line)
    line_buffer = line_buffer[-MAX_LINES:]
