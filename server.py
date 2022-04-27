import http.server
import socketserver
import os
PORT = 8000

handler = http.server.SimpleHTTPRequestHandler
handler.extensions_map.update({
    ".js": "application/javascript",
})
os.chdir("dist")
httpd = socketserver.TCPServer(("", PORT), handler)
httpd.serve_forever()