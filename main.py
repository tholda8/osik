curRSpeed = 0
curLSpeed = 0
RSpeed = 0
LSpeed = 0
delta = 0
time = 0
maxSpeed = 255
acceleration = 200
turn = 0.2
line = False
lineCol = 100
dist = False
distObj = 10

def on_forever():
    global delta, curLSpeed, curRSpeed, LSpeed, RSpeed, dist, line
    dist = distObj >= maqueenPlusV2.read_ultrasonic(DigitalPin.P13, DigitalPin.P14)
    line = lineCol >= maqueenPlusV2.read_line_sensor_data(maqueenPlusV2.MyEnumLineSensor.SENSOR_L2)

    if line:
        setSpeed(turn,1)
    else:
        setSpeed(1,turn)

    #print(delta + " " + time)
    if dist:
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
    global curLSpeed, curRSpeed, LSpeed, RSpeed
    LSpeed = l * maxSpeed
    RSpeed = r * maxSpeed

def setMotor(l: number = 255, r: number = 255):
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

