from machine import Pin, ADC, Timer
#from communication import *
import time
import network
import espnow

# Hardware definition
# Pins config
BP_PARAMETER = Pin(32, Pin.IN, Pin.PULL_UP)
BP_VALID = Pin(33, Pin.IN, Pin.PULL_UP)
BP_J1_UP = Pin(15, Pin.IN, Pin.PULL_DOWN)
BP_J2_UP = Pin(16, Pin.IN, Pin.PULL_DOWN)
BP_J1_DOWN = Pin(17, Pin.IN, Pin.PULL_DOWN)
BP_J2_DOWN = Pin(18, Pin.IN, Pin.PULL_DOWN)
BP_RESET_SCORE = Pin(19, Pin.IN, Pin.PULL_DOWN)
VIN_TEST = Pin(13, Pin.IN, Pin.PULL_UP)

# Adresses MAC des périphériques du système
adrMac = [
    b'\xb4\x8a\n\x8a/\x9c',      # Adresse MAC de ESP32 N°1
    b'\xb4\x8a\n\x8a.\xcc',      # Adresse MAC de ESP32 N°2
    b'\xb4\x8a\n\x8a.\xc8',      # Adresse MAC de ESP32 N°3
    b'\xb4\x8a\n\x8a/\x14',      # Adresse MAC de ESP32 N°4
    b'\xb4\x8a\n\x8a0\x10',      # Adresse MAC de ESP32 N°5
    b'\xb4\x8a\n\x8a/\xcc'       # Adresse MAC de ESP32 N°
]

# Variables
color = [0,0]
oldColor = [0,0]
lux = 6
oldLux = 0
score = [[0, 0, 0],[0, 0, 0]]
oldScore = [[0, 0, 0],[0, 0, 0]]
setNum = 0
oldSetNum = 0
setWin = [[0, 0, 0],[0, 0, 0]]
oldBpJ1Up = 0
oldBpJ2Up = 0
oldBpJ1Down = 0
oldBpJ2Down = 0
parameters = True
oldParameters = False
valid = False
reset = False
bp=0
start=0

couleurs = ["red","green","blue","purple","yellow","orange","pink","cyan"]

