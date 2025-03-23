from machine import Pin, I2C
import time
import ssd1306

i2c = I2C(0, scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def write_ligne(txt,row):
    # 16 caractères et 8 lignes de 0 à 7
    y = (row-1) * 8
    oled.text(txt, 0, y, 1)
    oled.show()

def clear_ligne(row):
    # 16 caractères et 8 lignes de 0 à 7
    ymin = (row-1)*8
    ymax = ymin + 7
    for y in range(ymin, ymax):
        for x in range(0,127):
            oled.pixel(x,y,0)
        oled.show()
    
def clear_screen():
    oled.fill(0)
    oled.show()

def oled_system_state(state):
    clear_ligne(7)
    clear_ligne(8)
    write_ligne(state,7)

def bonjour():
    oled.text('*Tennis Scorer**', 0, 0, 1)
    oled.text(' Version ', 0, 56, 1)
    oled.show()
    time.sleep(5)
    #oled.text('Hello', 0, 0, 0) #efface hello      
    #oled.show()
    #time.sleep(5)
    #oled.fill(0)
    oled.show()
