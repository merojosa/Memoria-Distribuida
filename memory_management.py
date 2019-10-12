from page_location import *

page_map = {}
count_page = 0

# When a page is created, it's located in primary memory. Return the new page number.
def create_page():
    global count_page
    global page_map

    page_number = new_page_number()
    page_map[page_number] = Page_Location.PRIMARY.value
    return page_number


def new_page_number():
    global count_page

    number = hex(count_page)
    count_page += 1
    return number

# Write

# Read