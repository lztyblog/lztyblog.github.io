import socket
from PIL import Image

UDP_IP = "192.168.82.2"
UDP_PORT = 8080
BUF_SIZE = 60000

sockRX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sockRX.bind((UDP_IP, UDP_PORT))

data,addr = sockRX.recvfrom(BUF_SIZE)
file_name = data.strip()

data,addr = sockRX.recvfrom(BUF_SIZE)
number_of_segments = int(data)

print("RX File: {0}".format(file_name))

f = open(file_name,'wb')

try:
  for i in range(0,number_of_segments):
    sockRX.settimeout(2)
    data,addr = sockRX.recvfrom(BUF_SIZE)
    f.write(data)
    print("rx segment: " + str(i))
  print("Download complete")
  f.close()
  sockRX.close()
  image = Image.open(file_name)
  image.show()

except socket.timeout:
  print("Oops timeout")
  f.close()
  sockRX.close()
  

