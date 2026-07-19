import socket, os

DIR = os.path.dirname(__file__)

def handle(conn):
    try:
        req = conn.recv(4096).decode('utf-8', errors='ignore')
        path = '/index.html' if 'GET / ' in req else req.split(' ')[1] if 'GET ' in req else '/'
        fpath = os.path.join(DIR, path.lstrip('/'))
        if os.path.isfile(fpath) and fpath.startswith(DIR):
            body = open(fpath).read()
            ct = 'text/html; charset=utf-8' if fpath.endswith('.html') else 'text/plain'
            resp = f"HTTP/1.1 200 OK\r\nContent-Type: {ct}\r\nContent-Length: {len(body.encode('utf-8'))}\r\nConnection: close\r\n\r\n{body}"
        else:
            resp = "HTTP/1.1 404\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        conn.send(resp.encode('utf-8'))
    except: pass
    finally: conn.close()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9010))
s.listen(5)
print("ok")
while True:
    c, _ = s.accept()
    handle(c)
