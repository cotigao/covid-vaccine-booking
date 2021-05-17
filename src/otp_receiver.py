from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import tempfile

class S(BaseHTTPRequestHandler):
    def __init__(self, mobile):
        self.mobile = mobile

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        with open(os.path.join(tempfile.gettempdir(), str(self.mobile) + '_cowin_covid_otp'), "w") as f:
            f.write(json.loads(post_data)["otp"])

        self._set_response()
        self.wfile.write(json.dumps({'received': 'ok'}).encode('utf-8'))

def run_otp_receiver(mobile, server_class=HTTPServer, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    handler_class = S(mobile)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

#run_otp_receiver()
