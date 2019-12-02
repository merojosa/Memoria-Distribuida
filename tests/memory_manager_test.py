import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import memory_manager

def send_packet_interface():

    id0 = memory_manager.create_page()


    memory_manager.write(id0, '%i{40}')
    memory_manager.write(id0, '%f{1.5}')
    
    memory_manager.save_page(id0)

   # data = memory_manager.get_page_data(id0)

    print('send_packet_interface OK')

    print("Datos obtenidos ", end="")
   # print(data)


send_packet_interface()
