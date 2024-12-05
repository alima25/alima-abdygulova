import random
import os

GRID_SIZE = 7
SHIP_SIZES = [3, 2, 2, 1, 1, 1, 1]
EMPTY = '.'
MISS = 'M'
HIT = 'H'
SUNK = 'S'

def create_grid(size):
    return [[EMPTY for _ in range(size)] for _ in range(size)]

def display_grid(grid, reveal=False):
    print("\n  " + " ".join("ABCDEFG"[:GRID_SIZE]))
    for i, row in enumerate(grid):
        print(f"{i + 1} " + " ".join(row if reveal else (c if c in [MISS, HIT, SUNK] else EMPTY for c in row)))
    print()

def place_ships(grid):
    ships = []
    for size in SHIP_SIZES:
        placed = False
        while not placed:
            orientation = random.choice(['H', 'V'])
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if can_place_ship(grid, row, col, size, orientation):
                ship = place_ship(grid, row, col, size, orientation)
                ships.append(ship)
                placed = True
    return ships

def can_place_ship(grid, row, col, size, orientation):
    for i in range(size):
        r, c = (row + i, col) if orientation == 'V' else (row, col + i)
        if r >= GRID_SIZE or c >= GRID_SIZE or grid[r][c] != EMPTY:
            return False
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and grid[nr][nc] != EMPTY:
                    return False
    return True

def place_ship(grid, row, col, size, orientation):
    ship = []
    for i in range(size):
        r, c = (row + i, col) if orientation == 'V' else (row, col + i)
        grid[r][c] = str(size)  
        ship.append((r, c))
    return ship

def is_sunk(grid, ship):
    return all(grid[r][c] == HIT for r, c in ship)
  
def handle_shot(grid, ships, row, col):
    if grid[row][col] in [MISS, HIT, SUNK]:
        return "Already shot here!"
    elif grid[row][col] == EMPTY:
        grid[row][col] = MISS
        return "Miss!"
    else:  
        grid[row][col] = HIT
        for ship in ships:
            if (row, col) in ship:
                if is_sunk(grid, ship):
                    for r, c in ship:
                        grid[r][c] = SUNK
                    return "Sunk!"
                return "Hit!"
    return "Error!"

def input_to_coords(inp):
    try:
        letter, number = inp[0].upper(), int(inp[1]) - 1
        row, col = number, "ABCDEFG".index(letter)
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return row, col
    except (ValueError, IndexError):
        pass
    return None

def play_game():
    player_name = input("Enter your name: ").strip()
    grid = create_grid(GRID_SIZE)
    ships = place_ships(grid)
    shots = 0

    clear_screen()
    display_grid(grid)  

    while any(grid[r][c].isdigit() for ship in ships for r, c in ship):
        inp = input("Enter your shot (e.g., B5): ").strip()
        coords = input_to_coords(inp)
        if not coords:
            print("Invalid input. Try again.")
            continue
        row, col = coords
        result = handle_shot(grid, ships, row, col)
        shots += 1

        clear_screen()
        display_grid(grid)
        print(result)  

    clear_screen()
    display_grid(grid, reveal=True)
    print(f"Victory! You sunk all ships in {shots} shots.")
    return player_name, shots
  
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    leaderboard = []
    while True:
        name, shots = play_game()
        leaderboard.append((name, shots))
        leaderboard.sort(key=lambda x: x[1]) 
        again = input("Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("\nLeaderboard:")
            for i, (player, score) in enumerate(leaderboard, start=1):
                print(f"{i}. {player}: {score} shots")
            break

if __name__ == "__main__":
    main()
