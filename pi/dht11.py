import Adafruit_DHT
import RPi.GPIO as GPIO

# DHT11 温湿度传感器管脚定义
makerobo_pin = 17


class DHT:
    # GPIO口定义
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT11
        self.hum = 0.0
        self.temp = 0.0

    def get_temp_hum(self):
        self.hum, self.temp = Adafruit_DHT.read_retry(self.sensor, makerobo_pin)
        if self.hum is not None and self.temp is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(self.temp, self.hum))
        return self.hum, self.temp

    def destroy(self):
        GPIO.cleanup()  # 释放资源