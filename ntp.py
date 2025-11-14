#!/usr/bin/env python3
# ntp.py - small NTP broadcast listener for Pi-3
# Only uses the socket module.

import socket

NTP_PORT = 123
NTP_DELTA = 2208988800  # seconds between 1900-01-01 and 1970-01-01
BUF_SIZE = 1024


def bytes_to_u32(chunk):
    """Convert 4 bytes (big-endian) to an unsigned 32-bit integer."""
    return ((chunk[0] << 24) |
            (chunk[1] << 16) |
            (chunk[2] << 8)  |
            chunk[3])


def parse_ntp_packet(packet):
    """
    Very small NTP parser:
    - require at least 48 bytes
    - read version + mode from first byte
    - read Transmit Timestamp seconds/fraction from bytes 40..47
    """
    if len(packet) < 48:
        return None

    first = packet[0]
    version = (first >> 3) & 0x07
    mode = first & 0x07

    # Transmit Timestamp (offset 40 bytes from start of NTP header)
    ntp_sec = bytes_to_u32(packet[40:44])
    ntp_frac = bytes_to_u32(packet[44:48])

    unix_sec = ntp_sec - NTP_DELTA
    unix_frac = ntp_frac / float(1 << 32)

    return {
        "version": version,
        "mode": mode,
        "ntp_sec": ntp_sec,
        "ntp_frac": ntp_frac,
        "unix_sec": unix_sec,
        "unix_frac": unix_frac,
    }


def main():
    # UDP socket on port 123; Pi-3 listens for NTP (including broadcast) here.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind(("", NTP_PORT))
    except OSError as e:
        print("Cannot bind to UDP port 123:", e)
        print("Hint: make sure you run this on Pi-3 with python3, and")
        print("      that you have permission (use: sudo python3 ntp.py).")
        return

    print("Listening on UDP/123 for NTP packets (Ctrl+C to stop)...")

    try:
        while True:
            data, addr = sock.recvfrom(BUF_SIZE)
            info = parse_ntp_packet(data)
            if info is None:
                continue

            # If你只想看广播包，可以过滤 mode != 5
            # 题目是 broadcast from Pi-1，所以这里一般 mode 应该是 5
            # 可以保留这个判断，也可以注释掉看所有 NTP 包
            # if info["mode"] != 5:
            #     continue

            print("From {0}".format(addr[0]))
            print("  Version: {0}, Mode: {1}".format(info["version"], info["mode"]))
            print("  NTP seconds : {0} (0x{0:08x})".format(info["ntp_sec"]))
            print("  NTP fraction: {0} (0x{0:08x})".format(info["ntp_frac"]))
            print("  Unix time   : {0} + {1:.9f} s".format(
                info["unix_sec"], info["unix_frac"]))
            print("")
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()


if __name__ == "__main__":
    main()
