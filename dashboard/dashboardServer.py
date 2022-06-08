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
        stdoutdata = sp.getoutput("hcitool con")
        if "84:CC:A8:69:97:D2" in stdoutdata.split():
            bluetoothData['connected'] = True
            temp = randrange(2000)
            bluetoothData['ly'] = str(temp)
            bluetoothData['lx'] = str(temp)
            bluetoothData['ry'] = str(temp)
            bluetoothData['rx'] = str(temp)
        else:
            bluetoothData['connected'] = False
            bluetoothData['ly'] = None
            bluetoothData['lx'] = None
            bluetoothData['ry'] = None
            bluetoothData['rx'] = None
        data['controller'] = bluetoothData

        # Distance sensor
        data['distance'] = randrange(100)

        # Weight sensor
        data['weight'] = randrange(100)

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

    def start(self):
        logging.info("Starting webserver...")
        from waitress import serve
        serve(self.app, host="0.0.0.0", port=8080)

if __name__ == '__main__':
    app.run(debug=True)