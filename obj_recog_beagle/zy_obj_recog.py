from websocket import create_connection
from json import dumps
import json
import rcpy
import time
import rcpy.clock as clock
import rcpy.servo as servo


ws = create_connection("ws://10.109.99.41:9090")
print("Sending 'Hello, World'...\n\n")
msg = {'op': 'subscribe', 'topic': '/fibonacci/goal','type':'actionlib_tutorials/FibonacciActionGoal'}
ws.send(dumps(msg))

object = []
srvo = [0 for i in range(6)]
#print(srvo)    #(0,0,0,0,0,0)

def initial():
    with open('open_1.json', 'r') as f:
        data = json.load(f)
    #print(data)
    #channel = data['poses'][i]['position']['x']
    #period = data['poses'][i]['position']['y']
    #duty = data['poses'][i]['position']['z']
    datalen = len(data['poses'])
    servo.enable()
    for i in range(0, datalen):
        #print(data['poses'][i]['position']['x'],data['poses'][i]['position']['z'])
        srvo[i] = servo.Servo(data['poses'][i]['position']['x'])
        clck = clock.Clock(srvo[i], data['poses'][i]['position']['y'])
        clck.start()
        srvo[i].set(data['poses'][i]['position']['z'])
    time.sleep(1)
    return

def action():
    with open(jsfile, 'r') as f:
        data = json.load(f)
    #print(data)
    datalen = len(data['poses'])
    for i in range(0, datalen):
        srvo[i].set(data['poses'][i]['position']['z'])
        #print(data['poses'][i]['position']['z'])
    time.sleep(1)
    return

def reset():
    with open('open_1.json', 'r') as f:
        data = json.load(f)
    #print('open start')
    servo.enable()
    datalen = len(data['poses'])
    for i in range(0, datalen):
        print(i, data['poses'][i]['position']['x'], data['poses'][i]['position']['z'])
        srvo[i].set(data['poses'][i]['position']['z'])
    #print('open finish')
    time.sleep(1)
    return

initial()

while(True):
    servo.enable()
    print("Receiving...\n")
    rcpy.set_state(rcpy.RUNNING)
    result = ws.recv()
    print("\n"+result+"\n")
    mm=json.loads(result)
    print(mm['msg'])
    print(mm['msg']['goal']['order'])
    revnum = mm['msg']['goal']['order']
    for i in range(3):
        object = ['button','bottle','phone']
    print(object[revnum])
    jsname = object[revnum]
    jsfile = str(jsname)+".json"
    print(jsfile)
    time.sleep(1)

    action()
    time.sleep(2)
    reset()
    time.sleep(1)
    servo.disable()
    
    print('Over')
ws.close()
