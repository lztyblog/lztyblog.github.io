#!/usr/bin/env python3
import socket
import os
import sys
import time

# Simple UDP sender for the lab.
# Sends: (1) output filename, (2) number of chunks, (3) raw file data chunks

BUF_SIZE = 1024

def main():
    if len(sys.argv) != 5:
        print("Usage: python3 UDPTX.py <DEST_IP> <DEST_PORT> <INPUT_FILE> <OUTPUT_NAME>")
        print("Example: python3 UDPTX.py 192.168.51.1 8000 bob.jpg bob-copy.jpg")
        sys.exit(1)

    dest_ip = sys.argv[1]
    dest_port = int(sys.argv[2])
    input_file = sys.argv[3]
    output_name = sys.argv[4]

    if not os.path.isfile(input_file):
        print("Error: file not found:", input_file)
        sys.exit(1)

    file_size = os.path.getsize(input_file)
    chunks = (file_size + BUF_SIZE - 1) // BUF_SIZE  # ceil

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 1) send output filename
    sock.sendto(output_name.encode("ascii", errors="ignore"), (dest_ip, dest_port))
    time.sleep(0.05)  # tiny gap so receiver doesn't merge/control weirdly

    # 2) send number of chunks
    sock.sendto(str(chunks).encode("ascii"), (dest_ip, dest_port))
    time.sleep(0.05)

    print("Sending:", input_file)
    print("To:", dest_ip, dest_port)
    print("Output name:", output_name)
    print("Chunks:", chunks, "BUF_SIZE:", BUF_SIZE)

    # 3) send data
    with open(input_file, "rb") as f:
        for i in range(chunks):
            data = f.read(BUF_SIZE)
            if not data:
                break
            sock.sendto(data, (dest_ip, dest_port))

            # small delay helps netcat relays not drop bursts
            time.sleep(0.001)

            if i % 200 == 0:
                print("tx chunk", i)

    sock.close()
    print("Done.")

if __name__ == "__main__":
    main()
