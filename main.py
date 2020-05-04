#! /usr/bin/env python3
import argparse
from termcolor import colored
from http.server import HTTPServer, BaseHTTPRequestHandler

banner = '''
             _   _                              __ _ _ _             _   _                                            
            | | | |                            / _(_) | |           | | (_)                                           
 _ __  _   _| |_| |__   ___  _ __     _____  _| |_ _| | |_ _ __ __ _| |_ _  ___  _ __    ___  ___ _ ____   _____ _ __ 
| '_ \| | | | __| '_ \ / _ \| '_ \   / _ \ \/ /  _| | | __| '__/ _` | __| |/ _ \| '_ \  / __|/ _ \ '__\ \ / / _ \ '__|
| |_) | |_| | |_| | | | (_) | | | | |  __/>  <| | | | | |_| | | (_| | |_| | (_) | | | | \__ \  __/ |   \ V /  __/ |   
| .__/ \__, |\__|_| |_|\___/|_| |_|  \___/_/\_\_| |_|_|\__|_|  \__,_|\__|_|\___/|_| |_| |___/\___|_|    \_/ \___|_|   
| |     __/ |                                                                                                         
|_|    |___/                                                                                                                                                                                                                                                                                                                 

https://github.com/NeuronAddict/exfiltration-server
'''

print(colored(banner, 'green'))

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
