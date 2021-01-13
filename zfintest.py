import time
import math
import board
import busio
import adafruit_adxl34x
from datetime import datetime
import requests
from threading import Thread
import socket

# params
_bag_id = '020'
_i = 30
_f = 24
_x1_min = 287.0
_x1_max = 348.0
_x2_min = 252.0
_x2_max = 348.0

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

url = "http://ec2-18-217-1-165.us-east-2.compute.amazonaws.com/punch"

bag_id = socket.gethostname().split('-')[1]
print(bag_id)
def request(myjson):
    x = requests.post(url, json = myjson)

time.sleep(30)
#myobj2 = {"bag_id":str(bag_id),"score": "0","count": "0"}
xxx = requests.post(url, json = {"bag_id": bag_id, "score": "0", "count": "0"})
print(xxx)

previous = 0

i = 0

count = 0

mass = 50

score = 0

from datetime import datetime
prev_t = datetime.utcnow()
chained = False
second_chained = False

hit = False
fc = False
sc = False

while True:
    accel_x = accelerometer.acceleration[0]
    accel_y = accelerometer.acceleration[1]
    accel_z = accelerometer.acceleration[2]
    
    accel_a = math.sqrt(float(accel_x)**2 + float(accel_y)**2 + float(accel_z)**2)
    
    if accel_a > 26 and i - previous > 36:
        previous = i
        dt = datetime.utcnow()
        time_delta = (dt - prev_t).total_seconds()*1000.0
#        print(dt)
        if sc or (hit and not (time_delta > _x1_min and time_delta < _x1_max)) or (fc and not (time_delta > _x2_min and time_delta < _x2_max)):
            hit = True
            fc = False
            sc = False
        
        elif hit and time_delta > _x1_min and time_delta < _x1_max:
            hit = False
            fc = True
            sc = False
            
        elif fc and time_delta > _x2_min and time_delta < _x2_max:
            hit = False
            fc = False
            sc = True

        else:
            hit = True
            fc = False
            sc = False

            
        #print(str(hit), str(fc), str(sc))
        
        if hit:
            count += 1
            
        #print(str(hit), str(fc), str(sc))
        
        prev_t = dt
        #print(count)
        
        #print('\n')
        score += ((accel_a-9.78)*mass)/100 
        myobj = {"bag_id":str(bag_id),"score":str(score),"count": str(count)}
        t = Thread(target=request, args=(myobj,))
        t.start()
    i += 1

