import threading
from datetime import *
import queue
import socket
import time
import struct
import packet_builders.local_distributed_packet_builder as local_packet_builder
from enum_operation_code import Operation_Code

node_id = 0
max_size = 3000000
size_left = 0
metadata_pos = 0
data_pos = max_size
byte_table = []
page_list = []
count_node = 0

def set_id():
    global count_node
    node_id = generate_node_id()
    return node_id


def generate_node_id():
    global count_node

    id = hex(count_node)
    count_node += 1
    return id


def save_page(id, page_size, content, dateMod):
    global size_left
    added_page = PageData()
    added_page.page_id = id
    added_page.date_modification = dateMod
    added_page.page_size = page_size
    added_page.content = content
    page_list.append(added_page)
    size_left += added_page.page_size
    return size_left


def getPageContent(id):
    for page in page_list:
        if(page.page_id == id):
            return page.content
    return 

def getDateModification(id):
    for page in page_list:
        if(page.page_id == id):
            return page.date_modification
    return 

def getDateBirth():
    for page in page_list:
        if(page.page_id == id):
            return page.date_birth
    return 

def getPageSize():
    for page in page_list:
        if(page.page_id == id):
            return page.size_left
    return 

class PageData():
    def __init__(self, *args, **kwargs):
        self.page_id = 0
        self.page_size = 0
        self.content = []
        self.date_birth = datetime.now()
        self.date_modification = datetime.now()


print(save_page(set_id(),8,'wew',datetime.now()))
print(save_page(set_id(),8,'png',datetime.now()))
print(getPageContent('0x0'))
print(getPageContent('0x1'))