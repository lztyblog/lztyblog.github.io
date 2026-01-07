import socket

# ================== CONFIG ==================
PORT = 8000
BUF_SIZE = 1024
# ============================================

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))

    print("Listening on UDP port", PORT)

    # 1) receive output filename
    data, addr = sock.recvfrom(2048)
    output_name = data.decode("ascii").strip()

    # 2) receive number of chunks
    data, addr = sock.recvfrom(2048)
    chunks = int(data.decode("ascii").strip())

    print("Receiving from", addr)
    print("Saving as", output_name)
    print("Chunks:", chunks)

    with open(output_name, "wb") as f:
        for i in range(chunks):
            data, addr = sock.recvfrom(BUF_SIZE + 200)
            f.write(data)

            if i % 200 == 0:
                print("Received chunk", i)

    sock.close()
    print("File received")

if __name__ == "__main__":
    main()
