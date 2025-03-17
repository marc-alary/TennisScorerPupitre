# initialisation functions

from machine import UART, Pin
import time

uart = UART(1, baudrate=9600, tx=Pin(27), rx=Pin(26))

RST = Pin(14, Pin.OUT, Pin.PULL_UP)
CFG = Pin(23, Pin.OUT, Pin.PULL_UP)
#RUN = Pin(25, Pin.IN)
RST.value(1)
CFG.value(1)
print("Uart vide : ",uart.txdone())
uart.write("Toto")
print(uart.read())
print("begin configuration")
time.sleep(2)
CFG.value(0)
time.sleep(0.5)

MODE = 0  #0:TCP Server 1:TCP Client 2:UDP Server 3:UDP Client
GATEWAY = (192, 168, 0, 10)   # GATEWAY
TARGET_IP = (192, 168, 0, 10)# TARGET_IP
LOCAL_IP = (192, 168, 0, 20)    # LOCAL_IP
SUBNET_MASK = (255,255,255,0) # SUBNET_MASK
LOCAL_PORT1 = 5000             # LOCAL_PORT
TARGET_PORT = 80            # TARGET_PORT
BAUD_RATE = 9600            # BAUD_RATE

def answer(question):
    try:
        testUart = uart.read()   
        if b'\xaa' in testUart:        
            print(question + " : OK")
        else:
            print(question + " : Error")
    except:
        print("Pas de réponse !")

uart.write(b'\x57\xab\x10'+MODE.to_bytes(1, 'little')) #Le mode
time.sleep(0.5)
answer("Mode configuration")
time.sleep(0.5)
uart.write(b'\x57\xab\x11'+bytes(bytearray(LOCAL_IP))) # ip locale
time.sleep(0.5)
print(uart.read())
answer("IP Locale")
time.sleep(0.5)
uart.write(b'\x57\xab\x12'+bytes(bytearray(SUBNET_MASK))) # masque ss reseau
time.sleep(0.5)
answer("Masque de sous réseau")
time.sleep(0.5)
uart.write(b'\x57\xab\x13'+bytes(bytearray(GATEWAY))) #@ gateway
time.sleep(0.5)
answer("Gateway")
time.sleep(0.5)
uart.write(b'\x57\xab\x14'+LOCAL_PORT1.to_bytes(2, 'little')) #num port1 local
time.sleep(0.5)
answer("Local port")
time.sleep(0.5)
uart.write(b'\x57\xab\x15'+bytes(bytearray(TARGET_IP))) # ip distante
time.sleep(0.5)
answer("IP destinataire")
time.sleep(0.5)
uart.write(b'\x57\xab\x16'+TARGET_PORT.to_bytes(2, 'little')) # num port distant
time.sleep(0.5)
answer("Num port distant")
time.sleep(0.5)
uart.write(b'\x57\xab\x21'+BAUD_RATE.to_bytes(4, 'little')) # baud serial
time.sleep(0.5)
answer("Baud rate")
time.sleep(0.5)
uart.write(b'\x57\xab\x0D') # save in eeprom
time.sleep(2)
answer("Sauvegarde en EEprom")
time.sleep(0.5)
uart.write(b'\x57\xab\x0E') # execute conf and reset
time.sleep(2)
answer("Execute Config et Reset")
time.sleep(0.5)
uart.write(b'\x57\xab\x5E') #leave serial port configuration mode
time.sleep(2)
answer("Mode configuration Exit")
time.sleep(0.5)
CFG.value(1)
time.sleep(2)
print("end configuration")
# ## FIXME
# 
#RST.value(0)
#time.sleep(2)
#RST.value(1)
#time.sleep(2)