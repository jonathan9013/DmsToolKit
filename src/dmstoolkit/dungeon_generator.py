import numpy as np
import random
import openpyxl
from openpyxl.styles import PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from pathlib import Path
from typing import Literal

def generate_dungeon():
    grid = np.zeros((5,5), dtype=object)
    cur_row_index = 2
    cur_col_index = 2
    ahead_row_index = 0
    ahead_col_index = 0
    left_row_index = 0
    left_col_index = 0
    right_row_index = 0
    right_col_index = 0
    grid[(cur_row_index,cur_col_index)]=1
    prev_direction = 0
    prev_choice = "na"
    
    while get_grid_sum(grid)<500:
        
        choice = hall_or_room(prev_choice)
        #print(choice)
        if choice == "hall":    
            direction, length, width = generate_hall(prev_direction)
            if prev_choice == "room":
                #print(f"Current: {cur_row_index},{cur_col_index}")
                cur_row_index, cur_col_index = get_room_exit(direction, prev_direction, ahead_row_index, ahead_col_index, left_row_index, left_col_index, right_row_index, right_col_index)
                #print(f"New: {cur_row_index},{cur_col_index}")
            grid, cur_row_index, cur_col_index = build_hall(length, direction, width, grid, cur_row_index, cur_col_index)
        elif choice == "room":
            size = generate_room()
            grid, ahead_row_index, ahead_col_index, left_row_index, left_col_index, right_row_index, right_col_index, direction = build_room(size, prev_direction, grid, cur_row_index, cur_col_index) 
            
        prev_direction = direction
        prev_choice = choice
        #print(choice)
        #print(cur_row_index, cur_col_index)
        
    export_to_xlsx(grid)

def get_room_exit(direction, prev_direction, ahead_row_index, ahead_col_index, left_row_index, left_col_index, right_row_index, right_col_index):
    #print(f"Dir {direction}, Prev {prev_direction}")
    if direction == prev_direction:
        return ahead_row_index, ahead_col_index
    if direction == prev_direction - 1:
        return left_row_index, left_col_index
    if direction == prev_direction + 1:
        return right_row_index, right_col_index
    if direction == 4 and prev_direction == 1:
        return left_row_index, left_col_index
    if direction == 1 and prev_direction == 4:
        return right_row_index, right_col_index
        

def hall_or_room(prev_choice):
    if prev_choice == "room":
        return "hall"
    else:
        chance = random.randint(1,100)
        if chance <= 70:
            return "hall"
        else:
            return "room"
    
def generate_room():
    room_chance = random.randint(1,100)
    size = 0
    if room_chance > 0 and room_chance <= 20:
        size = 9
    elif room_chance > 20 and room_chance <= 80:
        size = 7
    elif room_chance > 80 and room_chance <= 100:
        size = 5
    
    return size

