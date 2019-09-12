import socket
import struct
import ack_builder
import datetime
import file_manager
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

packetMov = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x03',  sensor_type=0,  data=25.3)
packetTemp = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x03',  sensor_type=0,  data=25.3)
packetHum =packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x03',  sensor_type=0,  data=25.3)

print ("UDP target IP: " + str(UDP_IP))
print ("UDP target port: " + str(UDP_PORT))
print ("PacketMov: " + str(struct.unpack(packet_builder.FORMAT, packetMov)))
print ("PacketTemp: " + str(struct.unpack(packet_builder.FORMAT, packetTemp)))
print ("PacketHum: " + str(struct.unpack(packet_builder.FORMAT, packetHum)))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


while(true):
  sock.sendto(packetMov, (UDP_IP, UDP_PORT))
  sock.sendto(packetTemp, (UDP_IP, UDP_PORT))
  sock.sendto(packetHum, (UDP_IP, UDP_PORT))
  time.sleep(1)
  
  #data, addr = sock.recvfrom(1024)    # Buffer size is 1024 bytes
  #print ("ACK: ")
  #packet = struct.unpack(ack_builder.FORMAT, data)

  #sequence = str(packet[0])
  #date = str(datetime.datetime.fromtimestamp(packet[1]))
  #team_id = str(packet[2])
  #sensor_id = str(int.from_bytes(packet[3], "big"))
  #sensor_type = str(packet[4])
  
  #print(sequence + ' ' + date + ' ' + team_id + ' ' + sensor_id + ' ' + sensor_type)

