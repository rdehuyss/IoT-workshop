# IoT workshop

This is the Github Repository for the IOT Workshop.

## Prerequisites
### Hardware
- ESP32 dev board running micropython and microusb cable
- sensors (DHT11, DHT22, BME680)
- Breadboard
- Jumper cables

### Software
- CH341SER.exe USB-to-UART bridge (windows only)
- Latest Docker and Docker Compose
- PyCharm
- Python 3.6
- Upgrade pip (`python -m pip install --upgrade pip`)
- Esptool (`pip install esptool`)
- Jupyter (`pip install jupyter`)
- Jupyter MicroPython Kernel
  - Navigate to ./00 Installation/Jupyter Notebook/
  - Run `pip install -e jupyter_micropython_kernel`
  - Run `python -m jupyter_micropython_kernel.install`
  - Verify Jupyter MicroPython Kernel installation using command `jupyter kernelspec list`
- Putty

