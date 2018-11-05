import bme680
import machine
import ujson
import time
from i2c import I2CAdapter
from mqttpublisher import MQTTPublisher


class AirQuality:

    def __init__(self):
        f = open('config.json')
        self.config_data = ujson.load(f)
        f.close()

        self.i2c_dev = I2CAdapter(-1, scl=machine.Pin(5), sda=machine.Pin(4))
        self.sensor = bme680.BME680(i2c_device=self.i2c_dev)
        self.mqttPublisher = MQTTPublisher(self.config_data)
        self.mqttPublisher.connect()
        self.airQualityStats = AirQualityStats()

        # These oversampling settings can be tweaked to
        # change the balance between accuracy and noise in
        # the data.
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)

    def measure(self):
        # start_time and curr_time ensure that the
        # burn_in_time (in seconds) is kept track of.

        start_time = time.time()
        curr_time = time.time()
        burn_in_time = 240

        burn_in_data = []

        # Collect gas resistance burn-in values, then use the average
        # of the last 50 values to set the upper limit for calculating
        # gas_baseline.
        print('Collecting gas resistance burn-in data for 4 mins\n')
        while curr_time - start_time < burn_in_time:
            curr_time = time.time()
            if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
                gas = self.sensor.data.gas_resistance
                burn_in_data.append(gas)
                print('Gas [{0}]: {1} Ohms'.format(len(burn_in_data), gas))
                time.sleep(1)

        gas_baseline = sum(burn_in_data[-50:]) / 50.0

        # Set the humidity baseline to 40%, an optimal indoor humidity.
        hum_baseline = 40.0

        # This sets the balance between humidity and gas reading in the
        # calculation of air_quality_score (25:75, humidity:gas)
        hum_weighting = 0.25

        print('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(
            gas_baseline,
            hum_baseline))

        while True:
            if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
                temp = self.sensor.data.temperature
                pressure = self.sensor.data.pressure
                gas = self.sensor.data.gas_resistance
                gas_offset = gas_baseline - gas

                hum = self.sensor.data.humidity
                hum_offset = hum - hum_baseline

                # Calculate hum_score as the distance from the hum_baseline.
                if hum_offset > 0:
                    hum_score = (100 - hum_baseline - hum_offset)
                    hum_score /= (100 - hum_baseline)
                    hum_score *= (hum_weighting * 100)

                else:
                    hum_score = (hum_baseline + hum_offset)
                    hum_score /= hum_baseline
                    hum_score *= (hum_weighting * 100)

                # Calculate gas_score as the distance from the gas_baseline.
                if gas_offset > 0:
                    gas_score = (gas / gas_baseline)
                    gas_score *= (100 - (hum_weighting * 100))

                else:
                    gas_score = 100 - (hum_weighting * 100)

                # Calculate air_quality_score.
                air_quality_score = hum_score + gas_score

                self.airQualityStats.update(temp, pressure, hum, air_quality_score, gas)
                print(self.airQualityStats)
                self.mqttPublisher.publish(self.airQualityStats)

                time.sleep(2)


class AirQualityStats:

    def __init__(self):
        self.temperature = -1
        self.pressure = -1
        self.humidity = -1
        self.air_quality_score = -1
        self.gas = -1

    def update(self, temperature, pressure, humidity, air_quality_score, gas):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.air_quality_score = air_quality_score
        self.gas = gas

    def __str__(self):
        return '{0} C, {1} hPa, {2:.2f} %RH, {3:.2f} IAQ, {4:.2f} Ohms'.format(
            self.temperature,
            self.pressure,
            self.humidity,
            self.air_quality_score,
            self.gas)
