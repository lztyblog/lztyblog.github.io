#!/usr/bin/env python3
import socket
import struct
import time

# NTP uses epoch starting 1900-01-01
# Unix epoch starts 1970-01-01
NTP_UNIX_DELTA = 2208988800

BUF_SIZE = 2048
NTP_PORT = 123
BROADCAST_IP = "192.168.255.255"   # lab network broadcast (/16)

def main():
    # create UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # allow broadcast packets
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind to any free local port (NOT 123)
    s.bind(("0.0.0.0", 0))

    # "connect" to broadcast:123 (UDP connect is only for filtering)
    s.connect((BROADCAST_IP, NTP_PORT))

    print("Listening for broadcast NTP packets...")
    print("Broadcast address:", BROADCAST_IP)
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            data = s.recv(BUF_SIZE)

            # NTP packet must be at least 48 bytes
            if len(data) < 48:
                continue

            # Transmit Timestamp is bytes 40..47
            ntp_sec, ntp_frac = struct.unpack("!II", data[40:48])

            # convert to Unix time
            unix_time = ntp_sec - NTP_UNIX_DELTA
            frac_seconds = ntp_frac / 2**32

            # local receive time (for rough offset idea)
            local_time = time.time()

            print("---- NTP packet ----")
            print("NTP seconds   :", ntp_sec, "(0x%08x)" % ntp_sec)
            print("NTP fraction  :", ntp_frac, "(0x%08x)" % ntp_frac)
            print("Unix time     :", unix_time, "+ %.9f s" % frac_seconds)
            print("Local time    :", local_time)
            print("Local - NTP   :", local_time - (unix_time + frac_seconds))
            print("")

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        s.close()

if __name__ == "__main__":
    main()
