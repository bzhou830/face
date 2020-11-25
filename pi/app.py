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

# DHT11 温湿度传感器管脚定义
makerobo_pin = 17

# 设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

# 忽略警告信息
GPIO.setwarnings(False)


class Car:
    # 电机引脚初始化为输出模式
    # 按键引脚初始化为输入模式
    # 超声波引脚初始化
    def __init__(self):
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
        self.pwm_ENA1 = GPIO.PWM(ENA1, 2000)
        self.pwm_ENB1 = GPIO.PWM(ENB1, 2000)
        self.pwm_ENA2 = GPIO.PWM(ENA2, 2000)
        self.pwm_ENB2 = GPIO.PWM(ENB2, 2000)
        self.pwm_ENA1.start(0)
        self.pwm_ENB1.start(0)
        self.pwm_ENA2.start(0)
        self.pwm_ENB2.start(0)
    
    def reset_pins(self):
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


    def run(self, leftspeed=50, rightspeed=50):
        '''
        四个轮子均前转
        '''        
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
        GPIO.output(INC, GPIO.HIGH)
        GPIO.output(IND, GPIO.LOW)

        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        
        self.pwm_ENB1.ChangeDutyCycle(leftspeed)
        self.pwm_ENA2.ChangeDutyCycle(rightspeed)
        self.pwm_ENA1.ChangeDutyCycle(leftspeed)
        self.pwm_ENB2.ChangeDutyCycle(rightspeed)

    def back(self, leftspeed=50, rightspeed=50):
        '''
        四个轮子均后转
        '''
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.HIGH)
        GPIO.output(INC, GPIO.LOW)
        GPIO.output(IND, GPIO.HIGH)

        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        
        self.pwm_ENB1.ChangeDutyCycle(leftspeed)
        self.pwm_ENA2.ChangeDutyCycle(rightspeed)
        self.pwm_ENA1.ChangeDutyCycle(leftspeed)
        self.pwm_ENB2.ChangeDutyCycle(rightspeed)
    
    
    def left(self, leftspeed=50, rightspeed=50):
        '''
        左轮不动，右轮前转
        '''
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
        GPIO.output(INC, GPIO.HIGH)
        GPIO.output(IND, GPIO.LOW)
        self.pwm_ENB1.ChangeDutyCycle(leftspeed)
        self.pwm_ENA2.ChangeDutyCycle(rightspeed)


    def right(self, leftspeed=50, rightspeed=50):
        '''
        右轮不动，左轮前转
        '''
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        self.pwm_ENA1.ChangeDutyCycle(leftspeed)
        self.pwm_ENB2.ChangeDutyCycle(rightspeed)

   
    def spin_left(self, leftspeed=85, rightspeed=85):
        '''
        右轮前转，左轮后转
        '''
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
        GPIO.output(INC, GPIO.HIGH)
        GPIO.output(IND, GPIO.LOW)
        
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        self.pwm_ENB1.ChangeDutyCycle(leftspeed)
        self.pwm_ENA2.ChangeDutyCycle(rightspeed)
        self.pwm_ENA1.ChangeDutyCycle(leftspeed)
        self.pwm_ENB2.ChangeDutyCycle(rightspeed)

    # 小车原地右转
    def spin_right(self, leftspeed=85, rightspeed=85):
        '''
        左轮前转，右轮后转
        '''
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.HIGH)
        GPIO.output(INC, GPIO.LOW)
        GPIO.output(IND, GPIO.HIGH)
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        self.pwm_ENB1.ChangeDutyCycle(leftspeed)
        self.pwm_ENA2.ChangeDutyCycle(rightspeed)
        self.pwm_ENA1.ChangeDutyCycle(leftspeed)
        self.pwm_ENB2.ChangeDutyCycle(rightspeed)

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


class Gps:
    def __init__(self):
        self.x = L76X.L76X()
        self.x.L76X_Set_Baudrate(9600)
        self.x.L76X_Send_Command(self.x.SET_NMEA_BAUDRATE_115200)
        time.sleep(2)
        self.x.L76X_Set_Baudrate(115200)
        self.x.L76X_Send_Command(self.x.SET_POS_FIX_400MS)
        # Set output message
        self.x.L76X_Send_Command(self.x.SET_NMEA_OUTPUT)
        self.x.L76X_Exit_BackupMode()

    def get_gps(self):
        self.x.L76X_Gat_GNRMC()
        if self.x.Status == 1:
            print('Already positioned')
        else:
            print('No positioning')
            return ""
        print('Time %d:' % self.x.Time_H)
        print('%d:' % self.x.Time_M)
        print('%d' % self.x.Time_S)
        print('Lon = %f' % self.x.Lon)
        print('Lat = %f' % self.x.Lat)
        self.x.L76X_Baidu_Coordinates(self.x.Lat,self.x.Lon)
        print('Baidu coordinate %f' % self.x.Lat_Baidu)
        print(',%f' % self.x.Lon_Baidu)
        res = 'Time %d:%d:%d. \n Lon = %f, Lat = %f \n Baidu coordinate %f, %f.'.format(self.x.Time_H, self.x.Time_M, self.x.Time_S, self.x.Lon, self.x.Lat, self.x.Lat_Baidu, self.x.Lon_Baidu)
        return res


car = Car()
dht = DHT()
gps = Gps()

app = Flask(__name__)

@app.route('/')
def index():
    #car.brake()
    hum, tem = 10, 100  # dht.get_temp_hum()
    gps_data = 1111111  # gps.get_gps()
    templateData = {
        'tem': tem,
        'hum': hum,
        'gps': gps
    }
    return render_template('index.html', tem = tem, hum = hum, gps = gps)


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
    car.reset_pins()
    if cmd_key == "front":
        car.run()
    elif cmd_key == "leftFront":
        car.left()
    elif cmd_key == "stop":
        car.brake()
    elif cmd_key == "rightFront":
        car.right()
    elif cmd_key == "rear":
        car.back()
    elif cmd_key == "leftRear":
        car.spin_left()
    elif cmd_key == "rightRear":
        car.spin_right()

    # we can pass it to moto.
    print(cmd_key)
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, threaded=True, debug=True)