def build_room(size, direction, grid, cur_row_index, cur_col_index):
    if direction == 0:
        direction = 2
    base_rows, base_cols = grid.shape
    half_size = size // 2
    
    match direction:
        case 1:
            start_r, end_r = cur_row_index - size, cur_row_index
            start_c, end_c = cur_col_index - half_size, cur_col_index + half_size + 1
        case 2:        
            start_r, end_r = cur_row_index - half_size, cur_row_index + half_size + 1
            start_c, end_c = cur_col_index + 1, cur_col_index + size + 1
        case 3:
            start_r, end_r = cur_row_index +1, cur_row_index + size + 1
            start_c, end_c = cur_col_index - half_size, cur_col_index + half_size + 1
        case 4:
            start_r, end_r = cur_row_index - half_size, cur_row_index + half_size + 1
            start_c, end_c = cur_col_index - size, cur_col_index
        
    min_r = min(0, start_r)
    max_r = max(base_rows, end_r)
    min_c = min(0, start_c)
    max_c = max(base_cols, end_c)
    
    new_rows = max_r - min_r
    new_cols = max_c - min_c
    new_grid = np.zeros((new_rows, new_cols), dtype=object)
    
    row_shift = -min_r
    col_shift = -min_c
    
    orig_start_r = 0 + row_shift
    orig_end_r = base_rows + row_shift
    orig_start_c = 0 + col_shift
    orig_end_c = base_cols + col_shift
    new_grid[orig_start_r:orig_end_r, orig_start_c:orig_end_c] = grid
    
    new_grid[start_r + row_shift : end_r + row_shift, 
            start_c + col_shift : end_c + col_shift] = 1
    
    ahead_row_index = 0
    ahead_col_index = 0
    
    left_row_index = 0
    left_col_index = 0
    
    right_row_index = 0
    right_col_index = 0
    
    match direction:
        case 1:
            ahead_row_index = cur_row_index - size
            ahead_col_index = cur_col_index
            
            left_row_index = cur_row_index - (half_size + 1)
            left_col_index = cur_col_index - half_size
            
            right_row_index = cur_row_index - (half_size + 1)
            right_col_index = cur_col_index + half_size
        case 2:
            ahead_row_index = cur_row_index 
            ahead_col_index = cur_col_index + size
            
            left_row_index = cur_row_index - half_size
            left_col_index = cur_col_index + (half_size + 1)
            
            right_row_index = cur_row_index + half_size
            right_col_index = cur_col_index + (half_size + 1)
        case 3:
            ahead_row_index = cur_row_index + size
            ahead_col_index = cur_col_index
            
            left_row_index = cur_row_index + (half_size + 1)
            left_col_index = cur_col_index + half_size
            
            right_row_index = cur_row_index + (half_size + 1)
            right_col_index = cur_col_index - half_size
        case 4:
            ahead_row_index = cur_row_index 
            ahead_col_index = cur_col_index - size
            
            left_row_index = cur_row_index + half_size
            left_col_index = cur_col_index - (half_size + 1)
            
            right_row_index = cur_row_index - half_size
            right_col_index = cur_col_index - (half_size + 1)           
    
    ahead_row_index += row_shift
    ahead_col_index += col_shift
    left_row_index += row_shift
    left_col_index += col_shift
    right_row_index += row_shift
    right_col_index += col_shift

    return new_grid, ahead_row_index, ahead_col_index, left_row_index, left_col_index, right_row_index, right_col_index, direction
            
def generate_hall(prev_direction):
    bactrack_direction = 0
    match prev_direction:
        case 0:
            bactrack_direction = 0
        case 1:
            bactrack_direction = 3
        case 2:
            bactrack_direction = 4
        case 3:
            bactrack_direction = 1
        case 4:
            bactrack_direction = 2
    direction = random.randint(1,4)
    while direction == bactrack_direction:
        direction = random.randint(1,4)
    length = random.randint(2,8)
    width = 1
    if length > 3:
        wide_chance = random.randint(1,100)
        if wide_chance > 90:
            width = 2
    return direction, length, width

def build_hall(length, direction, width, grid, cur_row_index, cur_col_index):
    if width == 1:
        for i in range(length):
            match direction:
                case 1:
                    cur_row_index -= 1
                case 2:
                    cur_col_index += 1
                case 3:
                    cur_row_index += 1
                case 4:
                    cur_col_index -= 1
            try:
                if cur_col_index < 0:
                    cur_col_index = 0
                    grid = expand_grid(grid, direction)
                if cur_row_index < 0:
                    cur_row_index=0
                    grid = expand_grid(grid, direction)
                            
                grid[(cur_row_index,cur_col_index)]=1
                
            except IndexError:
                while cur_row_index >= grid.shape[0]:
                    grid = expand_grid(grid, 3)
                while cur_col_index >= grid.shape[1]:
                    grid = expand_grid(grid, 2)
                grid[(cur_row_index,cur_col_index)]=1
    
    else:
        match direction:
            case 1:
                second_row_index = cur_row_index
                second_col_index = cur_col_index + 1
            case 2:
                second_row_index = cur_row_index +1
                second_col_index = cur_col_index
            case 3:
                second_row_index = cur_row_index
                second_col_index = cur_col_index - 1
            case 4:
                second_row_index = cur_row_index -1
                second_col_index = cur_col_index 

        for i in range(length):
            match direction:
                case 1:
                    cur_row_index -= 1
                    second_row_index -= 1
                case 2:
                    cur_col_index += 1
                    second_col_index += 1
                case 3:
                    cur_row_index += 1
                    second_row_index += 1
                case 4:
                    cur_col_index -= 1
                    second_col_index -= 1
                
            
            if cur_row_index < 0:
                cur_row_index=0
                second_row_index=0
                grid = expand_grid(grid, direction)
                
            elif second_row_index < 0:
                second_row_index = 0
                cur_row_index = 1
                grid = expand_grid(grid, 1)
            
            while is_row_invalid(grid,cur_row_index) or is_row_invalid(grid,second_row_index):
                grid = expand_grid(grid, 3)
                
            if cur_col_index < 0:
                cur_col_index = 0
                second_col_index =0
                grid = expand_grid(grid, direction)
                
            elif second_col_index < 0:
                second_col_index = 0
                cur_col_index = 1
                grid = expand_grid(grid, 4)
            
            while is_col_invalid(grid, cur_col_index) or is_col_invalid(grid, second_col_index):
                grid = expand_grid(grid, 2)                    
                
            grid[(cur_row_index,cur_col_index)]=1
            grid[(second_row_index,second_col_index)]=1
                
            
                
    return grid, cur_row_index, cur_col_index

