#! /usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_response(200)
        self.end_headers()
        self.wfile.flush()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.log_message('{}\n'.format(body.decode()))
        self.log_message(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.flush()

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
