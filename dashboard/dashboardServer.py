import time
import logging
from flask import Flask, render_template
from random import randrange
import subprocess as sp
import json
from threading import *
import os.path
from distance.HCSRO4Component import *

class dashboardServer(Thread):
    app = Flask(__name__)

    @app.route('/api')
    def getData():
        # print("--------------------------")
        # super(dashboardServer, self).get_weight()
        # super().get_weight()
        '''
        Exposes the robot API endpoint.

                Returns:
                        json_data (str): JSON content of robot,
                        status (int): 200 OK
                        headers (array): Set CORS, content-type application/json
        '''

        data = {}

        # General robot status
        data['online'] = True
        
        # Bluetooth info
        bluetoothData = {}

        btFile = open(os.path.dirname(__file__) + '/../sensorData/btData')
        btRead = btFile.read()
        btRead = btRead.replace("\'", "\"")
        parsedData = json.loads(btRead)

        if not 'ly' in parsedData or len(obj['ly']) == 0:
            bluetoothData['connected'] = False
            bluetoothData['ly'] = 0
            bluetoothData['lx'] = 0
            bluetoothData['ry'] = 0
            bluetoothData['rx'] = 0
            bluetoothData['flag'] = 0
            bluetoothData['driveorGrip'] = 0
        else:
            bluetoothData['connected'] = True
            bluetoothData['ly'] = int(parsedData["LY"])
            bluetoothData['lx'] = int(parsedData["LX"])
            bluetoothData['ry'] = int(parsedData["RY"])
            bluetoothData['rx'] = int(parsedData["RX"])
            bluetoothData['flag'] = int(parsedData["flag"])
            bluetoothData['driveorGrip'] = int(parsedData["driveOrGrip"])

        data['controller'] = bluetoothData

        # Weight sensor
        weightFile = open(os.path.dirname(__file__) + '/../sensorData/weightData')
        data['weight'] = int(weightFile.read())

        # TODO: Distance sensor
        # distance = sensorDistance()
        # print("---------------------------------")
        # print(distance)
        data['distance'] = 0

        # Convert to JSON string
        json_data = json.dumps(data)

        # Return in JSON format
        return json_data, 200, {"Access-Control-Allow-Origin": "*", 'Content-Type': 'application/json'}

    @app.route('/')
    def index():
        '''
        Shows the Dashboard page.

                Returns:
                        render_template (str): HTML content of index.html
        '''

        return render_template("index.html")

    # @app.route('/api/rand')
    # def getRand():
    #     return str(randrange(10)), 200, {"Access-Control-Allow-Origin": "*"}

    # @app.route('/api/bt')
    # def getBt():
    #     stdoutdata = sp.getoutput("hcitool con")
    #     if "84:CC:A8:69:97:D2" in stdoutdata.split():
    #         return "connected", 200, {"Access-Control-Allow-Origin": "*"}
    #     else:
    #         return "disconnected", 200, {"Access-Control-Allow-Origin": "*"}
    
    # @app.route('/api/weight')
    # def getWeight():
    #     return str(randrange(1000)), 200, {"Access-Control-Allow-Origin": "*"}

    def run(self):
        logging.info("Starting webserver...")
        from waitress import serve
        serve(self.app, host="0.0.0.0", port=8080)

if __name__ == '__main__':
    app.run(debug=True)