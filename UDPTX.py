#!/usr/bin/env python3
# UDPTX.py - very simple UDP file sender

import socket
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 UDPTX.py <dest_ip> <dest_port> <filename>")
        sys.exit(1)

    dest_ip = sys.argv[1]
    dest_port = int(sys.argv[2])
    filename = sys.argv[3]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        f = open(filename, "rb")
    except OSError as e:
        print("Failed to open file:", e)
        sys.exit(1)

    # 每次发一点点，防止太大
    chunk_size = 1024

    while True:
        data = f.read(chunk_size)
        if not data:
            break  # 文件结束
        sock.sendto(data, (dest_ip, dest_port))

    # 我这里没有专门的“结束包”，接收端用超时来停
    f.close()
    sock.close()
    print("Finished sending", filename)

if __name__ == "__main__":
    main()
