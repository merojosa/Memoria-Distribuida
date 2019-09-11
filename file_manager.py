
def save_data(date, team_id, sensor_id, sensor_type, data_packet):
    # Create or open the file.
    file = open("404.txt", "w+")
    file.write("Date and time: " + date + " - Team id: " + team_id + " - Sensor id: " + sensor_id + " - Sensor type: " + sensor_type
               + " - Data: " + data_packet)
    file.close()