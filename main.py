#https://io.adafruit.com/MauroDiaz/dashboards/project Diaz,Mauro Alexis
import machine, time, network
from hcsr04 import HCSR04
from umqtt.simple import MQTTClient
from machine import Pin, Timer, I2C, PWM
from lcd_i2c import LCD

ssid = 'Wokwi-GUEST'
wifipassword = ''

# ===========================
# VARIABLES
# ===========================

# Buzzer
buzzer = PWM(Pin(19), freq=440, duty_u16=32768)
buzzer.duty(0)
ALARMA_ON = 0

# Display 
I2C_ADDR = 0x27     
i2c = I2C(0, scl=Pin(5), sda=Pin(18), freq=800000)
lcd = LCD(addr=I2C_ADDR, cols=20, rows=4, i2c=i2c)

# Ultrasonido 
sensor = HCSR04(trigger_pin=12, echo_pin=14)

# Display
lcd.begin()
lcd.print("Distancia:")
lcd.set_cursor(col=0, row=1)
last_distance = None

#Funcion distancia
def publicar_distance(timer):
    global distance
    distance = round(sensor.distance_cm())
    conexionMQTT.publish(topic_2, str(distance))
    

#MQTT
mqtt_server = "io.adafruit.com"
port = 1883
user = '' #se coloca user de Adafruit 
password = '' #se coloca user key de Adafruit 
client_id = '' #nombre del feed de Adafruit 

#Donde dice user colocar el respectivo nombre
topic_1 = 'User/feeds/alarma'
topic_2 = 'User/feeds/Proximidad'


# ===========================
# FUNCIONES PREDETERMINADAS
# ===========================

# Definir modo Station para conectarse al AP remoto
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, wifipassword)

# Conectar a WiFi
print("Conectado WiFi...")
while not sta_if.isconnected():
    print (".", end="")
    time.sleep(0.1)
print("Conectado")
print(sta_if.ifconfig())

#Funcion Callback
def funcion_callback(topic, msg):
    global ALARMA_ON
    msg = msg.decode('utf-8')
    topic = topic.decode('utf-8')

    print("Mensaje de topico " + topic + ":" + msg)

    #Manejar los mensajes recibidos del broker MQTT
    if topic == topic_1:
        if "OFF" in msg:
            ALARMA_ON = 0
        elif "ON" in msg:
            ALARMA_ON = 1

# Conectar al broker MQTT
try:
    conexionMQTT = MQTTClient(client_id, mqtt_server, user=user, password=password, port=int(port))
    conexionMQTT.set_callback(funcion_callback)
    conexionMQTT.connect() # Conectar

    # Nos subscribimos a un topico luego del connect
    conexionMQTT.subscribe(topic_1) 
    print("Conectando al broker MQTT")

except OSError as e:
    print("Error al conectar con el Broker MQTT, procede a reiniciar...")
    time.sleep(5)
    machine.reset()


# ===========================
# MAIN
# ===========================

while True: 
    try:

        # Publicar la distancia al feed MQTT

        #inicializacion de condicion para luego usarlo
        distance1 = round(sensor.distance_cm())
        
        #Uso del display y actualizacion de adafruit en caso de algun cambio
        if distance1 != last_distance:
            publicar_distance(None)
            # Ajusta la posición para los números
            lcd.set_cursor(col=10, row=1)  
            # Limpiar solo el área de los números y "cm"
            lcd.print(" " * 6)  
            lcd.set_cursor(col=10, row=1)
            lcd.print(str(distance) + " cm")
            last_distance = distance1

        #actualizacion del chequeo de mensajes
        conexionMQTT.check_msg()
        time.sleep_ms(500) 

        #Condicion de alarma
        if ALARMA_ON and distance <= 50:
            buzzer.duty(50) 
        else:
            # Apaga el parlante PWM cuando la alarma no está activada
            buzzer.duty(0)  
        
    except OSError as e:
        print("Error de operacion:", e)
        time.sleep(5)
        machine.reset()
