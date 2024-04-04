import RIS_usb
import time
RIS_usb.reset_RIS()
pattern = "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
RIS_usb.set_pattern(pattern)
RIS_usb.read_pattern()
