# IoT workshop

This is the Github Repository for the IOT Workshop.

## Prerequisites
### Hardware
- ESP32 dev board running micropython and microusb cable
- sensors (DHT11, DHT22, BME680)
- Breadboard
- Jumper cables

### Software
- CH341SER.exe USB-to-UART bridge (windows only), zie 00 Installation in deze repo
- Latest Docker and Docker Compose
- PyCharm
  - Go to settings > Plugins > Install Jetbrains Plugin > Search for MicroPython and install it
  - Troubleshooting: if MicroPython not available from Tools Menu, do the following: Go to settings > Project > Project Interpreter and make sure the following items are there:
    - adafruit-ampy (tested with v 1.0.5)
    - docopt (tested with v0.6.2)
- Python 3.6
- Upgrade pip (`python -m pip install --upgrade pip`)
- Esptool (`pip install esptool`)
- Jupyter (`pip install jupyter`)
- Jupyter MicroPython Kernel
  - Navigate to ./00 Installation/Jupyter Notebook/
  - Run `git clone https://github.com/goatchurchprime/jupyter_micropython_kernel`
  - Run `pip install -e jupyter_micropython_kernel`
  - Run `python -m jupyter_micropython_kernel.install`
  - Verify Jupyter MicroPython Kernel installation using command `jupyter kernelspec list`
- Putty (or any other Serial Console)

