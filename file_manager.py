import data_detector

def save_data(date, team_id, sensor_id, sensor_type, data_packet):

    name_file = data_detector.detect_team(team_id)

    if( name_file != None ):                    # If there is no error.
        file = open(name_file + ".txt", "a+")

        file.write("Date and time: " + str(date) + " - Team id: " + str(team_id) + " - Sensor id: " + str(sensor_id) + " - Sensor type: " + str(sensor_type)
                   + " - Data: " + str(data_packet) + "\n")
        file.close()

    else:
        print("team_id no reconocido: " + team_id )