from page_location import *
import file_manager

page_map = {}
count_page = 0
pages = {}

PAGE_SIZE = 10

# When a page is created, it's located in primary memory. Return the new page number.
def create_page():
    global count_page
    global page_map

    page_number = new_page_number()
    page_map[page_number] = Page_Location.PRIMARY.value
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

    if(page_id in pages):

        old_data = pages[page_id]

        # Append data acording offset.

        if(offset > len(old_data)):
            # Fill with spaces when the offset is bigger than the length
            difference = offset - len(old_data)
            pages[page_id] = old_data[:len(old_data)] + (' ' * difference) + data
        else:
            # If it needs to overwrite, go ahead.
            pages[page_id] = old_data[:offset] + data + old_data[offset + len(data):]

        if(get_page_size(page_id) >=  PAGE_SIZE):
            swap_from_primary_to_secondary(page_id)

    else:
        print("Error: la página " + str(page_id) + " no existe.")

def save_page(page_id):
    file_manager.save_new_file(page_id, pages[page_id])
    pass

def swap_from_primary_to_secondary(page_id):
    global pages

    save_page(page_id)
    del pages[page_id]

def get_page_size(page_id):
    return len(pages[page_id])

# Read