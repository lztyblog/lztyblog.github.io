import socket
import os
import time

# ================== CONFIG ==================
PI1_IP = "192.168.51.1"      # Pi-1 IP address
PORT = 8000                 # UDP port (must match nc + receiver)
INPUT_FILE = "bob.jpg"      # file to send
OUTPUT_NAME = "bob-copy.jpg"
BUF_SIZE = 1024
# ============================================

def main():
    if not os.path.isfile(INPUT_FILE):
        print("File not found:", INPUT_FILE)
        return

    file_size = os.path.getsize(INPUT_FILE)
    chunks = (file_size + BUF_SIZE - 1) // BUF_SIZE

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Sending to", PI1_IP, "port", PORT)
    print("Chunks:", chunks)

    # 1) send output filename
    sock.sendto(OUTPUT_NAME.encode("ascii"), (PI1_IP, PORT))
    time.sleep(0.05)

    # 2) send number of chunks
    sock.sendto(str(chunks).encode("ascii"), (PI1_IP, PORT))
    time.sleep(0.05)

    # 3) send data
    with open(INPUT_FILE, "rb") as f:
        for i in range(chunks):
            data = f.read(BUF_SIZE)
            sock.sendto(data, (PI1_IP, PORT))
            time.sleep(0.001)

            if i % 200 == 0:
                print("Sent chunk", i)

    sock.close()
    print("Send complete")

if __name__ == "__main__":
    main()
