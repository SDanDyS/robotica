import time
import logging
from flask import Flask, render_template
from random import randrange
import subprocess as sp
import json
from threading import *
import os
from distance.HCSRO4Component import *

class dashboardServer(Thread):
    app = Flask(__name__)

    @app.route('/api')
    def getData():
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

        btFile = open(os.path.dirname(__file__) + '/../btData')
        btRead = btFile.read()
        btRead = btRead.replace("\'", "\"")
        parsedData = json.loads(btRead)

        
        # print("----------------btFile-----------")
        # print(btFile.getmtime(btFile))

        if not 'LY' in parsedData:
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
        weightFile = open(os.path.dirname(__file__) + '/../weightData')
        data['weight'] = int(weightFile.read())

        # Voltage sensor
        voltageFile = open(os.path.dirname(__file__) + '/../voltageData')
        data['voltage'] = voltageFile.read()


        # # Distance sensor
        data['distance'] = 0
        # try:
        #     distance = sensorDistance()
        #     data['distance'] = distance
        # except:
        #     data['distance'] = 0
        #     pass

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

    def run(self):
        logging.info("Starting webserver...")
        from waitress import serve
        serve(self.app, host="0.0.0.0", port=8080)

if __name__ == '__main__':
    app.run(debug=True)