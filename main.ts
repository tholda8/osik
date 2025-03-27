let curRSpeed = 0
let curLSpeed = 0
let RSpeed = 0
let LSpeed = 0
let delta = 0
let time = 0
let maxSpeed = 255
let acceleration = 500
let turn = 0
let line = false
let lineCol = 200
let dist = false
let distObj = 10
radio.setGroup(19)
let stop = true
radio.onReceivedNumber(function on_received_number(receivedNumber: number) {
    let stop: boolean;
    if (receivedNumber == 3) {
        stop = true
    }
    
    if (receivedNumber == 2) {
        stop = false
    }
    
    
})
basic.forever(function on_forever() {
    
    if (stop) {
        return
    }
    
    dist = distObj >= maqueenPlusV2.readUltrasonic(DigitalPin.P13, DigitalPin.P14)
    line = lineCol >= maqueenPlusV2.readLineSensorData(maqueenPlusV2.MyEnumLineSensor.SensorL2)
    console.log(curLSpeed)
    if (line) {
        setSpeed(turn, 1)
    } else {
        setSpeed(1, turn)
    }
    
    // print(delta + " " + time)
    if (false) {
        brake()
    } else {
        curLSpeed = accelerate(delta, curLSpeed, LSpeed)
        curRSpeed = accelerate(delta, curRSpeed, RSpeed)
        setMotor(curLSpeed, curRSpeed)
    }
    
    delta = 0
})
function brake() {
    
    curLSpeed = 0
    curRSpeed = 0
    LSpeed = 0
    RSpeed = 0
    setMotor(0, 0)
}

function accelerate(deltaT: number, curSpeed: number, speed: number): number {
    
    if (curSpeed < speed) {
        curSpeed += acceleration * deltaT
        if (curSpeed > speed) {
            curSpeed = speed
        }
        
    }
    
    if (curSpeed > speed) {
        curSpeed -= acceleration * deltaT
        if (curSpeed < speed) {
            curSpeed = speed
        }
        
    }
    
    return curSpeed
}

function setSpeed(l: number = 1, r: number = 1) {
    
    LSpeed = l * maxSpeed
    RSpeed = r * maxSpeed
}

function setMotor(l: number = 255, r: number = 255) {
    console.log(l + " " + r)
    if (l > 0) {
        maqueenPlusV2.controlMotor(maqueenPlusV2.MyEnumMotor.LeftMotor, maqueenPlusV2.MyEnumDir.Forward, l)
    } else {
        maqueenPlusV2.controlMotor(maqueenPlusV2.MyEnumMotor.LeftMotor, maqueenPlusV2.MyEnumDir.Backward, -l)
    }
    
    if (r > 0) {
        maqueenPlusV2.controlMotor(maqueenPlusV2.MyEnumMotor.RightMotor, maqueenPlusV2.MyEnumDir.Forward, r)
    } else {
        maqueenPlusV2.controlMotor(maqueenPlusV2.MyEnumMotor.RightMotor, maqueenPlusV2.MyEnumDir.Backward, -r)
    }
    
}

loops.everyInterval(1, function on_every_interval() {
    
    time += .01
    delta += .01
})
