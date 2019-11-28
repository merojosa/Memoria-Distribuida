import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import memory_manager

def send_packet_interface():

    id1 = memory_manager.create_page()
    id2 = memory_manager.create_page()

    
    memory_manager.write(id2, '%i{40}')
    memory_manager.write(id2, '%f{1.5}')
    memory_manager.write(id1, '%f{77}')
    
    memory_manager.swap_from_primary_to_secondary(id2)
    memory_manager.swap_from_primary_to_secondary(id1)

    data = memory_manager.get_page_data(id2)

    print('send_packet_interface OK')

    print("Datos obtenidos ", end="")
    print(data)


send_packet_interface()
