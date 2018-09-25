import dht
import machine


# Blue sensor
class DHT11Sensor:

    def __init__(self, pin):
        self.sensor = dht.DHT11(machine.Pin(pin))

    def doMeasurement(self):
        self.sensor.measure()
        print('DHT11 Measurement')
        print('\tTemperature:', str(self.sensor.temperature()))
        print('\tHumidity:', str(self.sensor.humidity()))
