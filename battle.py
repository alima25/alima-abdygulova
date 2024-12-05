import random

# Константы
GRID_SIZE = 7
SHIP_SIZES = [3, 2, 2, 1, 1, 1, 1]
EMPTY = '🌊'
MISS = '❌'
HIT = '🔥'
SUNK = '💀'

# Функция создания игрового поля
def create_grid(size):
    return [[EMPTY for _ in range(size)] for _ in range(size)]

# Функция отображения игрового поля
def display_grid(grid, reveal=False):
    print("\n  " + " ".join("ABCDEFG"[:GRID_SIZE]))  # Верхняя строка с буквами
    for i, row in enumerate(grid):
        print(f"{i + 1} " + " ".join(
            row if reveal else (c if c in [MISS, HIT, SUNK] else EMPTY for c in row)
        ))
    print()

# Функция размещения кораблей
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

# Проверка возможности размещения корабля
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

# Размещение корабля на поле
def place_ship(grid, row, col, size, orientation):
    ship = []
    for i in range(size):
        r, c = (row + i, col) if orientation == 'V' else (row, col + i)
        grid[r][c] = str(size)  # Указываем размер корабля
        ship.append((r, c))
    return ship

# Проверка, потоплен ли корабль
def is_sunk(grid, ship):
    return all(grid[r][c] == HIT for r, c in ship)

# Обработка выстрела
def handle_shot(grid, ships, row, col):
    if grid[row][col] in [MISS, HIT, SUNK]:
        return "Вы уже стреляли сюда!"
    elif grid[row][col] == EMPTY:
        grid[row][col] = MISS
        return "Мимо!"
    else:  # Это корабль
        grid[row][col] = HIT
        for ship in ships:
            if (row, col) in ship:
                if is_sunk(grid, ship):
                    for r, c in ship:
                        grid[r][c] = SUNK
                    return "Корабль потоплен!"
                return "Попадание!"
    return "Ошибка!"

# Преобразование координат
def input_to_coords(inp):
    try:
        letter, number = inp[0].upper(), int(inp[1]) - 1
        row, col = number, "ABCDEFG".index(letter)
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return row, col
    except (ValueError, IndexError):
        pass
    return None

# Очистка экрана
def clear_screen():
    print("\n" * 100)

# Основной цикл игры
def play_game():
    player_name = input("Введите ваше имя: ").strip()
    grid = create_grid(GRID_SIZE)
    ships = place_ships(grid)
    shots = 0

    while any(grid[r][c].isdigit() for ship in ships for r, c in ship):
        clear_screen()  # Очистка экрана
        display_grid(grid)  # Отображение игрового поля
        inp = input("Введите координаты выстрела (например, B5): ").strip()
        coords = input_to_coords(inp)
        if not coords:
            print("Неверный ввод. Попробуйте снова.")
            continue
        row, col = coords
        result = handle_shot(grid, ships, row, col)
        shots += 1

        clear_screen()
        display_grid(grid)  # Отображение обновленного поля
        print(result)  # Печать результата выстрела ("Попадание!", "Мимо!" и т.д.)

    clear_screen()
    display_grid(grid, reveal=True)
    print(f"Победа! Вы потопили все корабли за {shots} выстрелов.")
    return player_name, shots

# Главный цикл с таблицей лидеров
def main():
    leaderboard = []
    while True:
        name, shots = play_game()
        leaderboard.append((name, shots))
        leaderboard.sort(key=lambda x: x[1])  # Сортировка по количеству выстрелов
        again = input("Сыграем еще раз? (y/n): ").strip().lower()
        if again != 'y':
            print("\nТаблица лидеров:")
            for i, (player, score) in enumerate(leaderboard, start=1):
                print(f"{i}. {player}: {score} выстрелов")
            break

if __name__ == "__main__":
    main()
