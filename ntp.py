

import socket

DELTA_1900_TO_1970 = 2208988800  # seconds between 1900-01-01 and 1970-01-01
UDP_PORT_NTP = 123
MIN_IP_HDR = 20
UDP_HDR = 8

def u16_be(b: bytes) -> int:
    return (b[0] << 8) | b[1]

def u32_be(b: bytes) -> int:
    return (b[0] << 24) | (b[1] << 16) | (b[2] << 8) | b[3]

def ip_to_str(b: bytes) -> str:
    return ".".join(str(x) for x in b)

def parse_ipv4_udp(pkt: bytes):
    """Return (src_ip, dst_ip, udp_off, udp_len) or None if not IPv4/UDP."""
    if len(pkt) < MIN_IP_HDR:
        return None
    v_ihl = pkt[0]
    version = (v_ihl >> 4) & 0xF
    ihl = (v_ihl & 0xF) * 4
    if version != 4 or ihl < MIN_IP_HDR or len(pkt) < ihl + UDP_HDR:
        return None

    # Protocol 17 = UDP
    proto = pkt[9]
    if proto != 17:
        return None

    total_len = u16_be(pkt[2:4])  # may be shorter than recv buffer
    # clamp to actual
    total_len = min(total_len, len(pkt))

    src_ip = ip_to_str(pkt[12:16])
    dst_ip = ip_to_str(pkt[16:20])

    # UDP header begins right after IP header
    udp_off = ihl
    if total_len < udp_off + UDP_HDR:
        return None

    udp_len = u16_be(pkt[udp_off + 4: udp_off + 6])
    # minimal sanity
    if udp_len < UDP_HDR or total_len < udp_off + udp_len:
        return None

    return (src_ip, dst_ip, udp_off, udp_len)

def parse_ntp_payload(udp_payload: bytes):
    """
    Expect at least 48 bytes. Return dict with raw/derived time if looks like NTP.
    NTP first byte: LI(2) VN(3) Mode(3). Broadcast should have Mode=5.
    """
    if len(udp_payload) < 48:
        return None
    b0 = udp_payload[0]
    li   = (b0 >> 6) & 0b11
    vn   = (b0 >> 3) & 0b111
    mode =  b0       & 0b111

    # Transmit Timestamp at bytes 40..47 (sec, frac)
    sec = u32_be(udp_payload[40:44])
    frac = u32_be(udp_payload[44:48])

    unix_sec = sec - DELTA_1900_TO_1970
    unix_frac = frac / float(1 << 32)

    return {
        "li": li, "vn": vn, "mode": mode,
        "ntp_sec": sec, "ntp_frac": frac,
        "unix_sec": unix_sec, "unix_frac": unix_frac,
    }

def main():
    # Raw IPv4 socket receiving UDP packets (requires sudo)
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    # No bind needed; kernel will deliver UDP datagrams (incl. broadcast) to this raw socket.

    print("Sniffing UDP (raw) for NTP on Linux…  (Ctrl+C to stop)")
    try:
        while True:
            pkt, addr = s.recvfrom(4096)  # addr is (ip, 0), but we parse IP header anyway
            parsed = parse_ipv4_udp(pkt)
            if not parsed:
                continue
            src_ip, dst_ip, udp_off, udp_len = parsed

            # UDP header fields
            sport = u16_be(pkt[udp_off:udp_off+2])
            dport = u16_be(pkt[udp_off+2:udp_off+4])
            if dport != UDP_PORT_NTP:
                continue

            payload_off = udp_off + UDP_HDR
            payload_end = payload_off + (udp_len - UDP_HDR)
            if payload_end > len(pkt):
                continue
            payload = pkt[payload_off:payload_end]

            ntp = parse_ntp_payload(payload)
            if not ntp:
                continue
            if ntp["mode"] != 5:
                continue

            ns = ntp["ntp_sec"]; nf = ntp["ntp_frac"]
            us = ntp["unix_sec"]; uf = ntp["unix_frac"]
            print(
                f"{src_ip} → {dst_ip}  UDP/{dport}  VN={ntp['vn']} Mode={ntp['mode']}\n"
                f"  Tx(NTP): seconds={ns} (0x{ns:08x}), fraction={nf} (0x{nf:08x})\n"
                f"  → Unix:  {us} + {uf:.9f} s"
            )
    except KeyboardInterrupt:
        pass
    finally:
        try:
            s.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
