from machine import UART, Pin
import time
import var

uart = UART(1, baudrate=9600, tx=Pin(27), rx=Pin(26))

RST = Pin(14, Pin.OUT, Pin.PULL_UP)
CFG = Pin(23, Pin.OUT, Pin.PULL_UP)

MODE = 3  #0:TCP Server 1:TCP Client 2:UDP Server 3:UDP Client
GATEWAY = (192, 168, 0, 1)   # GATEWAY
TARGET_IP = (192, 168, 0, 10)# TARGET_IP
LOCAL_IP = (192, 168, 0, 20)    # LOCAL_IP
SUBNET_MASK = (255,255,255,0) # SUBNET_MASK
LOCAL_PORT1 = 5005             # LOCAL_PORT
TARGET_PORT = 5005            # TARGET_PORT
BAUD_RATE = 9600            # BAUD_RATE


# Adresse IP et port du Raspberry Pi
RASPBERRY_IP = "192.168.0.10"  # Remplace par l'IP de ton Raspberry Pi
RASPBERRY_PORT = 5005         # Port UDP sur lequel le Raspberry écoute
SEND_INTERVAL = 20             # Intervalle en secondes pour envoyer les scores

def construire_score():
    """
    Construit la chaîne de caractères contenant les scores des deux joueurs.
    Le format du message est : "joueur1_set1|joueur1_set2|joueur1_set3|joueur2_set1|joueur2_set2|joueur2_set3"
    """
    s = ""
    for x in range(2):  # On a 2 joueurs
        for y in range(3):  # Trois sets par joueur
            s += str(var.score[x][y]) + "|"
    return s[:-1]  # On retire le dernier caractère '|' pour avoir un format propre

def answer(question):
    try:
        testUart = uart.read()   
        if b'\xaa' in testUart:        
            print(question + " : OK")
        else:
            print(question + " : Error")
    except:
        print("Pas de réponse !")

def start_udp_sender():
    """
    Fonction qui envoie régulièrement les scores via UART,
    le CH9121 se charge ensuite d’envoyer en UDP vers l’IP cible.
    """
    print("📡 Démarrage de l'envoi UART (via CH9121 UDP)...")
    while True:
        try:
            message = construire_score()
            uart.write(message.encode())  # Envoi vers le CH9121
            print("📤 Score envoyé via UART (CH9121):", message)
        except Exception as e:
            print("❌ Erreur UART:", e)

        time.sleep(SEND_INTERVAL)

def init_configuration():
    RST.value(1)
    CFG.value(1)
    print("Uart vide : ",uart.txdone())
    uart.write("Toto")
    print(uart.read())
    print("begin configuration")
    time.sleep(2)
    CFG.value(0)
    time.sleep(0.5)

    uart.write(b'\x57\xab\x10'+MODE.to_bytes(1, 'little')) #Mode UDP Client
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
    time.sleep(1)
    answer("Mode configuration Exit")
    time.sleep(0.5)
    CFG.value(1)
    time.sleep(1)
    print("end configuration")