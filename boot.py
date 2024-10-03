import ugit
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ugit.pull_all()
