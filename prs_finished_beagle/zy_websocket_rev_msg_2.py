from websocket import create_connection 
from json import dumps 
import json 
import rcpy 
import time 
import rcpy.servo as servo 
import rcpy.clock as clock 
import getopt, sys
import datetime

def initial():
    with open('open.json', 'r') as f:
        data = json.load(f)
    #print(data)
    datalen = len(data['poses']) #6
    servo.enable()
    for i in range(0, datalen):
        #print(data['poses'][i]['position']['x'],data['poses'][i]['position']['z'])
        srvo[i] = servo.Servo(data['poses'][i]['position']['x'])
        clck = clock.Clock(srvo[i], data['poses'][i]['position']['y'])
        clck.start()
        srvo[i].set(data['poses'][i]['position']['z'])
        #print(i)
    time.sleep(1)
    return

def close1():
    for i in range(0, 5):
        srvo[i].set(data['poses'][i]['position']['z'])
        #print(i)
    srvo[5].set(data['poses'][5]['position']['z'])
    #print('Duty of close_1: ',data['poses'][4]['position']['z'])
    srvo[4].set(data['poses'][10]['position']['z'])
    #print('Duty of close_2: ',data['poses'][10]['position']['z'])
    time.sleep(0.6)
    print('close')
    return

def open1():
    for i in range(6, 12):
        srvo[i-6].set(data['poses'][i]['position']['z'])
    #print('Duty of open_1: ',data['poses'][10]['position']['z'])
    srvo[4].set(data['poses'][4]['position']['z'])
    #print('Duty of open_2: ',data['poses'][4]['position']['z'])
    print('open')
    time.sleep(0.6)
    return

def rock():
    for i in range(0, 4):
        srvo[i].set(data['poses'][i]['position']['z'])
    srvo[5].set(data['poses'][5]['position']['z'])
    print('rock')
    time.sleep(0.2)
    return
def paper():
    for i in range(6, 10):
        srvo[i-6].set(data['poses'][i]['position']['z'])
    srvo[5].set(data['poses'][11]['position']['z'])
    print('paper')
    time.sleep(0.2)
    return
def scissors():
    for i in range(12, 16):
        srvo[i-12].set(data['poses'][i]['position']['z'])
    srvo[5].set(data['poses'][16]['position']['z'])
    print('scissors')
    time.sleep(0.2)
    return
def oneaction():
    datalen = len(data['poses'])
    servo.enable()
    for i in range(0, datalen):
        srvo[i].set(data['poses'][i]['position']['z'])
    time.sleep(0.2)
    return

srvo = [0 for i in range(6)] #(0,0,0,0,0,0)
initial()
print('Starting')
while(True):
    ws = create_connection("ws://10.109.99.41:9090")
    start_time = datetime.datetime.now()
    msg = {'op': 'subscribe', 'topic': '/rand_no'} #Receive random num from ROS topic
    ws.send(dumps(msg))
    result =  ws.recv()
    mm=json.loads(result)
    print('Start game!')
    print(mm['msg']['data'])
    randno = mm['msg']['data']
    print('Over')
    print('Start Again')
    servo.enable()
    #robotic hand move
    with open('rock_paper_scissors_1.json', 'r') as f:
        data = json.load(f)
    open1()
    close1()
    open1()
    close1()
    open1()
    close1()
    open1()
    close1()
    #Receive random number from rostopic
    print("Receiving Final Decision...")
    randno = mm['msg']['data']
    #print(randno)
    if randno == 1:
        rock()
    elif randno == 2:
        paper()
    else:
        scissors()
    srvo[4].set(data['poses'][10]['position']['z']) #-1.5
    srvo[4].set(data['poses'][4]['position']['z']) #0.8
    time.sleep(2)
    #Compare results in MATLAB, receive the final result from MATLAB
    msg = {'op': 'subscribe', 'topic': '/final_result'} #Receive random num from ROS topic
    ws.send(dumps(msg))
    result =  ws.recv()
    #print("Received '%s'" % result)
    mm=json.loads(result)
    print(mm['msg']['data'])
    re = mm['msg']['data']
    if re == 1:
        print('You win!')
        with open('win.json', 'r') as f:
            data = json.load(f)
    elif re == 2:
        print('You lose!')
        with open('lose.json', 'r') as f:
            data = json.load(f)
    elif re == 3:
        print('Tie!')
        with open('tie.json', 'r') as f:
            data = json.load(f)
    else:
        print('No result!')
        with open('open.json', 'r') as f:
            data = json.load(f)
 
    oneaction()
    time.sleep(3)
    end_time = datetime.datetime.now()
    oneround = end_time-start_time
    print(oneround)
    ws.close()
