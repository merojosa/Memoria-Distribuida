import memory_manager

process_table = dict()

def malloc(sensor_id,team_id):
    global process_table
    new_page = memory_manager.create_page()

    #if not process_table[(sensor_id,team_id)]:
    process_table[(sensor_id,team_id)] = ProcessInfo()

    process_table[(sensor_id,team_id)].last_page = new_page
    process_table[(sensor_id,team_id)].page_list.append(new_page)


def write(sensor_id, team_id, data: str):
    offset = process_table[(sensor_id,team_id)].last_byte
    page_id = process_table[(sensor_id,team_id)].last_page

    if( offset + len(data.encode("utf8")) >= memory_manager.PAGE_SIZE):
        page_id = memory_manager.create_page()
        offset = 0
        process_table[(sensor_id,team_id)].last_page = page_id
        process_table[(sensor_id,team_id)].page_list.append(page_id)
        process_table[(sensor_id,team_id)].last_byte = 0   
    
    memory_manager.write(page_id, offset, data)
    process_table[(sensor_id,team_id)].last_byte += len(data.encode("utf8"))


def read(sensor_id, team_id):
    page_list = process_table[(sensor_id,team_id)].page_list
    return memory_manager.get_pages(page_list)


#Work in progress, needs case when is picking empty space
def interpret_data(sensor_id, team_id, page_data_list):
    data_list = []
    sensor_data = ""
    data_iter = 0
    for data in page_data_list:
        sensor_data += data
        if data_iter >= process_table[(sensor_id,team_id)].data_size:
            data_list.append(sensor_data)
            sensor_data = ""
            data_iter = 0
    return data_list
  

class ProcessInfo():
    def __init__(self, *args, **kwargs):
        self.last_page = None
        self.last_byte = 0
        self.page_list = []
        self.data_size = 0
