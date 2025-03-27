curRSpeed = 0
curLSpeed = 0
RSpeed = 0
LSpeed = 0
delta = 0
time = 0
maxSpeed = 255
acceleration = 500
turn = 0
line = False
lineCol = 200
dist = False
distObj = 10

radio.set_group(19)

stop = True
def on_received_number(receivedNumber):
    if receivedNumber == 3:
        stop = True
    if receivedNumber == 2:
        stop = False
    pass
radio.on_received_number(on_received_number)

def on_forever():
    global delta, curLSpeed, curRSpeed, LSpeed, RSpeed, dist, line
    if stop:
        return

    dist = distObj >= maqueenPlusV2.read_ultrasonic(DigitalPin.P13, DigitalPin.P14)
    line = lineCol >= maqueenPlusV2.read_line_sensor_data(maqueenPlusV2.MyEnumLineSensor.SENSOR_L2)
    print(curLSpeed)
    if line:
        setSpeed(turn,1)
    else:
        setSpeed(1,turn)
    #print(delta + " " + time)
    if False:
        brake()
    else:
        curLSpeed = accelerate(delta,curLSpeed,LSpeed)
        curRSpeed = accelerate(delta,curRSpeed,RSpeed)
        setMotor(curLSpeed, curRSpeed)
    delta = 0
basic.forever(on_forever)

def brake():
    global curLSpeed, curRSpeed, LSpeed, RSpeed
    curLSpeed = 0
    curRSpeed = 0
    LSpeed = 0 
    RSpeed = 0
    setMotor(0,0)



def accelerate(deltaT, curSpeed, speed):
    global acceleration
    if curSpeed < speed:
        curSpeed += acceleration*deltaT
        if curSpeed > speed: 
            curSpeed = speed
    if curSpeed > speed:
        curSpeed -= acceleration*deltaT
        if curSpeed < speed: 
            curSpeed = speed
    return curSpeed
    

def setSpeed(l: number = 1, r: number = 1):
    global curLSpeed, curRSpeed, LSpeed, RSpeed, maxSpeed
    LSpeed = l * maxSpeed
    RSpeed = r * maxSpeed

def setMotor(l: number = 255, r: number = 255):
    print(l + " " + r)
    if l > 0:
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, l)
    else:
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, maqueenPlusV2.MyEnumDir.BACKWARD, -l)
    if r > 0:
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, r)
    else:
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, maqueenPlusV2.MyEnumDir.BACKWARD, -r)

def on_every_interval():
    global delta, time
    time += .01
    delta += .01
loops.every_interval(1, on_every_interval)

