import socket
import os
import time

UDP_IP = "192.168.68.1"
UDP_PORT = 8000
BUF_SIZE = 1024

sockTX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  

read_file_name="bob.jpg"
write_file_name="bob-copy.jpg"
file_size = os.path.getsize(read_file_name)
number_of_segments = (-(-file_size//BUF_SIZE))

sockTX.sendto(write_file_name.encode("ascii"), (UDP_IP, UDP_PORT))
time.sleep(0.1)
sockTX.sendto(str(number_of_segments).encode("ascii"), (UDP_IP, UDP_PORT))
time.sleep(0.1)

print("Sending: " + read_file_name + ":" + str(number_of_segments))

f=open(read_file_name,"rb")
data = f.read(BUF_SIZE)

for i in range(0,number_of_segments):
  sockTX.sendto(data, (UDP_IP, UDP_PORT))
  time.sleep(0.1)
  print("tx segment: " + str(i) + " len: " + str(len(data)))
  data = f.read(BUF_SIZE)

sockTX.close()
f.close()

