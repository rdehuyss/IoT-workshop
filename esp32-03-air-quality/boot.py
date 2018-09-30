import gc
import webrepl
import utime as time
import ujson

gc.collect()


print('\nBooting...')

def do_connect():
    import network

    f = open('config.json')
    config_data = ujson.load(f)
    f.close()

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config_data['wifi']['ssid'], config_data['wifi']['password'])
        while not sta_if.isconnected():
            pass
    print('connected at:', sta_if.ifconfig())


do_connect()
webrepl.start()
time.sleep(1)
print('Booted!')