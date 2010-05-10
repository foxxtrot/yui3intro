def getNextPageNumber(page_number, total_items, page_length):
    if (total_items % page_length == 0 and page_number < total_items / page_length) or (total_items % page_length != 0 and page_number <= total_items / page_length):
        return page_number + 1
    else:
	return None

def getPrevPageNumber(page_number):
    if page_number > 1:
        return page_number - 1
    else:
        return None
