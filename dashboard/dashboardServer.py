import time
import logging
from flask import Flask, render_template
from random import randrange

class dashboardServer:
    app = Flask(__name__)

    @app.route('/api/rand')
    def getRand():
        return str(randrange(10)), 200, {"Access-Control-Allow-Origin": "*"}

    @app.route('/api/bt')
    def getBt():
        return str(randrange(10)), 200, {"Access-Control-Allow-Origin": "*"}

    @app.route('/')
    def hello_world():
        return render_template("index.html")

    def start(self):
        logging.info("Starting webserver...")

        self.app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)