from machine import UART, Pin
import time

EOL = '\r\n'

def web_page():
    date = "Thu, 21 May 2024 11:07:32 GMT"
    server = "ESP32"
    connection = "close"
    transfer_encoding = "chunked"
    content_type = "text/html; charset=ISO-8859-1"

    entete_http = (
        'HTTP/1.1 200 OK' + EOL +
        'Date: ' + date + EOL +
        'Server: ' + server + EOL +
        'Connection: ' + connection + EOL +
        'Transfer-Encoding: ' + transfer_encoding + EOL +
        'Content-Type: ' + content_type + EOL + EOL
    )

    page_web = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ca marche !</title>
    </head>
    <body>
        <h1>Ca marche</h1>
        <p>coucou</p>
    </body>
    </html>"""

    return entete_http + page_web

# UART and Ethernet configuration
uart2 = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))

CFG = Pin(4, Pin.OUT, Pin.PULL_UP)
RST = Pin(2, Pin.OUT)
RST.value(1)
time.sleep(1)
RST.value(0)
time.sleep(1)
RST.value(1)

MODE = 0  # 0: TCP Server 1: TCP Client 2: UDP Server 3: UDP Client
GATEWAY = (192, 168, 0, 1)  # GATEWAY
TARGET_IP = (192, 168, 0, 1)  # TARGET_IP
LOCAL_IP = (192, 168, 0, 20)  # LOCAL_IP
SUBNET_MASK = (255, 255, 255, 0)  # SUBNET_MASK
LOCAL_PORT1 = 5000  # LOCAL_PORT
TARGET_PORT = 80  # TARGET_PORT
BAUD_RATE = 9600  # BAUD_RATE

def configure_ethernet():
    print("begin configuration")
    CFG.value(0)
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x10' + MODE.to_bytes(1, 'little'))
    time.sleep(0.5)
    print("mode: " + str(uart2.read()))
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x11' + bytes(bytearray(LOCAL_IP)))  # ip locale
    time.sleep(0.5)
    print("ip locale: " + str(uart2.read()))
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x12' + bytes(bytearray(SUBNET_MASK)))  # masque ss reseau
    time.sleep(0.5)
    print("masque sous reseau: " + str(uart2.read()))
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x13' + bytes(bytearray(GATEWAY)))  # @ gateway
    time.sleep(0.5)
    print("Gateway: " + str(uart2.read()))
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x14' + LOCAL_PORT1.to_bytes(2, 'little'))  # num port1 local
    time.sleep(0.5)
    print("local port: " + str(uart2.read()))
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x15' + bytes(bytearray(TARGET_IP)))  # ip distante
    time.sleep(0.5)
    print("ip destinataire: " + str(uart2.read()))
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x16' + TARGET_PORT.to_bytes(2, 'little'))  # num port distant
    time.sleep(0.5)
    print("num port distant: " + str(uart2.read()))
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x21' + BAUD_RATE.to_bytes(4, 'little'))  # baud serial
    time.sleep(0.5)
    print("baud rate: " + str(uart2.read()))
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x0D')  # save in eeprom
    time.sleep(0.5)
    print(uart2.read())
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x0E')  # execute conf and reset
    time.sleep(0.5)
    print(uart2.read())
    time.sleep(0.5)
    uart2.write(b'\x57\xab\x5E')  # leave serial port configuration mode
    time.sleep(0.5)
    print(uart2.read())
    time.sleep(0.5)
    CFG.value(1)
    time.sleep(0.5)
    print("end configuration")
    uart2.write(b'\x57\xAB\x61')  # get ip locale
    time.sleep(0.5)
    print("IP locale :")
    print(uart2.read())
    time.sleep(0.5)
    uart2.write(b'\x57\xAB\x81')  # get mac address
    time.sleep(0.5)
    print("@ MAC locale :")
    print(uart2.read())
    time.sleep(0.5)

def serve_http():
    while True:
        """
        if uart2.any():
            request = uart2.read()
            print("Request received:", request)
            response = web_page()
            uart2.write(response.encode())
            print("Response sent")
            """
        uart2.write("ABC")
        time.sleep(1)

configure_ethernet()
serve_http()