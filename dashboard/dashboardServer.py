import time
import logging
from flask import Flask, render_template
from random import randrange
import subprocess as sp
import json

class dashboardServer:
    app = Flask(__name__)

    @app.route('/api')
    def getData():
        data = {}
        
        # Bluetooth info
        bluetoothData = {}
        stdoutdata = sp.getoutput("hcitool con")
        if "84:CC:A8:69:97:D2" in stdoutdata.split():
            bluetoothData['connection'] = "connected"
            temp = randrange(2000)
            bluetoothData['ly'] = str(temp)
            bluetoothData['lx'] = str(temp)
            bluetoothData['ry'] = str(temp)
            bluetoothData['rx'] = str(temp)
        else:
            bluetoothData['connection'] = "disconnected"
            bluetoothData['ly'] = "-"
            bluetoothData['lx'] = "-"
            bluetoothData['ry'] = "-"
            bluetoothData['rx'] = "-"
        data['bluetooth'] = bluetoothData

        # Distance sensor
        data['distance'] = randrange(100)

        # Weight sensor
        data['weight'] = randrange(100)

        json_data = json.dumps(data)
        return json_data, 200, {"Access-Control-Allow-Origin": "*", 'Content-Type': 'application/json'}

    @app.route('/api/rand')
    def getRand():
        return str(randrange(10)), 200, {"Access-Control-Allow-Origin": "*"}

    @app.route('/api/bt')
    def getBt():
        stdoutdata = sp.getoutput("hcitool con")
        if "84:CC:A8:69:97:D2" in stdoutdata.split():
            return "connected", 200, {"Access-Control-Allow-Origin": "*"}
        else:
            return "disconnected", 200, {"Access-Control-Allow-Origin": "*"}
    
    @app.route('/api/weight')
    def getWeight():
        return str(randrange(1000)), 200, {"Access-Control-Allow-Origin": "*"}

    @app.route('/')
    def index():
        return render_template("index.html")

    def start(self):
        logging.info("Starting webserver...")

        self.app.run(port=8080, debug=True)

if __name__ == '__main__':
    app.run(debug=True)