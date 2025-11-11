import socket

NTP_PORT = 123
NTP_UNIX_EPOCH_DELTA = 2208988800  # seconds between 1900-01-01 and 1970-01-01

def parse_ntp(pkt: bytes):
    """
    Parse minimal NTP header fields we need.
    NTP v4 header >= 48 bytes. Transmit Timestamp at bytes [40:48].
    """
    if len(pkt) < 48:
        return None

    # First byte: LI (2b), VN (3b), Mode (3b)
    b0 = pkt[0]
    li    = (b0 >> 6) & 0x3
    vn    = (b0 >> 3) & 0x7
    mode  =  b0       & 0x7

    stratum = pkt[1]
    poll    = pkt[2]
    # precision = pkt[3]  # signed, not needed for this task

    # Transmit Timestamp (64-bit): seconds (40..43), fraction (44..47)
    ntp_secs = int.from_bytes(pkt[40:44], 'big', signed=False)
    ntp_frac = int.from_bytes(pkt[44:48], 'big', signed=False)

    # Convert to Unix seconds (integer part). Fraction kept separately.
    unix_secs = ntp_secs - NTP_UNIX_EPOCH_DELTA
    unix_frac = ntp_frac / (1 << 32)  # fractional seconds in [0,1)

    return {
        "li": li, "vn": vn, "mode": mode,
        "stratum": stratum, "poll": poll,
        "ntp_seconds": ntp_secs, "ntp_fraction": ntp_frac,
        "unix_seconds": unix_secs, "unix_fractional": unix_frac,
    }

def main():
    # Create UDP socket and bind to port 123 to receive broadcast.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Allow reuse (helps if ntpd also binds; may require SO_REUSEPORT on your image)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except OSError:
            pass

    # Bind to all interfaces on UDP/123 (requires sudo/root).
    sock.bind(("", NTP_PORT))

    print("Listening on UDP/123 for NTP broadcast ...  (Ctrl+C to stop)")
    while True:
        pkt, addr = sock.recvfrom(2048)
        info = parse_ntp(pkt)
        if not info:
            continue

        # Pretty print with raw hex for "show working" in the report
        ntp_secs_hex = f"0x{info['ntp_seconds']:08x}"
        ntp_frac_hex = f"0x{info['ntp_fraction']:08x}"

        print(
            f"from {addr[0]}  VN={info['vn']} Mode={info['mode']} Stratum={info['stratum']} Poll={info['poll']}\n"
            f"  TxTimestamp (NTP):  seconds={info['ntp_seconds']} ({ntp_secs_hex}), "
            f"fraction={info['ntp_fraction']} ({ntp_frac_hex})\n"
            f"  => Unix time: {info['unix_seconds']} + {info['unix_fractional']:.9f} s"
        )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
