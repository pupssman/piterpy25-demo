import network
import urequests
import machine
import time
from machine import Pin

# Configuration
WIFI_SSID = 'YOUR_WIFI_SSID'
WIFI_PASSWORD = 'YOUR_WIFI_PASSWORD'
API_URL = 'http://192.168.100.100:8080/flashes'
LED_PIN = 2  # Built-in LED typically on GPIO2

# Initialize LED
led = Pin(LED_PIN, Pin.OUT)
previous_flashes = 0

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            time.sleep(0.5)
    print('Network config:', sta_if.ifconfig())

def flash_led(times):
    for _ in range(times):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

def get_flash_count():
    try:
        response = urequests.get(API_URL)
        data = response.json()
        return data.get('num_flashes', 0)
    except:
        return None

def main():
    global previous_flashes
    connect_wifi()
    
    while True:
        current_flashes = get_flash_count()
        
        if current_flashes is not None:
            if previous_flashes > current_flashes:
                difference = previous_flashes - current_flashes
                print(f"Flashing {difference} times")
                flash_led(difference)
            
            previous_flashes = current_flashes
        
        time.sleep(30)  # Check every 30 seconds

if __name__ == '__main__':
    main()
