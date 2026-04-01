# file for redundant code
import re


# creating 2d grid to insert missing columns in HTML
# (to account for rowspan usage in some columns)
def expand_table(table):
    rowspan_counter = {}  # counter for rowspan
    grid = [] # 2d grid

    rows = table.find_all("tr") # rows from table
    for row in rows:
        grid_row = [] # row that goes into the grid
        cells = row.find_all("td") # cols that goes into grid_row
        cell_iter = iter(cells) # col pointer
        col = 0 # init col

        while True:
            if col in rowspan_counter:
                count, cell = rowspan_counter[col]
                grid_row.append(cell) # copy cell
                if count - 1 > 0:
                    rowspan_counter[col] = (count - 1, cell)
                else:
                    del rowspan_counter[col] # col no longer has rowspan
                col += 1
                continue

            cell = next(cell_iter, None) # declare cell
            if cell is None:
                break

            grid_row.append(cell) # add col to grid

            rowspan = int(cell.get("rowspan", 1)) # rowspan num (default 1)
            if rowspan > 1:
                rowspan_counter[col] = (rowspan - 1, cell) # decrement count, store cell to copy

            col += 1


        grid.append(grid_row)

    return grid


# header indices for each table
def get_header_indices(table):
    headers = [th.get_text(strip=True).lower() for th in table.find("tr").find_all("th")] # list of all col names
    return {header : index for index, header in enumerate(headers)} # ret {col name : index}

# location parser for complicated cell blocks
def parse_locations(cell):
    locations = set() # multiple locations
    curr_loc = [] # to account for different tag types for each location

    for child in cell.children:
        if child.name == "a":
            a_text = child.get_text(strip=True)
            if a_text:
                curr_loc.append(a_text)
        elif child.name == "br": # <br> symbolizes a new location
            if curr_loc:
                loc_str = " ".join(curr_loc).strip()
                # cleanup messy syntax
                loc_str = loc_str.replace("\u00a0", " ")
                loc_str = re.sub(r"\s+\)", ")", loc_str)
                # add to set
                locations.add(loc_str)
                curr_loc = []  # refresh
        else:  # plain text nodes, span or small
            text = child.get_text(separator=" ", strip=True)
            if text:
                curr_loc.append(text)

    if curr_loc:  # last group accounted for
        loc_str = " ".join(curr_loc).strip()
        loc_str = loc_str.replace("\u00a0", " ")
        loc_str = re.sub(r"\s+\)", ")", loc_str)
        locations.add(loc_str)

    return locations