def expand_grid(grid, side):
    match side:
        case 1:
            new_row = np.zeros(grid.shape[1], dtype=grid.dtype)
            grid = np.vstack([new_row, grid])
        case 2:
            new_col = np.zeros((grid.shape[0],1), dtype=grid.dtype)
            grid = np.hstack([grid, new_col])
        case 3:
            new_row = np.zeros(grid.shape[1], dtype=grid.dtype)
            grid = np.vstack([grid, new_row])
        case 4:
            new_col = np.zeros((grid.shape[0],1), dtype=grid.dtype)
            grid = np.hstack([new_col, grid])
    return grid
    
def is_row_invalid(grid, row_index):
    num_rows = grid.shape[0]
    return not(-num_rows <= row_index < num_rows)

def is_col_invalid(grid, col_index):
    num_cols = grid.shape[1]
    return not(-num_cols <= col_index <num_cols)

def get_grid_sum(grid):
    is_digit = np.char.isdigit(grid.astype(str))
    sum = grid[is_digit].astype(int).sum()
    return sum

def export_to_xlsx(grid):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "map"
    
    #enable standard grid lines so 0 cells renain as a normal grid
    ws.views.sheetView[0].showGridLines = True

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    #define styles
    gray_fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")
    thick_black = Side(style="thick", color='000000')
    
    top_row = 99
    bottom_row = 0
    
    left_col = 99
    right_col = 0
    
    for r in range(rows):
        for c in range(cols):
            #excell is 1-indexed(row 1, column 1)
            cell = ws.cell(row=r+1, column=c+1)
        
            
            #if cell is a 1 apply fill and calculate borders
            if grid[r][c] == 1:
                if r < top_row:
                    top_row = r
                if r > bottom_row:
                    bottom_row = r
                if c < left_col:
                    left_col = c
                if c > right_col:
                    right_col = c
                
                cell.fill = gray_fill
                
                border_kwargs = {}
                
                #check top for 0
                if r == 0 or grid[r-1][c] == 0:
                    border_kwargs['top'] = thick_black
                
                #check bottom for 0
                if r == rows-1 or grid[r+1][c] == 0:
                    border_kwargs['bottom'] = thick_black
    
                #check left for 0
                if c == 0 or grid[r][c-1] == 0:
                    border_kwargs['left'] = thick_black
                
                #check bottom for 0
                if c == cols-1 or grid[r][c+1] == 0:
                    border_kwargs['right'] = thick_black
                
                #apply borders
                cell.border = Border(**border_kwargs)
                
   
    if left_col == 0:
        ws.insert_cols(idx=1, amount=2)
        right_col = right_col + 2
    if top_row == 0:
        ws.insert_rows(1, amount=2)
        bottom_row = bottom_row + 2
        
    col_width = 5
    row_height = col_width * 4.5
    
    right_col = right_col + 3
    bottom_row = bottom_row + 3
    ws.cell(row=bottom_row, column=right_col, value="FDB")

    for col in range(1,right_col):
        col_letter = get_column_letter(col)
        ws.column_dimensions[col_letter].width = col_width
    for row in range(1, bottom_row):
        ws.row_dimensions[row].height = row_height
    
    download_path = Path.home() / "downloads" / "Dungeon.xslx"  
    wb.save(download_path)
    print(f"Workbook successfully saved to {download_path}")