import socket
import struct
import packet_builder

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

packet = packet_builder.create(team_id=5, sensor_id="001",  sensor_type=0,  data=25.3)

print ("UDP target IP: " + str(UDP_IP))
print ("UDP target port: " + str(UDP_PORT))
print ("Packet: " + str(struct.unpack(packet_builder.FORMAT, packet)))










sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(packet, (UDP_IP, UDP_PORT))
