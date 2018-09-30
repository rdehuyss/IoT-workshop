"""
Reading format. See http://cl.ly/ekot
0 Header   '\xaa'
1 Command  '\xc0'
2 DATA1    PM2.5 Low byte
3 DATA2    PM2.5 High byte
4 DATA3    PM10 Low byte
5 DATA4    PM10 High byte
6 DATA5    ID byte 1
7 DATA6    ID byte 2
8 Checksum Low byte of sum of DATA bytes
9 Tail     '\xab'
"""

import machine
import ustruct as struct
import sys
import utime as time


class SDS011:

    def __init__(self):
        self.airQualityStats = AirQualityStats()

    def init_uart(self):
        uart = machine.UART(1, 9600, tx=1, rx=3)
        uart.init(9600, bits=8, parity=None, stop=1)
        return uart

    CMDS = {'SET': b'\x01',
            'GET': b'\x00',
            'DUTYCYCLE': b'\x08',
            'SLEEPWAKE': b'\x06'}

    def make_command(self, cmd, mode, param):
        header = b'\xaa\xb4'
        padding = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'
        checksum = chr((ord(cmd) + ord(mode) + ord(param) + 255 + 255) % 256)
        tail = b'\xab'
        return header + cmd + mode + param + padding + bytes(checksum, 'utf8') + tail

    # sensor wakes for 60 secs before issuing measurement
    def set_dutycycle(self, rest_mins):
        uart = self.init_uart()
        cmd = self.make_command(self.CMDS['DUTYCYCLE'], self.CMDS['SET'], chr(rest_mins))
        print('Setting sds011 to read every', rest_mins, 'minutes:', cmd)
        uart.write(cmd)

    def wake(self):
        uart = self.init_uart()
        cmd = self.make_command(self.CMDS['SLEEPWAKE'], self.CMDS['SET'], chr(1))
        print('Sending wake command to sds011:', cmd)
        uart.write(cmd)

    def sleep(self):
        uart = self.init_uart()
        cmd = self.make_command(self.CMDS['SLEEPWAKE'], self.CMDS['SET'], chr(0))
        print('Sending sleep command to sds011:', cmd)
        uart.write(cmd)

    def process_reply(self, packet):
        print('Reply received:', packet)

    def process_measurement(self, packet):
        try:
            print('\nPacket:', packet)
            *data, checksum, tail = struct.unpack('<HHBBBs', packet)
            pm25 = data[0] / 10.0
            pm10 = data[1] / 10.0
            # device_id = str(data[2]) + str(data[3])
            checksum_OK = checksum == (sum(data) % 256)
            tail_OK = tail == b'\xab'
            packet_status = 'OK' if (checksum_OK and tail_OK) else 'NOK'
            print('PM 2.5:', pm25, '\nPM 10:', pm10, '\nStatus:', packet_status)
            self.airQualityStats.update(pm25, pm10, packet_status)
        except Exception as e:
            print('Problem decoding packet:', e)
            sys.print_exception(e)

    def read(self, allowed_time=0):
        uart = self.init_uart()
        start_time = time.ticks_ms()
        delta_time = 0
        while (delta_time <= allowed_time * 1000):
            try:
                header = uart.read(1)
                if header == b'\xaa':
                    command = uart.read(1)
                    if command == b'\xc0':
                        packet = uart.read(8)
                        self.process_measurement(packet)
                    elif command == b'\xc5':
                        packet = uart.read(8)
                        self.process_reply(packet)
                delta_time = time.ticks_diff(time.ticks_ms(), start_time) if allowed_time else 0
            except Exception as e:
                print('Problem attempting to read:', e)
                sys.print_exception(e)
        return self.airQualityStats


class AirQualityStats:

    def __init__(self):
        self.pm25 = -1
        self.pm10 = -1
        self.status = -1

    def update(self, pm25, pm10, status):
        self.pm25 = pm25
        self.pm10 = pm10
        self.status = status

    def __str__(self):
        return '{0} PM2.5, {1} PM10, status: {2}'.format(
            self.pm25,
            self.pm10,
            self.status)
