import os, http.server, socketserver

os.chdir("/Users/alangrubner/Documents/alan_grubner_music_site")
handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", 8888), handler) as httpd:
    httpd.serve_forever()
