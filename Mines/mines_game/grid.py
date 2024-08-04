import random

def create_grid(size, win_cells):
    grid = [['' for _ in range(size)] for _ in range(size)]

    all_positions = [(r, c) for r in range(size) for c in range(size)]
    win_positions = random.sample(all_positions, win_cells)

    for r, c in win_positions:
        grid[r][c] = 'WIN'

    for r in range(size):
        for c in range(size):
            if grid[r][c] != 'WIN':
                win_count = sum(
                    1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                    if (dr, dc) != (0, 0) and 0 <= r + dr < size and 0 <= c + dc < size and grid[r + dr][c + dc] == 'WIN'
                )
                grid[r][c] = str(win_count) if win_count > 0 else ''

    return grid
