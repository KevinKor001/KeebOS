import Display
import BootLogo
options = ["START", "SETTINGS", "CREDITS"]
selected = 0


def refresh_menu():
    print("Meunu Begin!")
    Display.pixel_bitmap.fill(0)
    Display.drawStr(5, 10, "--- MAIN MENU ---")

    for i, option in enumerate(options):
        y_pos = 25 + (i * 12)
        if i == selected:
            # Draw a selection box (XOR) over the text
            Display.drawBox(2, y_pos - 8, 100, 11, layer=1)
            Display.drawStr(5, y_pos, option, xor=1)
        else:
            Display.drawStr(5, y_pos, option)
    


#BootLogo.init()

# Initial draw    
#refresh_menu()




