import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

addr = ("", 8000)

serv = BaseHTTPServer.HTTPServer(addr, SimpleHTTPRequestHandler)

serv.serve_forever()