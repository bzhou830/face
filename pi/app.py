from flask import Flask, render_template, Response, request, jsonify, json
from camera import VideoCamera
import requests
import random
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import L76X
import math

# 小车电机引脚定义
IN1 = 24
IN2 = 23
IN3 = 22
IN4 = 21
INA = 17
INB = 5
INC = 6
IND = 12
ENA1 = 18
ENB1 = 19
ENA2 = 27
ENB2 = 26

# 超声波引脚定义
makerobo_ECHO = 13
makerobo_TRIG = 16

makerobo_pin = 17  # DHT11 温湿度传感器管脚定义

# 设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

# 忽略警告信息
GPIO.setwarnings(False)


class Car:
    # 电机引脚初始化为输出模式
    # 按键引脚初始化为输入模式
    # 超声波引脚初始化
    def init_stat(self):
        global pwm_ENA1
        global pwm_ENB1
        global pwm_ENA2
        global pwm_ENB2
        GPIO.setup(ENA1, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ENB1, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ENA2, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(INA, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(INB, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ENB2, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(INC, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IND, GPIO.OUT, initial=GPIO.LOW)
        # GPIO.setup(key,GPIO.IN)
        GPIO.setup(makerobo_ECHO, GPIO.IN)
        GPIO.setup(makerobo_TRIG, GPIO.OUT)
        # 设置pwm引脚和频率为2000hz
        pwm_ENA1 = GPIO.PWM(ENA1, 2000)
        pwm_ENB1 = GPIO.PWM(ENB1, 2000)
        pwm_ENA2 = GPIO.PWM(ENA2, 2000)
        pwm_ENB2 = GPIO.PWM(ENB2, 2000)
        pwm_ENA1.start(0)
        pwm_ENB1.start(0)
        pwm_ENA2.start(0)
        pwm_ENB2.start(0)

    # 小车前进
    def run(self, leftspeed, rightspeed):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
        GPIO.output(INC, GPIO.HIGH)
        GPIO.output(IND, GPIO.LOW)
        pwm_ENB1.ChangeDutyCycle(leftspeed)
        pwm_ENA2.ChangeDutyCycle(rightspeed)
        pwm_ENA1.ChangeDutyCycle(leftspeed)
        pwm_ENB2.ChangeDutyCycle(rightspeed)

    # 小车后退
    def back(self, leftspeed, rightspeed):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.HIGH)
        GPIO.output(INC, GPIO.LOW)
        GPIO.output(IND, GPIO.HIGH)
        pwm_ENB1.ChangeDutyCycle(leftspeed)
        pwm_ENA2.ChangeDutyCycle(rightspeed)
        pwm_ENA1.ChangeDutyCycle(leftspeed)
        pwm_ENB2.ChangeDutyCycle(rightspeed)

    # 小车左转
    def left(self, leftspeed, rightspeed):
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.HIGH)
        GPIO.output(INC, GPIO.LOW)
        GPIO.output(IND, GPIO.HIGH)
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENB1.ChangeDutyCycle(leftspeed)
        pwm_ENA2.ChangeDutyCycle(rightspeed)
        pwm_ENA1.ChangeDutyCycle(leftspeed)
        pwm_ENB2.ChangeDutyCycle(rightspeed)

    # 小车右转
    def right(self, leftspeed, rightspeed):
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENB1.ChangeDutyCycle(leftspeed)
        pwm_ENA2.ChangeDutyCycle(rightspeed)

    # 小车原地左转
    def spin_left(self, leftspeed, rightspeed):
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
        GPIO.output(INC, GPIO.HIGH)
        GPIO.output(IND, GPIO.LOW)
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENB1.ChangeDutyCycle(leftspeed)
        pwm_ENA2.ChangeDutyCycle(rightspeed)
        pwm_ENA1.ChangeDutyCycle(leftspeed)
        pwm_ENB2.ChangeDutyCycle(rightspeed)

    # 小车原地右转
    def spin_right(self, leftspeed, rightspeed):
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.HIGH)
        GPIO.output(INC, GPIO.LOW)
        GPIO.output(IND, GPIO.HIGH)
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwm_ENB1.ChangeDutyCycle(leftspeed)
        pwm_ENA2.ChangeDutyCycle(rightspeed)
        pwm_ENA1.ChangeDutyCycle(leftspeed)
        pwm_ENB2.ChangeDutyCycle(rightspeed)

    # 小车停止
    def brake(self):
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.LOW)
        GPIO.output(INC, GPIO.LOW)
        GPIO.output(IND, GPIO.LOW)
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)


class DHT:
    # GPIO口定义
    def makerobo_setup(self):
        sensor = Adafruit_DHT.DHT11

    # 循环函数
    def loop(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, makerobo_pin)
        while True:
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            else:
                print('Failed to get reading. Try again!')
            time.sleep(1)  # 延时1s

    def destroy(self):
        GPIO.cleanup()  # 释放资源


class Gps:
    def init_stat(self):
        x = L76X.L76X()
        x.L76X_Set_Baudrate(9600)
        x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
        time.sleep(2)
        x.L76X_Set_Baudrate(115200)
        x.L76X_Send_Command(x.SET_POS_FIX_400MS)
        # Set output message
        x.L76X_Send_Command(x.SET_NMEA_OUTPUT)
        x.L76X_Exit_BackupMode()

    def get_gps(self):
        self.x.L76X_Gat_GNRMC()
        if self.x.Status == 1:
            print('Already positioned')
        else:
            print('No positioning')
        print('Time %d:' % self.x.Time_H)
        print('%d:' % self.x.Time_M)
        print('%d' % self.x.Time_S)
        print('Lon = %f' % self.x.Lon)
        print(' Lat = %f' % self.x.Lat)
        self.x.L76X_Baidu_Coordinates(self.x.Lat,self.x.Lon)
        print('Baidu coordinate %f' % self.x.Lat_Baidu)
        print(',%f' % self.x.Lon_Baidu)


car = Car()
dht = DHT()
gps = Gps()

app = Flask(__name__)


@app.route('/')
def index():
    hum = random.randint(0, 100)
    tem = random.randint(-100, 100)
    gps = "30.111000, 150.0000"
    templateData = {
        'tem': tem,
        'hum': hum,
        'gps': gps
    }
    return render_template('index.html', **templateData)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cmd', methods=['POST'])
def cmd():
    c = request.form.to_dict()
    for key, val in c.items():
        cmd_key = key
        break

    # we can pass it to moto.
    print(cmd_key)
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, threaded=True, debug=True)
