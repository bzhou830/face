import Adafruit_DHT
import RPi.GPIO as GPIO

# DHT11 温湿度传感器管脚定义
makerobo_pin = 17


class DHT:
    # GPIO口定义
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT11

    def get_temp_hum(self):
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, makerobo_pin)
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
                break
            else:
                print('Failed to get reading. Try again!')
        return humidity, temperature

    def destroy(self):
        GPIO.cleanup()  # 释放资源