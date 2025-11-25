import socket
import sys

def run():
    if len(sys.argv) != 3:
        print("usage: python3 q6d-congestion.py <ip> <port>")
        return

    ip = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except:
        print("port must be int")
        return

    # you can change these to larger values after confirming it works
    total_bytes = 3 * 1024 * 1024     # about 3MB first test
    block = 4096                      # send block
    data = b"x" * block               # simple payload

    try:
        s = socket.socket()
    except Exception as e:
        print("socket error:", e)
        return

    try:
        s.connect((ip, port))
    except Exception as e:
        print("connect failed:", e)
        s.close()
        return

    sent = 0
    try:
        while sent < total_bytes:
            try:
                n = s.send(data)
                if n <= 0:
                    print("remote closed")
                    break
                sent += n
            except Exception as e:
                print("send error:", e)
                break
    except KeyboardInterrupt:
        print("stopped by user")

    print("sent:", sent, "bytes")
    try:
        s.close()
    except:
        pass

if __name__ == "__main__":
    run()
