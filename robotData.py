import serial
import redis
import time

robot = serial.Serial('COM10', 115200)

r = redis.Redis(host='localhost', port=6379, db=0)

while True:
    line = robot.readline().decode().strip()

    values = line.split(',')

    for i, value in enumerate(values):
        if len(values) >= 19:
            print(values)
            timestamp = time.time()
            r.hset('robot_sensors', 'timestamp', timestamp)

            r.hset('robot_sensors', 'encoder_left', values[0])
            r.hset('robot_sensors', 'encoder_right', values[2])
            
            r.hset('robot_sensors', 'sonar0', values[10])
            r.hset('robot_sensors', 'sonar1', values[11])
            r.hset('robot_sensors', 'sonar2', values[12])
            r.hset('robot_sensors', 'sonar3', values[13])
            r.hset('robot_sensors', 'sonar4', values[14])
            r.hset('robot_sensors', 'sonar5', values[15])

        #r.set(f"value{i}", value)

        # "sensors": Encoder