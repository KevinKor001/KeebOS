import storage
import microcontroller

# NVM byte 0 check:
# 1 = Code has Write access (USB is Read-Only)
# 0 = USB has Write access (Code is Read-Only)
code_write_enabled = (microcontroller.nvm[0] == 1)

# storage.remount requires readonly=False for code write access
storage.remount("/", readonly=not code_write_enabled)
