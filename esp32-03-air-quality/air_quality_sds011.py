from sds011 import SDS011
import ujson
import time
from mqttpublisher import MQTTPublisher


class AirQuality:

    def __init__(self):
        self.sensor = SDS011()
        self.mqttPublisher = MQTTPublisher(self.config_data)
        self.mqttPublisher.connect()

    def doMeasurement(self):

        while True:
            self.sensor.wake()
            airQualityStats = self.sensor.read(20)
            self.sensor.sleep()
            print(airQualityStats)
            self.mqttPublisher.publish(self.airQualityStats)
            time.sleep(120)

