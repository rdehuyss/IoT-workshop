import utime
from machine import Pin


def blink():
    led = Pin(5, Pin.OUT)
    enabled = False
    while True:
        if enabled:
            led.value(1)
        else:
            led.value(0)
        utime.sleep_ms(1000)
        enabled = not enabled
