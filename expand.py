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