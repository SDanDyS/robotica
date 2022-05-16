from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import logging

class view:
    def show(self):
        return bytes("<p>Test</p>", "utf-8")

class http_server:
        def __init__(self, view):
            requestHandler.view = view
            server = HTTPServer(('', 8080), requestHandler)
            server.serve_forever()

class requestHandler(BaseHTTPRequestHandler):
    t1 = None
    def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.view.show())
                        
            return

class dashboardServer:
    #def __init__(self):
    def start(self):
        logging.info("Starting webserver...")

        self.view = view()
        self.server = http_server(self.view)

if __name__ == '__main__':
    m = main()