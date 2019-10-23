import memory_manager

process_table = dict()

def malloc(sensor_id,team_id):
    global process_table
    new_page = memory_manager.create_page()

    process_table[(sensor_id,team_id)] = ProcessInfo()

    process_table[(sensor_id,team_id)].last_page = new_page
    process_table[(sensor_id,team_id)].page_list.append(new_page)

def save_data(sensor_id, team_id, date, data):
    if (sensor_id,team_id) not in process_table.keys():
        malloc(sensor_id, team_id)

    savedData = "%i{" + str(date) + "} "
    savedData += "%f{" + str(data) + "}"
    write(sensor_id, team_id, savedData)

def write(sensor_id, team_id, data: str):
    offset = process_table[(sensor_id,team_id)].last_byte
    page_id = process_table[(sensor_id,team_id)].last_page
    
    if( offset + len(data.encode("utf8")) >= memory_manager.PAGE_SIZE):
        page_id = memory_manager.create_page()
        offset = 0
        process_table[(sensor_id,team_id)].last_page = page_id
        process_table[(sensor_id,team_id)].page_list.append(page_id)
        process_table[(sensor_id,team_id)].last_byte = 0   
    
    memory_manager.write(page_id, data)
    process_table[(sensor_id,team_id)].last_byte += len(data.encode("utf8"))


def read(sensor_id, team_id):
    if (sensor_id,team_id) in process_table.keys():
        page_list = process_table[(sensor_id,team_id)].page_list
        return interpret_data(sensor_id, team_id, memory_manager.get_pages(page_list))
    else:
        return []
    
def interpret_data(sensor_id, team_id, page_data_list):
    data_list = []
    isInteger = True
    for page in page_data_list:
        for data in page:
            sensor_data = data

            
            if(isInteger):
                dataPair = [sensor_data]
                data_list.append(dataPair)
                isInteger = False
            else:
                data_list[-1].append(sensor_data)
                isInteger = True

    return data_list
  

class ProcessInfo():
    def __init__(self, *args, **kwargs):
        self.last_page = None
        self.last_byte = 0
        self.page_list = []
        self.data_size = 8



