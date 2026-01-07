#!/usr/bin/env python3
import socket
import sys

# Simple UDP receiver for the lab.
# Receives: (1) output filename, (2) number of chunks, (3) raw data chunks

BUF_SIZE = 1024

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 UDPRX.py <LISTEN_PORT>")
        print("Example: python3 UDPRX.py 8000")
        sys.exit(1)

    listen_port = int(sys.argv[1])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # bind to all interfaces, so you don't need to guess your PC IP here
    sock.bind(("", listen_port))

    print("Listening UDP on port", listen_port)

    # 1) get output filename
    data, addr = sock.recvfrom(2048)
    out_name = data.decode("ascii", errors="ignore").strip()
    if not out_name:
        out_name = "output.bin"

    # 2) get number of chunks
    data, addr = sock.recvfrom(2048)
    try:
        chunks = int(data.decode("ascii", errors="ignore").strip())
    except ValueError:
        print("Error: chunk count not a number")
        sock.close()
        sys.exit(1)

    print("From:", addr)
    print("Saving as:", out_name)
    print("Chunks:", chunks, "BUF_SIZE:", BUF_SIZE)

    with open(out_name, "wb") as f:
        for i in range(chunks):
            data, addr = sock.recvfrom(BUF_SIZE + 200)
            f.write(data)

            if i % 200 == 0:
                print("rx chunk", i)

    sock.close()
    print("Saved:", out_name)

if __name__ == "__main__":
    main()
