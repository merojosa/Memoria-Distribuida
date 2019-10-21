import memory_manager

process_table = dict()

def malloc(sensor_id,team_id):
    global process_table
    new_page = memory_manager.create_page()

    #if not process_table[(sensor_id,team_id)]:
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
    page_list = process_table[(sensor_id,team_id)].page_list
    return interpret_data(sensor_id, team_id, memory_manager.get_pages(page_list))
    
#Work in progress, needs case when is picking empty space
def interpret_data(sensor_id, team_id, page_data_list):
    data_list = []
    isInteger = True
    for page in page_data_list:
        #sensor_data = ""
        #data_iter = 0
        for data in page:
            sensor_data = data
            #if data_iter >= process_table[(sensor_id,team_id)].data_size:

            if(isInteger):
                stringToAppend = '%i' + sensor_data
                isInteger = False
            else:
                stringToAppend = '%f' + sensor_data
                isInteger = True

            data_list.append(stringToAppend)
                #sensor_data = ""
                #data_iter = 0

    return data_list
  

class ProcessInfo():
    def __init__(self, *args, **kwargs):
        self.last_page = None
        self.last_byte = 0
        self.page_list = []
        self.data_size = 8

sensor = 1
team = 1
date = 4254
data = 1424
date1 = 42543
data1 = 14243
date2 = 42544
data2 = 14244
date3 = 42545
data3 = 14245
date4 = 42546
data4 = 14246
#pList = [[123],[12],[311],[123]]
save_data(sensor,team, date,data)
save_data(sensor,team, date1,data1)
save_data(sensor,team, date2,data2)
save_data(sensor,team, date3,data3)
save_data(sensor,team, date4,data4)
#interpret_data(sensor, team, pList)
print(read(sensor, team))

