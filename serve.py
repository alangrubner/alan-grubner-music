import os, re, http.server, socketserver

class RangeHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        try:
            f = open(path, 'rb')
        except OSError:
            return super().send_head()

        try:
            file_size = os.fstat(f.fileno()).st_size
        except Exception:
            f.close()
            return super().send_head()

        range_header = self.headers.get('Range')
        if range_header:
            m = re.match(r'bytes=(\d+)-(\d*)', range_header)
            if m:
                start = int(m.group(1))
                end = int(m.group(2)) if m.group(2) else file_size - 1
                end = min(end, file_size - 1)
                length = end - start + 1
                f.seek(start)
                ctype = self.guess_type(path)
                self.send_response(206)
                self.send_header('Content-type', ctype)
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.send_header('Content-Length', str(length))
                self.send_header('Accept-Ranges', 'bytes')
                self.end_headers()
                return f

        f.close()
        return super().send_head()

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

os.chdir("/Users/alangrubner/Documents/alan_grubner_music_site")
with ThreadedServer(("", 8888), RangeHandler) as httpd:
    httpd.serve_forever()
