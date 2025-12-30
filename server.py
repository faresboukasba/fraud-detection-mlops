#!/usr/bin/env python3
"""
Simple HTTP Server for Fraud Detection UI
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        return super().end_headers()
    
    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return super().do_GET()

if __name__ == '__main__':
    os.chdir('/app')
    server = HTTPServer(('0.0.0.0', 8501), MyHTTPRequestHandler)
    print('Server started on http://0.0.0.0:8501')
    server.serve_forever()
