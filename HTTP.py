# q2a_head_request.py
# A simple Python script to send an HTTP HEAD request
# Use this for Wireshark capture (e.g., to Pi-3 web server)

import http.client

def send_head_request(host, port=80, path="/"):
    # 建立HTTP连接
    connection = http.client.HTTPConnection(host, port)
    print(f"[*] Connecting to {host}:{port}")
    
    # 发送HEAD请求
    connection.request("HEAD", path)
    print(f"[*] Sent HEAD request to {path}")

    # 接收响应
    response = connection.getresponse()
    print("[*] Response status:", response.status, response.reason)
    print("[*] Response headers:")
    
    for header, value in response.getheaders():
        print(f"  {header}: {value}")
    
    # 关闭连接
    connection.close()
    print("[*] Connection closed.")

if __name__ == "__main__":
    # 修改成你的 Pi-3 的 IP 地址或主机名
    target_host = "192.168.13.3"   # 示例，可换为你的 Pi-3 地址
    send_head_request(target_host)
