import queue
import socket
import struct
import threading

import ID_ID
import ID_ML
import ID_NM


def main():

    id_ml_start = queue.Queue()
    id_nm_start = queue.Queue()

    ID_ID_process = threading.Thread(target=ID_ID.start, args=(id_ml_start, id_nm_start))
    ID_ML_process = threading.Thread(target=ID_ML.start, args=(id_ml_start,))
    ID_NM_process = threading.Thread(target=ID_NM.start, args=(id_nm_start,))

    ID_ID_process.start()
    ID_ML_process.start()
    ID_NM_process.start()

    ID_ID_process.join()
    ID_ML_process.join()
    ID_NM_process.join()


main()
