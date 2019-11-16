import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import memory_manager

def send_packet_interface():

    id1 = memory_manager.create_page()
    id2 = memory_manager.create_page()


    memory_manager.write(id2, '%i{40}')
    memory_manager.write(id2, '%f{1.5}')

    memory_manager.INTERFACE_IP = '127.0.0.1'
    memory_manager.INTERFACE_PORT = 2000

    memory_manager.save_page(id2)

    print('send_packet_interface OK')

send_packet_interface()