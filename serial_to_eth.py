from machine import UART, Pin
import time
import var
import _thread
import uasyncio

uart = UART(1, baudrate=9600, tx=Pin(27), rx=Pin(26))

RST = Pin(14, Pin.OUT, Pin.PULL_UP)
CFG = Pin(23, Pin.OUT, Pin.PULL_UP)

MODE = 0  #0:TCP Server 1:TCP Client 2:UDP Server 3:UDP Client
GATEWAY = (192, 168, 0, 10)   # GATEWAY
TARGET_IP = (192, 168, 0, 10)# TARGET_IP
LOCAL_IP = (192, 168, 0, 20)    # LOCAL_IP
SUBNET_MASK = (255,255,255,0) # SUBNET_MASK
LOCAL_PORT1 = 5000             # LOCAL_PORT
TARGET_PORT = 80            # TARGET_PORT
BAUD_RATE = 9600            # BAUD_RATE

# INIT WORKING VARIABLE
data =  b'\0'
transmitInProgress = False
headerFound = False
printData = True
lenWrite = 0

EOL = '\r\n'
#The header and the body of a HTTP request/response are supposed to be separated by \r\n\r\n (section 4.1 of RFC 2616)
HEADER_BODY_SEPARATOR = EOL+EOL

def build_response():
    print("Score actualisé : ", var.score)
    #date = "Thu, 21 may 2024 11:07:32 GMT" 
    #server = "ESP32"
    #connection = "close"
    #Transfer_Encoding = "chunked"
    content_Type = "text/html; charset=ISO-8859-1"
    page_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tableau des scores</title>
            <style>
            body {
                background-image: rgb(255, 255, 255)
            }
            table {
                border-collapse: collapse;
                width: 90%;
                font-size:160px;
            }
            th, tr, td {
                border: rgb(24, 24, 24) 5px solid;
                height:110px;
            }
            .center {
                margin-left:auto;
                margin-right:auto;
                margin-top:200px;
            }
            .tblue {
                background-color:rgb(10, 140, 180);
                font-family:arial;
                text-align:center;
                color:rgb(10, 40, 180);
            }
            .tred {
                background-color:rgb(220, 40, 10);
                font-family:arial;
                text-align:center;
                color:rgb(97, 0, 0);
            }
            .titletext {
                text-align:center;
                font-size: 110px;
                font-family:arial;
                background:rgb(0, 0, 0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .wpt {
                width: 40%
            }
            </style>
        </head>
        <body>
            <h1 class="titletext">Tableau des scores</h1>
            
            <div id="tablerefresh">
            <table id="refr" class="center">
                <tr>
                    <td class="tred wpt">Visiteur</td>
                    <td class="tred">""" + str(var.score[0][0]) + """</td>
                    <td class="tred">""" + str(var.score[0][1]) + """</td>
                    <td class="tred">""" + str(var.score[0][2]) + """</td>
                </tr>
                <tr>
                    <td class="tblue wpt">Club</td>
                    <td class="tblue">""" + str(var.score[1][0]) + """</td>
                    <td class="tblue">""" + str(var.score[1][1]) + """</td>
                    <td class="tblue">""" + str(var.score[1][2]) + """</td>
                </tr>
            </table>
            </div>
            <script src="/jquery-3.7.1.min.js"></script>
            <script>
                $(document).ready(function() {
                    // Rafraîchissement toutes les 1000 ms (1 seconde)
                    setInterval(function() {
                        $("#tablerefresh").load(location.href + " #refr");
                    }, 5000);
                });
            </script>
        </body>
        </html>"""
    
    #simple_html = "<!DOCTYPE html><html lang=\"en\"><body><h1>Ca marche</h1><p>coucou</p></body></html>"
    length_web = len(page_html)
    #print(length_web)
    
    #entete_http = 'HTTP/1.1 200 OK '+EOL+'Date:' +date+EOL+'Server: '+server+EOL+'Connection: '+connection+EOL+'Content-Length:'+str(length_web)+EOL+'Transfer-Encoding: '+Transfer_Encoding+EOL+'content-Type: '+content_Type+EOL
    #entete_http = 'HTTP/1.1 200 OK '+Econtent_TypeOL+'Date:' +date+EOL+'Server: '+server+EOL+'Connection: '+connection+EOL+'Transfer-Encoding: '+Transfer_Encoding+EOL+'content-Type: '+content_Type+EOL
    simple_entete_http = 'HTTP/1.1 200 OK '+EOL+'Content-Length:'+str(length_web)+EOL+'content-Type: '+content_Type

    #buff = simple_entete_http+HEADER_BODY_SEPARATOR+simple_html
    buff = simple_entete_http+HEADER_BODY_SEPARATOR+page_html
    length_buff = len(buff)
    return buff, length_buff    
    
#The header and the body are supposed to be separated by \r\n\r\n (section 4.1 of RFC 2616)
def checkHeaderComplete(data) :
    if (data.find(HEADER_BODY_SEPARATOR.encode()) > 0) :
        return True
    else :
        return False

def serv_web():
    global data
    global headerFound
    global printData
    global transmitInProgress
    global lenWrite

    while headerFound == False:
        if uart.any() > 0 :
            data = data+uart.read()
            headerFound = checkHeaderComplete(data)

    if headerFound and printData:
        len_data = len(data)
        print(f'len datat {len_data} \n data {data}')
        printData = False
    
    if headerFound :
        buf, lenBuf = build_response()
        #print(f'lenBuf {lenBuf}')
        transmitInProgress = True
        while transmitInProgress == True :
            lenWrite += uart.write(buf)
            #print(f'lenWrite {lenWrite}')
            buf = buf[lenWrite:]
            if (lenWrite >= lenBuf) :
                headerFound = False
                printData = True
                transmitInProgress = False
                lenWrite = 0
                data = b'\0' 

    #return "BONJOUR<br/>", 12

def answer(question):
    try:
        testUart = uart.read()   
        if b'\xaa' in testUart:        
            print(question + " : OK")
        else:
            print(question + " : Error")
    except:
        print("Pas de réponse !")

def preparing_to_send_serv_web():
    if var.check is True:
        while True :
            time.sleep(0.1)
            if uart.any() > 0 :
                serv_web()
                print('send')
         
def start_http_server():
    _thread.start_new_thread(preparing_to_send_serv_web, ())
    
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