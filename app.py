from flask import Flask, jsonify, render_template, request
import requests
import redis
import time

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    response = requests.get("http://localhost:5000/sensors")
    data = response.json()

    return render_template("index.html", data=data)

@app.route('/sensors')
def get_sensors():
    sensors = {        
        "timestamp": r.hget('robot_sensors', 'timestamp').decode('utf-8'),
        "motor_left": {
            "speed": r.hget('robot_sensors','encoder_left').decode('utf-8'),
            "voltage": "0",
            "current": "0"
        },
        "motor_right": {
            "speed": r.hget('robot_sensors','encoder_right').decode('utf-8'),
            "voltage": "0",
            "current": "0"
        },
        "battery": {
            "voltage": "0",
            "current": "0"
        },
        "accelerometer": {
            "x": "0",
            "y": "0",
            "z": "0"
        },
        "sonar": [
            r.hget('robot_sensors','sonar0').decode('utf-8'),
            r.hget('robot_sensors','sonar1').decode('utf-8'),
            r.hget('robot_sensors','sonar2').decode('utf-8'),
            r.hget('robot_sensors','sonar3').decode('utf-8'),
            r.hget('robot_sensors','sonar4').decode('utf-8'),
            r.hget('robot_sensors','sonar5').decode('utf-8')
        ]
    }
    return  jsonify(sensors)

@app.route('/input', methods=['POST'])
def input_data():
    cmd = request.form['exec']
    r.set('command', cmd)

    response = requests.get("http://localhost:5000/sensors")
    data = response.json()
    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)