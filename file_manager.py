import os.path

def save_data(date, team_id, sensor_id, sensor_type, data_packet):

    file = open("404.txt", "a+")

    file.write("Date and time: " + date + " - Team id: " + team_id + " - Sensor id: " + sensor_id + " - Sensor type: " + sensor_type
               + " - Data: " + data_packet + "\n")
    file.close()