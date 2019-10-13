from page_location import *
import file_manager

page_location_map = {}
count_page = 0
pages = {}

PAGE_SIZE = 10

# When a page is created, it's located in primary memory. Return the new page number.
def create_page():
    global count_page
    global page_location_map

    page_number = new_page_number()
    page_location_map[page_number] = Page_Location.PRIMARY.value
    pages[page_number] = ""
    return page_number


def new_page_number():
    global count_page

    number = hex(count_page)
    count_page += 1
    return number


# Falta escribir en disco.
def write(page_id, offset, data):
    global pages
    global page_location_map

    new_data = ""

    old_data = get_page_data(page_id)

    # Append data acording offset.
    if(offset > len(old_data)):
        # Fill with spaces when the offset is bigger than the length
        difference = offset - len(old_data)
        new_data = old_data[:len(old_data)] + (' ' * difference) + data
    else:
        # If it needs to overwrite, go ahead.
        new_data = old_data[:offset] + data + old_data[offset + len(data):]

    if(page_location_map[page_id] == Page_Location.PRIMARY.value):
        write_primary(page_id, new_data)
    else:
        write_secondary(page_id, new_data)


def save_page(page_id):
    global pages
    file_manager.save_new_file(page_id, pages[page_id])
    pass

def swap_from_primary_to_secondary(page_id):
    global pages
    global page_location_map

    save_page(page_id)
    del pages[page_id]
    page_location_map[page_id] = Page_Location.SECONDARY

def get_page_size(page_id):
    return len(pages[page_id])

def write_primary(page_id, data):
    global pages

    pages[page_id] = data

    if(get_page_size(page_id) >=  PAGE_SIZE):
        swap_from_primary_to_secondary(page_id)

# Pending if it's correct to do this (write directly on disk)
def write_secondary(page_id, data):
    file_manager.write_file(page_id, data)

def get_page_data(page_id):
    global pages
    global page_location_map

    if(page_id in pages and page_location_map[page_id] == Page_Location.PRIMARY.value):
        return pages[page_id]
    else:
        return file_manager.get_file_data(page_id)

id = create_page()

# Read