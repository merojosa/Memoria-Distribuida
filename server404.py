import socket
import struct
import packet_builder
import datetime
import file_manager

UDP_IP = "10.1.137.67"
UDP_PORT = 5000

sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)    # Buffer size is 1024 bytes
    print ("Received message: ")
    packet = struct.unpack(packet_builder.FORMAT, data)

    sequence = packet[0]
    date = datetime.datetime.fromtimestamp(packet[1])
    team_id = packet[2]
    sensor_id = int.from_bytes(packet[3], "big")
    sensor_type = packet[4]
    data_packet = packet[5]

    print(packet)
    file_manager.save_data(date, team_id, sensor_id, sensor_type, data_packet)
