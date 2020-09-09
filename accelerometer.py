import time
import math
import board
import busio
import adafruit_adxl34x
from datetime import datetime
import requests
from threading import Thread
import socket

#import numpy as np
#import matplotlib.pyplot as plt

#plt.axis([0, 100, -3, 3])

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
bag_id = socket.gethostname().split('-')[1]
print(bag_id)
i=0

# mass in kilograms
mass = 30

v_old = 0
url = "http://ec2-18-217-1-165.us-east-2.compute.amazonaws.com/punch"
waiter = 0
score = 0
p_count = 0

def request(myjson):
    x = requests.post(url, json = myjson)

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)
    
    accel_x = accelerometer.acceleration[0]
    accel_y = accelerometer.acceleration[1]
    accel_z = accelerometer.acceleration[2]
    accel_a = math.sqrt(float(accel_x)**2 + float(accel_y)**2 + float(accel_z)**2)
    force = mass * (abs(accel_x) + abs(accel_y) + abs(accel_z))
    if accel_a > 12: 
        score+=float(accel_a)-9.78
        p_count+=1
        print(p_count, score)
        myobj = {"bag_id":str(bag_id),"score":str(score),"count":str(p_count)}
        t = Thread(target=request, args=(myobj,))
        t.start()
        time.sleep(.1)
