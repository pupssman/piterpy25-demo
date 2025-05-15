import network
import urequests
import machine
import time
from machine import Pin

LED_PIN = 2  # Built-in LED typically on GPIO2

# Initialize LED early for error reporting
led = Pin(LED_PIN, Pin.OUT)

# Configuration
def load_config():
    try:
        with open('env.txt') as f:
            return dict(line.strip().split('=') for line in f)
    except:
        print("Critical error: Missing env.txt configuration file")
        # Flash LED 5 times slowly (1 second on/off)
        for _ in range(5):
            led.on()
            time.sleep(1)
            led.off()
            time.sleep(1)
        # Hang the system
        while True:
            time.sleep(1)

config = load_config()
API_URL = f"http://{config['API_HOST']}/flashes"
previous_flashes = 0

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(config['WIFI_SSID'], config['WIFI_PASSWORD'])
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
