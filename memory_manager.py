from page_location import *

page_map = {}
count_page = 0
pages = {}

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


def write(page_number, offset, data):

    if(page_number in pages):

        old_data = pages[page_number]

        # Append data acording offset.

        if(offset > len(old_data)):
            # Fill with spaces when the offset is bigger than the length
            difference = offset - len(old_data)
            pages[page_number] = old_data[:len(old_data)] + (' ' * difference) + data
        else:
            # If it needs to overwrite, go ahead.
            pages[page_number] = old_data[:offset] + data + old_data[offset + len(data):]

    else:
        print("Error: la página " + str(page_number) + " no existe.")


# Read