from page_location import *
import file_manager
import re

page_location_map = {}
count_page = 0
pages = {}

FLOAT_SIZE = 4
PAGE_SIZE = 12

# When a page is created, it's located in primary memory. Return the new page id.
def create_page():
    global count_page
    global page_location_map

    page_id = new_page_id()
    page_location_map[page_id] = Page_Location.PRIMARY.value
    pages[page_id] = PageInfo()
    return page_id


def new_page_id():
    global count_page

    id = hex(count_page)
    count_page += 1
    return id


def write(page_id, data_interface):
    global pages
    global page_location_map

    # Iterate every word with the format %ONE_LETTER{NUMBERS OR LETTERS}.
    # Omits if there are spaces between ONE_LETTER and {NUMBERS OR LETTERS}
    for expression in re.findall(r"%\w{[\w0-9\.]+}", data_interface):
        data_type = expression[1]
        single_data = expression[3:len(expression) - 1]

        if(data_type == 'f' or data_type == 'i'):
            single_data_size = FLOAT_SIZE
        else:
            raise Exception('Tipo de dato desconocido: ' + data_type)
            
        if(page_location_map[page_id] == Page_Location.PRIMARY.value):
                write_primary(page_id, single_data, single_data_size)
        else:
            swap_from_secondary_to_primary(page_id)
            write_primary(page_id, single_data, single_data_size)

def save_page(page_id):
    global pages
    file_manager.save_object("pages/", page_id + ".page404", pages[page_id])
    pass


def swap_from_primary_to_secondary(page_id):
    global pages
    global page_location_map

    save_page(page_id)
    del pages[page_id]
    page_location_map[page_id] = Page_Location.SECONDARY.value


def swap_from_secondary_to_primary(page_id):
    global pages
    global page_location_map

    pages[page_id] = get_page_data(page_id)
    file_manager.delete_file("pages/" + page_id + ".page404")
    page_location_map[page_id] = Page_Location.PRIMARY.value



def write_primary(page_id, data, size):
    global pages

    pages[page_id].content.append(data)
    pages[page_id].current_size += size

    if(pages[page_id].current_size >=  PAGE_SIZE):
        swap_from_primary_to_secondary(page_id)


def get_page_data(page_id):
    global pages
    global page_location_map

    if(page_location_map[page_id] == Page_Location.PRIMARY.value):
        return pages[page_id].content
    else:
        return file_manager.get_object("pages/" + page_id + ".page404").content


def get_pages(page_id_list):

    page_content_list = []

    for id in page_id_list:
        page_content_list.append(get_page_data(id))

    return page_content_list


class PageInfo():
    def __init__(self, *args, **kwargs):
        self.current_size = 0
        self.content = []