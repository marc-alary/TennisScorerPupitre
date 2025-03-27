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
#VIN_TEST = Pin(13, Pin.IN, Pin.PULL_UP)

# Adresses MAC des périphériques du système
adrMac = [
    b'\xb4\x8a\n\x8a/\x14',      # J1 SET1
    b'\xb4\x8a\n\x8a.\xcc',      # J1 SET2
    b'\xb4\x8a\n\x8a/\x9c',      # J1 SET3
    b'\xb4\x8a\n\x8a.\xc8',      # J2 SET1
    b'\xb4\x8a\n\x8a/\xcc',      # J2 SET2
    b'\xb4\x8a\n\x8a0\x10'       # J2 SET3
]

# Variables score du match
score = [[0, 0, 0],[0, 0, 0]]
oldScore = [[0, 0, 0],[0, 0, 0]]
setNum = 0
oldSetNum = 0
setWin = [[0, 0, 0],[0, 0, 0]]

# Variables paramètres afficheurs
color = [0,0]
oldColor = [0,0]
userLum = 1
oldUserLum = 0

# Variables boutons poussoirs
parameter = False
oldParameter = False
valid = False
reset = False
bp = True
j1Up = False
j1Dn = False
j2Up = False
j2Dn = False

# Variables état système
etatSystem="SET 1"
oldEtatSystem="RIEN"
check=False

couleurs = ["red","green","blue","purple","yellow","orange","pink","cyan"]