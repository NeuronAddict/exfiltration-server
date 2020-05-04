#! /usr/bin/env python3
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler


parser = argparse.ArgumentParser('Exfiltration server.\nLog all queries and print result to exfiltrate data via http.')
parser.add_argument('port', default='8000', type=int, nargs='?', help='Port to listen on. Default: 8000')
parser.add_argument('--bind', default='0.0.0.0', nargs='?', help='IP to bind. Default: 0.0.0.0')

args = parser.parse_args()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.flush()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.flush()
        self.log_message(self.path)
        self.log_message('{}\n'.format(body.decode()))


print('start listening on {}:{}'.format(args.bind, args.port))
httpd = HTTPServer((args.bind, args.port), SimpleHTTPRequestHandler)
httpd.serve_forever()
