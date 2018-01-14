import RPi.GPIO as GPIO
import os
import picamera
import time


import threading
import Adafruit_PCA9685


class Robot():
    def __init__(self):
       
        self.servo = 380
        GPIO.setmode(GPIO.BCM)
     
        GPIO.setup(27, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)


class RobotMove(Robot):
    def __init__(self):
        super().__init__()
        self.speed = 0
        self.dirL = False
        self.dirR = True
        
        self.motor1 = GPIO.PWM(24, 500)
        self.motor1.start(0)
        self.motor2 = GPIO.PWM(23, 500)
        self.motor2.start(0)
        
    def check_distance(self):
        
        if self.dist < 10:
            GPIO.output(13, True)
        else:
            GPIO.output(13, False)
                  
                    
    def move_robot(self, dirL, dirR):
        self.dirL = dirL
        self.dirR = dirR
        if self.speed == 0:
            self.speed = 40
            
    def speed_up(self, v):
        if self.speed < 89:
            self.speed += v
            
    def speed_down(self, v):
        if self.speed > 40:
            self.speed -= v
    
    def stop(self):
        self.speed = 0

    def update(self):
        GPIO.output(27, self.dirL)
        GPIO.output(22, self.dirR)
        
        self.motor1.ChangeDutyCycle(self.speed)
        self.motor2.ChangeDutyCycle(self.speed)
    

class DistanceSensor(threading.Thread):
    def __init__(self):
       
        self.trig = 4
        self.echo = 5
        self.dist = 0
        self.can_run = threading.Event()
        self.thing_done = threading.Event()
        self.thing_done.set()
        self.can_run.set()
        threading.Thread.__init__(self)

    def run(self):

        while True:
            self.can_run.wait()
            try:
                self.thing_done.clear()
                              
                GPIO.setup(self.trig, GPIO.OUT)
                GPIO.setup(self.echo, GPIO.IN)
                
                GPIO.output(self.trig, False)
                time.sleep(0.5)
                
                GPIO.output(self.trig, True)
                time.sleep(0.0001)
                GPIO.output(self.trig, False)
                
                while GPIO.input(self.echo) == 0:
                    pulse_start = time.time()
                
                while GPIO.input(self.echo) == 1:
                    pulse_end = time.time()

                pulse_duration = pulse_end - pulse_start
                self.dist = pulse_duration * 17150
                self.dist = round(self.dist, 2)
                RobotMove.check_distance(self)
                
            finally:
                self.thing_done.set()

    def pause(self):
        self.can_run.clear()
        self.thing_done.wait()

    def resume(self):
        self.can_run.set()


class Camera():
    
    def cam_play(self):
        os.system('uv4l --driver raspicam --auto-video_nr --encoding h264 --width 320 --height 240 --quality 10 --framerate 10 --vflip')

    def cam_stop(self):
        os.system('sudo pkill uv4l')


class CameraMove(Robot):
    def __init__(self):
        super().__init__()
      
    def cam_move(self, x):
        self.servo += x
        if self.servo > 460:
            self.servo = 460
        if self.servo < 320:
            self.servo = 320
 
        self.pwm.set_pwm(0, 0, self.servo)
