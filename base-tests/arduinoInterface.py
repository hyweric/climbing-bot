import serial
import time

arduino = serial.Serial(port='/dev/cu.usbserial-10', baudrate=9600, timeout=.1)

def send_angle(servo_id, angle):
    message = f"{servo_id}{angle}\n"
    arduino.write(message.encode())
    time.sleep(0.05) # small delay to ensure data is sent

def transform_angle1(angle):
    return angle + 63 

def transform_angle2(angle):
    return angle + 50

while True:
    servo_id = input("SERVOID (1, 2, 3): ")
    if servo_id not in ['1', '2', '3']:
        print("invalid (1,2, or 3)")
        continue
    
    try:
        angle = int(input("Enter angle (-180-180): "))
        if -180 <= angle <= 180:
            angle = transform_angle1(angle) if servo_id == '' else transform_angle2(angle)
            send_angle(servo_id, angle)
        else:
            print("invalid (0-180)")
    except ValueError:
        print("invalid")