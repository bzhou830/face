from flask import Flask, render_template, Response, request, jsonify, json
from camera import VideoCamera
import requests
import random
from car import Car
from dht11 import DHT
from gps import Gps


car = Car()
dht = DHT()
gps = Gps()

app = Flask(__name__)

@app.route('/')
def index():
    #car.brake()
    hum, tem = "--.-", "--.-"  # dht.get_temp_hum()
    gps_data = "----, ----"  # gps.get_gps()
    return render_template('index.html', tem = tem, hum = hum, gpsdata = gps_data)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_data')
def get_data():
    hum, tem = dht.get_temp_hum()
    gps_data = gps.get_gps()
    templateData = {
        'tem': tem,
        'hum': hum,
        'gps': gps_data
    }
    return jsonify(templateData)

@app.route('/cmd', methods=['POST'])
def cmd():
    c = request.form.to_dict()
    for key, val in c.items():
        cmd_key = key
        break
    car.reset_pins()
    if cmd_key == "front":
        car.run()
    elif cmd_key == "leftFront":
        car.left()
    elif cmd_key == "stop":
        car.brake()
    elif cmd_key == "rightFront":
        car.right()
    elif cmd_key == "rear":
        car.back()
    elif cmd_key == "leftRear":
        car.spin_left()
    elif cmd_key == "rightRear":
        car.spin_right()

    # we can pass it to moto.
    print(cmd_key)
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, threaded=True, debug=True)
