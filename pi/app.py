from flask import Flask, render_template, Response, request
from camera import VideoCamera
import requests
import random

app = Flask(__name__)


@app.route('/')
def index():
    hum = random.randint(0, 100)
    tem = random.randint(-100,100)
    templateData = {
        'tem': tem,
        'hum': hum
    }
    return render_template('index.html', **templateData)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cmd', methods=['POST'])
def cmd():
    c = request.form.to_dict()
    for key, val in c.items():
        cmd_key = key
        break
    
    # we can pass it to moto.
    print(cmd_key)
    return "ok"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, threaded=True, debug=True)