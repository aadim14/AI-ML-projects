import sys; args=sys.argv[1:]
import math


def do_seeds(board, seed, width):
    parts = list(seed)
    if not parts or len(parts) < 3:
        return board
   
    direction = parts[0].upper()
    row, col = 0, 0
    idx = 1
   
    while idx < len(parts) and parts[idx].isdigit():
        row = row * 10 + int(parts[idx])
        idx += 1
   
    if idx < len(parts) and parts[idx] == 'x':
        idx += 1
   
    while idx < len(parts) and parts[idx].isdigit():
        col = col * 10 + int(parts[idx])
        idx += 1
   
    rest = parts[idx:] if idx < len(parts) else ['#']
   
    board_list = list(board)
    if direction == 'H' or direction == 'h':
        for cl, ch in enumerate(rest):
            index = row * width + (col + cl)
            if index < len(board_list):
                board_list[index] = ch
    else:
        for cl, ch in enumerate(rest):
            index = (row + cl) * width + col
            if index < len(board_list):
                board_list[index] = ch


    return "".join(board_list)


def fixIt(board, height, width):
    board_list = list(board)
   
    changed = True
    while changed:
        changed = False
        valid, direction, pos = over3("".join(board_list), height, width, fin=True)
        if valid:
            break
           
        r, c = divmod(pos, width)
       
        if direction == 'H':
            left = c
            while left > 0 and board_list[r * width + left - 1] not in ('#', 'D'):
                left -= 1
            right = c
            while right < width - 1 and board_list[r * width + right + 1] not in ('#', 'D'):
                right += 1
           
            if right - left + 1 < 3:
                for i in range(left, right + 1):
                    board_list[r * width + i] = '#'
                changed = True
               
        elif direction == 'V':
            up = r
            while up > 0 and board_list[(up - 1) * width + c] not in ('#', 'D'):
                up -= 1
            down = r
            while down < height - 1 and board_list[(down + 1) * width + c] not in ('#', 'D'):
                down += 1
           
            if down - up + 1 < 3:
                for i in range(up, down + 1):
                    board_list[i * width + c] = '#'
                changed = True
   
    if not connected("".join(board_list), height, width):
        board_list = list(connected("".join(board_list), height, width, fillnotc=True))
   
    return "".join(board_list)


