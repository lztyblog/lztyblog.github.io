#!/usr/bin/env python3
# UDPRX.py - very simple UDP file receiver

import socket
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 UDPRX.py <listen_port> <output_file>")
        sys.exit(1)

    listen_port = int(sys.argv[1])
    output_file = sys.argv[2]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", listen_port))
    # 如果一段时间没有收到数据，就退出循环
    sock.settimeout(5.0)  # 秒，可以自己调

    try:
        f = open(output_file, "wb")
    except OSError as e:
        print("Cannot open output file:", e)
        sys.exit(1)

    print("Listening on UDP port", listen_port)

    while True:
        try:
            data, addr = sock.recvfrom(2048)
        except socket.timeout:
            # 认为发送端已经发完
            break

        if not data:
            # 通常不会收到空数据，这里只是防御式写法
            break

        f.write(data)

    f.close()
    sock.close()
    print("Finished receiving, saved as", output_file)

if __name__ == "__main__":
    main()
