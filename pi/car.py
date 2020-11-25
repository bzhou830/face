import RPi.GPIO as GPIO

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

class Car:
    # 电机引脚初始化为输出模式
    # 按键引脚初始化为输入模式
    # 超声波引脚初始化
    def __init__(self):
        # 设置GPIO口为BCM编码方式
        GPIO.setmode(GPIO.BCM)
        # 忽略警告信息
        GPIO.setwarnings(False)
        
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