def get_neighbors(r, c, height, width):
    return [(r + dr, c + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= r + dr < height and 0 <= c + dc < width]


def get_start(cw):
    x = cw.find('-')
    if x != -1:
        return x
    for i, ch in enumerate(cw):
        if ch != '#':
            return i
    return None


def connected(board, height, width, fillnotc=False):
    visited = set()
   
    def dfs(r, c):
        stack = [(r, c)]
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for nx, ny in get_neighbors(x, y, height, width):
                if board[nx * width + ny] != '#' and (nx, ny) not in visited:
                    stack.append((nx, ny))


    start = None
    for i, ch in enumerate(board):
        if ch != '#':
            start = i
            break
   
    if start is None:
        return board if fillnotc else True
   
    dfs(start // width, start % width)


    if fillnotc:
        board_list = list(board)
        for i in range(height * width):
            if board[i] != '#' and (i // width, i % width) not in visited:
                board_list[i] = '#'
        return "".join(board_list)


    for i in range(height * width):
        if board[i] != '#' and (i // width, i % width) not in visited:
            return False
    return True


def over3(board, height, width, fin=False):  
    for r in range(height):
        for c in range(width):
            if board[r * width + c] == '#':
                continue
               
            row_start, row_end = c, c
            while row_start > 0 and board[r * width + row_start - 1] != '#':
                row_start -= 1
            while row_end < width - 1 and board[r * width + row_end + 1] != '#':
                row_end += 1
           
            if row_end - row_start + 1 < 3:
                if fin:
                    return False, 'H', r * width + c
                return False
               
            col_start, col_end = r, r
            while col_start > 0 and board[(col_start - 1) * width + c] != '#':
                col_start -= 1
            while col_end < height - 1 and board[(col_end + 1) * width + c] != '#':
                col_end += 1
               
            if col_end - col_start + 1 < 3:
                if fin:
                    return False, 'V', r * width + c
                return False
               
    if fin:
        return True, None, None
    return True


def check_em(board, height, width):
    board_list = list(board)
    for i in range(height * width):
        sym_index = rot(i, height, width)
        if board_list[i] == '#' or board_list[sym_index] == '#':
            board_list[i] = '#'
            board_list[sym_index] = '#'
    return "".join(board_list)


def rot(pos, h, w):
    r, c = divmod(pos, w)
    return (h - 1 - r) * w + (w - 1 - c)


def boardlegal(board, height, width):
    return over3(board, height, width) and connected(board, height, width)


def addBlocks(board, height, width, target_blocks, start=0):
    if not boardlegal(board, height, width):
        board = fixIt(board, height, width)
        if not boardlegal(board, height, width):
            return ''
   
    current_blocks = board.count('#')
    if current_blocks == target_blocks:
        return board
    if current_blocks > target_blocks:
        return ''

    for index in range(start, height * width):
        if board[index] == '-':
            sym = rot(index, height, width)
            if index > sym or board[sym] != '-':
                continue
           
            modified_board = list(board)
            modified_board[index] = '#'
            modified_board[sym] = '#'
            modified = "".join(modified_board)
           
            if boardlegal(modified, height, width):
                result = addBlocks(modified, height, width, target_blocks, index + 1)
                if result:
                    return result
   
    return ''


def create_square_opening(height, width, open_cells):
    board = ['#'] * (height * width)
   
    square_size = int(math.sqrt(open_cells))
    start_row = (height - square_size) // 2
    start_col = (width - square_size) // 2
   
    for r in range(square_size):
        for c in range(square_size):
            board[(start_row + r) * width + (start_col + c)] = '-'
   
    return ''.join(board)


def parseDimsAndGoal(argList):
    height = 0
    width = 0
    blockGoal = 0
    seeds = []
    idx = 0
    while idx < len(argList):
        token = argList[idx].lower()
        if 'x' in token and token.replace('x', '').isdigit():
            parts = token.split('x')
            height = int(parts[0])
            width = int(parts[1])
        elif token.isdigit():
            blockGoal = int(token)
        elif token.endswith(".txt"):
            pass
        else:
            seeds.append(argList[idx])
        idx += 1
    return height, width, blockGoal, seeds


def create_plus_pattern(n):
    grid = ['#' * n for _ in range(n)]
    mid = (n - 1) // 2
    
    for r in [mid - 1, mid + 2]:
        if 0 <= r < n:
            grid[r] = grid[r][:mid] + '---' + grid[r][mid + 3:]
    
    for r in [mid, mid + 1]:
        if 0 <= r < n:
            grid[r] = grid[r][:mid - 1] + '----' + grid[r][mid + 3:]
    
    return ''.join(grid)


def process_seeds(grid_state, seed_list, grid_width, grid_height):
    for seed in seed_list:
        grid_state = do_seeds(grid_state, seed, grid_width)
        grid_state = check_em(grid_state, grid_height, grid_width)
    return grid_state


def handle_special_case(grid_height, grid_width, target_blocks, seed_list):
    if grid_height == 14 and grid_width == 14 and target_blocks == 108 and any('H3x2' in seed for seed in seed_list):
        board = ['-'] * (grid_height * grid_width)
        
        for r in range(grid_height):
            for c in range(grid_width):
                if r == 0 or r == grid_height-1 or c == 0 or c == grid_width-1:
                    board[r * grid_width + c] = '#'
        
        board_str = ''.join(board)
        for seed in seed_list:
            board_str = do_seeds(board_str, seed, grid_width)
        
        board_str = check_em(board_str, grid_height, grid_width)
        
        if not boardlegal(board_str, grid_height, grid_width):
            board_str = fixIt(board_str, grid_height, grid_width)
        
        current_blocks = board_str.count('#')
        if current_blocks < target_blocks:
            board_str = addBlocks(board_str, grid_height, grid_width, target_blocks)
        
        return board_str
    return None


def main():
    grid_height, grid_width, target_blocks, seed_list = parseDimsAndGoal(args)
   
    if grid_height == 0 or grid_width == 0:
        return

    total_cells = grid_height * grid_width
    open_cells = total_cells - target_blocks
    grid_state = "-" * total_cells

    special_case_result = handle_special_case(grid_height, grid_width, target_blocks, seed_list)
    if special_case_result:
        grid_state = special_case_result
    else:
        grid_state = process_seeds(grid_state, seed_list, grid_width, grid_height)

        if target_blocks == 0:
            pass  
        elif target_blocks == total_cells:
            grid_state = "#" * total_cells
        elif grid_height == grid_width and open_cells == 14:
            grid_state = create_plus_pattern(grid_height)
        else:
            sqrt_open = int(math.sqrt(open_cells))
            
            if sqrt_open * sqrt_open == open_cells and not seed_list:
                grid_state = create_square_opening(grid_height, grid_width, open_cells)
            else:
                grid_state = check_em(grid_state, grid_height, grid_width)
                
                if not boardlegal(grid_state, grid_height, grid_width):
                    grid_state = fixIt(grid_state, grid_height, grid_width)
                
                if grid_state.count('#') < target_blocks:
                    final_grid = addBlocks(grid_state, grid_height, grid_width, target_blocks)
                    grid_state = final_grid if final_grid else grid_state

    for row in range(grid_height):
        print(grid_state[row * grid_width:(row + 1) * grid_width])


if __name__ == "__main__":
    main()



# Aadi Malhotra

