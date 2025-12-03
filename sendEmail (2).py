# sendEmail.py
# Send a simple SMTP email to Pi-3 using only socket.

import socket

PI3_IP = "192.168.X.3"   # ← 换成 Pi-3 的实际地址
PORT = 25

def send(sock, msg):
    sock.sendall((msg + "\r\n").encode())

def recv(sock):
    return sock.recv(1024).decode()

s = socket.socket()
s.connect((PI3_IP, PORT))

print(recv(s))                     # 220 greeting
send(s, "HELO pc")
print(recv(s))

send(s, "MAIL FROM:<pc@test>")
print(recv(s))

send(s, "RCPT TO:<deskX@raspberrypi-mail.server>")
print(recv(s))

send(s, "DATA")
print(recv(s))

send(s, "Subject: test via Pi-3")
send(s, "")
send(s, "This email is sent from the PC.")
send(s, ".")
print(recv(s))

send(s, "QUIT")
print(recv(s))

s.close()
