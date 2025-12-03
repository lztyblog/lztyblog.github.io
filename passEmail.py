import socket

LISTEN_PORT = 25
LAB_SERVER = "raspberrypi-mail.lan"
LAB_PORT = 25

def send(sock, msg):
    sock.sendall((msg + "\r\n").encode())

def recv(sock):
    return sock.recv(1024).decode()

# --- Accept email from PC ---
srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("", LISTEN_PORT))
srv.listen(1)

c, addr = srv.accept()
send(c, "220 Pi-3 ready")

mail_from = ""
rcpt_to = ""
body = []
in_data = False

while True:
    line = recv(c)
    if not line:
        break
    text = line.strip()

    if in_data:
        if text == ".":
            send(c, "250 OK")
            break
        body.append(text)
        continue

    up = text.upper()
    if up.startswith("HELO"):
        send(c, "250 Hello")
    elif up.startswith("MAIL FROM"):
        mail_from = text
        send(c, "250 OK")
    elif up.startswith("RCPT TO"):
        rcpt_to = text
        send(c, "250 OK")
    elif up == "DATA":
        send(c, "354 End with '.'")
        in_data = True

c.close()
srv.close()

# --- Forward to lab mail server ---
s = socket.socket()
s.connect((LAB_SERVER, LAB_PORT))
recv(s)

send(s, "HELO pi3")
recv(s)

send(s, mail_from)
recv(s)

send(s, rcpt_to)
recv(s)

send(s, "DATA")
recv(s)

send(s, "Subject: relayed")
send(s, "")
for l in body:
    send(s, l)
send(s, ".")
recv(s)

send(s, "QUIT")
s.close()
