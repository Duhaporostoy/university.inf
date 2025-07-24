import flet as ft
import random
import time
import threading
import json
import os

# --- Настройки ---
RECORD_FILE = "maze_records.json"
CELL_SIZE = 35
DIFFICULTY_SETTINGS = {
    "Легкий": {"rows": 10, "cols": 10},
    "Средний": {"rows": 15, "cols": 20},
    "Высокий": {"rows": 20, "cols": 30}
}

# --- Константы для состояния стен ---
WALL = True  # Стена есть
PATH = False  # Проход открыт


# --- Логика сохранения рекордов ---
def load_best_times():
    default_times = {
        "Легкий": float('inf'),
        "Средний": float('inf'),
        "Высокий": float('inf')
    }
    try:
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, 'r') as f:
                data = json.load(f)
                return {**default_times, **data}
    except Exception:
        pass
    return default_times


def save_best_times(best_times):
    try:
        with open(RECORD_FILE, 'w') as f:
            json.dump(best_times, f)
    except Exception:
        pass


best_times = load_best_times()


# --- Логика лабиринта с DFS Stack ---
class MazeCell:
    """Класс для представления ячейки лабиринта во время генерации"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': WALL, 'right': WALL, 'bottom': WALL, 'left': WALL}
        self.visited = False


def init_generation_grid(rows, cols):
    """Инициализирует сетку для генерации лабиринта"""
    return [[MazeCell(x, y) for y in range(cols)] for x in range(rows)]


def remove_wall(current, next):
    """Удаляет стену между двумя соседними ячейками"""
    dx = next.x - current.x
    dy = next.y - current.y
    if dx == 1:  # next справа
        current.walls['right'] = PATH
        next.walls['left'] = PATH
    elif dx == -1:  # next слева
        current.walls['left'] = PATH
        next.walls['right'] = PATH
    elif dy == 1:  # next снизу
        current.walls['bottom'] = PATH
        next.walls['top'] = PATH
    elif dy == -1:  # next сверху
        current.walls['top'] = PATH
        next.walls['bottom'] = PATH


def generate_maze_stack(rows, cols):
    """Генерирует лабиринт с использованием алгоритма DFS со стеком"""
    grid = init_generation_grid(rows, cols)

    # Начинаем с (0, 0)
    start_x, start_y = 0, 0
    grid[start_x][start_y].visited = True
    stack = [grid[start_x][start_y]]

    while stack:
        current = stack[-1]
        # Найти непосещенных соседей
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # лево, право, верх, низ
        for dx, dy in directions:
            nx, ny = current.x + dx, current.y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not grid[nx][ny].visited:
                neighbors.append(grid[nx][ny])

        if neighbors:
            next_cell = random.choice(neighbors)
            remove_wall(current, next_cell)
            next_cell.visited = True
            stack.append(next_cell)
        else:
            stack.pop()

    # Преобразование в формат для отрисовки
    # vertical_walls[y][x] означает вертикальную стену справа от ячейки (x,y)
    vertical_walls = [[WALL] * (cols + 1) for _ in range(rows)]
    # horizontal_walls[y][x] означает горизонтальную стену снизу от ячейки (x,y)
    horizontal_walls = [[WALL] * cols for _ in range(rows + 1)]
    # cells_render[y][x] просто для отрисовки пола
    cells_render = [[True] * cols for _ in range(rows)]

    # Заполнение массивов стен на основе сгенерированного grid
    for x in range(rows):
        for y in range(cols):
            cell = grid[x][y]
            # Вертикальные стены
            if not cell.walls['left'] and y > 0:
                vertical_walls[x][y] = PATH
            if not cell.walls['right'] and y < cols - 1:
                vertical_walls[x][y + 1] = PATH
            # Горизонтальные стены
            if not cell.walls['top'] and x > 0:
                horizontal_walls[x][y] = PATH
            if not cell.walls['bottom'] and x < rows - 1:
                horizontal_walls[x + 1][y] = PATH

    # Открыть вход (левая стена (0,0)) и выход (правая стена (rows-1, cols-1))
    # В нашей системе координат (x - строки, y - столбцы)
    # Вход: левая стена ячейки (0, 0)
    vertical_walls[0][0] = PATH
    # Выход: правая стена ячейки (rows-1, cols-1)
    vertical_walls[rows - 1][cols] = PATH  # Индекс cols для правой границы

    return {
        "vertical_walls": vertical_walls,
        "horizontal_walls": horizontal_walls,
        "cells_render": cells_render,
        "rows": rows,
        "cols": cols
    }


def format_time(seconds):
    if seconds == float('inf') or seconds <= 0:
        return "Нет данных"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 100)
    return f"{minutes:02d}:{secs:02d}.{millis:02d}"


# --- Экраны интерфейса ---
def main_menu(page: ft.Page):
    page.title = "Лабиринт - Главное меню"
    page.bgcolor = "#E6F3FF"
    page.window_always_on_top = True
    page.window_maximized = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.clean()

    def start_game(e):
        mode_selection_screen(page)

    def settings(e):
        settings_screen(page)

    def exit_game(e):
        page.window.destroy()  # Исправлено: правильный способ закрытия окна

    records_text = ft.Column([
        ft.Text("Лучшие времена:", size=20, color="#2E86AB", weight=ft.FontWeight.BOLD),
        ft.Text(f"Легкий: {format_time(best_times['Легкий'])}", size=16, color="#333333"),
        ft.Text(f"Средний: {format_time(best_times['Средний'])}", size=16, color="#333333"),
        ft.Text(f"Высокий: {format_time(best_times['Высокий'])}", size=16, color="#333333"),
    ], spacing=5)
    
    menu = ft.Column([
        ft.Text("Игра Лабиринт", size=48, weight=ft.FontWeight.BOLD, color="#2E86AB"),
        records_text,
        ft.ElevatedButton("Начать игру", on_click=start_game, width=250, height=50,
                          style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#5DA7DB")),
        ft.ElevatedButton("Настройки", on_click=settings, width=250, height=50,
                          style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#5DA7DB")),
        ft.ElevatedButton("Выход", on_click=exit_game, width=250, height=50,
                          style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#FF6B6B")),
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30)
    page.add(menu)


def mode_selection_screen(page: ft.Page):
    page.title = "Лабиринт - Выбор режима"
    page.bgcolor = "#E6F3FF"
    page.clean()

    def select_single_player(e):
        difficulty_selection_screen(page)

    def back_to_menu(e):
        main_menu(page)

    menu = ft.Column([
        ft.Text("Выберите режим игры", size=36, weight=ft.FontWeight.BOLD, color="#2E86AB"),
        ft.ElevatedButton("Одиночный режим", on_click=select_single_player, width=300, height=60,
                          style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#5DA7DB")),
        ft.ElevatedButton("Назад", on_click=back_to_menu, width=300, height=50,
                          style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#FF6B6B")),
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30)
    page.add(menu)


def difficulty_selection_screen(page: ft.Page):
    page.title = "Лабиринт - Выбор сложности"
    page.bgcolor = "#E6F3FF"
    page.clean()

    def start_with_difficulty(difficulty):
        settings = DIFFICULTY_SETTINGS[difficulty]
        level_seed = random.randint(1, 1000000)
        game_screen(page, settings["rows"], settings["cols"], difficulty, seed=level_seed)

    def back_to_mode_selection(e):
        mode_selection_screen(page)

    menu = ft.Column([
        ft.Text("Выберите уровень сложности", size=36, weight=ft.FontWeight.BOLD, color="#2E86AB"),
        ft.ElevatedButton("Легкий уровень", on_click=lambda e: start_with_difficulty("Легкий"), width=300, height=60,
                          style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#4CAF50")),
        ft.ElevatedButton("Средний уровень", on_click=lambda e: start_with_difficulty("Средний"), width=300, height=60,
                          style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#FF9800")),
        ft.ElevatedButton("Высокий уровень", on_click=lambda e: start_with_difficulty("Высокий"), width=300, height=60,
                          style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#F44336")),
        ft.ElevatedButton("Назад", on_click=back_to_mode_selection, width=300, height=50,
                          style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#FF6B6B")),
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30)
    page.add(menu)


def settings_screen(page: ft.Page):
    page.title = "Лабиринт - Настройки"
    page.bgcolor = "#E6F3FF"
    page.clean()

    def back_to_menu(e):
        main_menu(page)

    page.add(
        ft.Text("Настройки (пока недоступны)", size=32, color="#2E86AB", weight=ft.FontWeight.BOLD),
        ft.ElevatedButton("Назад в меню", on_click=back_to_menu,
                          style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#5DA7DB"))
    )


def game_screen(page: ft.Page, maze_rows, maze_cols, difficulty_level, seed=None):
    restart_seed = seed if seed is not None else random.randint(1, 1000000)
    page.bgcolor = "#000000"
    page.window_maximized = True
    page.clean()

    # Генерация лабиринта
    if seed is not None:
        random.seed(seed)
    maze = generate_maze_stack(maze_rows, maze_cols)
    if seed is not None:
        random.seed()  # Сброс seed

    start_time = time.time()
    timer_active = [True]
    game_active = [True]
    game_paused = [False]

    # Определяем размер ячейки
    max_dimension = max(maze_rows, maze_cols)
    if max_dimension <= 15:
        cell_size = 40
    elif max_dimension <= 25:
        cell_size = 30
    else:
        cell_size = 25

    canvas_width = cell_size * maze_cols
    canvas_height = cell_size * maze_rows
    canvas = ft.Stack(width=canvas_width, height=canvas_height)
    game_container = ft.Container(content=canvas, alignment=ft.alignment.center, expand=True)

    timer_text_ref = ft.Ref[ft.Text]()
    timer_text = ft.Text(f"Время: 00:00.00", size=20, color="#FFFFFF", weight=ft.FontWeight.BOLD, ref=timer_text_ref)
    level_text = ft.Text(f"Уровень: {difficulty_level}", size=18, color="#FFFF00", weight=ft.FontWeight.BOLD)

    # --- Отрисовка лабиринта ---
    # Полы (опционально)
    for y in range(maze_rows):
        for x in range(maze_cols):
            if maze["cells_render"][y][x]:
                canvas.controls.append(
                    ft.Container(left=x * cell_size, top=y * cell_size, width=cell_size, height=cell_size,
                                 bgcolor="#1976D2"))  # Синий пол

    # Горизонтальные стены
    for y in range(maze_rows + 1):
        for x in range(maze_cols):
            # maze["horizontal_walls"][y][x] - стена снизу от ячейки (x, y-1) или сверху от ячейки (x, y)
            if maze["horizontal_walls"][y][x]:
                canvas.controls.append(
                    ft.Container(left=x * cell_size, top=y * cell_size - 1, width=cell_size, height=2,
                                 bgcolor="#FFFFFF"))

    # Вертикальные стены
    for y in range(maze_rows):
        for x in range(maze_cols + 1):
            # maze["vertical_walls"][y][x] - стена справа от ячейки (x-1, y) или слева от ячейки (x, y)
            if maze["vertical_walls"][y][x]:
                canvas.controls.append(
                    ft.Container(left=x * cell_size - 1, top=y * cell_size, width=2, height=cell_size,
                                 bgcolor="#FFFFFF"))

    # Игрок и выход
    player_x, player_y = 0, 0
    exit_x, exit_y = maze_cols - 1, maze_rows - 1

    exit_cell = ft.Container(left=exit_x * cell_size, top=exit_y * cell_size, width=cell_size, height=cell_size,
                             bgcolor="#4CAF50")  # Зеленый выход
    canvas.controls.append(exit_cell)

    player = ft.Container(left=player_x * cell_size, top=player_y * cell_size, width=cell_size, height=cell_size,
                          bgcolor="#F44336")  # Красный игрок
    canvas.controls.append(player)

    # UI элементы
    overlay_dark = ft.Container(visible=False, expand=True, bgcolor="#00000099")

    time_text = ft.Text("", size=18, color="#2E86AB", text_align=ft.TextAlign.CENTER)
    record_text = ft.Text("", size=16, color="#4CAF50", text_align=ft.TextAlign.CENTER)

    victory_dialog = ft.Container(
        visible=False, width=400, height=300, bgcolor="#FFFFFF", border_radius=20,
        content=ft.Column([
            ft.Text("Поздравляем!", size=32, color="#2E86AB", weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER),
            ft.Text("Вы прошли лабиринт!", size=20, text_align=ft.TextAlign.CENTER),
            ft.Text(f"Уровень: {difficulty_level}", size=16, color="#2E86AB", text_align=ft.TextAlign.CENTER),
            time_text, record_text,
            ft.Row([
                ft.ElevatedButton("Новый уровень",
                                  on_click=lambda e: restart_game(page, maze_rows, maze_cols, difficulty_level,
                                                                  restart_seed),
                                  width=150, height=45, style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#4CAF50")),
                ft.ElevatedButton("В меню", on_click=lambda e: main_menu(page), width=150, height=45,
                                  style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#FF6B6B")),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND, spacing=20)
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center
    )

    pause_menu = ft.Container(
        visible=False, width=400, height=250, bgcolor="#FFFFFF", border_radius=20,
        content=ft.Column([
            ft.Text("Пауза", size=32, color="#2E86AB", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.ElevatedButton("Продолжить", on_click=lambda e: resume_game(), width=250, height=45,
                              style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#4CAF50")),
            ft.ElevatedButton("Перезапустить уровень",
                              on_click=lambda e: restart_game(page, maze_rows, maze_cols, difficulty_level,
                                                              restart_seed),
                              width=250, height=45, style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#FF9800")),
            ft.ElevatedButton("Выйти в лобби", on_click=lambda e: main_menu(page), width=250, height=45,
                              style=ft.ButtonStyle(color="#FFFFFF", bgcolor="#FF6B6B")),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center
    )

    # --- Логика игры ---
    def restart_game(page, rows, cols, difficulty, seed_for_restart):
        timer_active[0] = False
        game_screen(page, rows, cols, difficulty, seed=seed_for_restart)

    def move_player(dx, dy):
        if not game_active[0] or game_paused[0]:
            return
        nonlocal player_x, player_y
        new_x, new_y = player_x + dx, player_y + dy

        # Проверка границ лабиринта
        if not (0 <= new_x < maze_cols and 0 <= new_y < maze_rows):
            return

        # Проверка стен
        # dx=1 (вправо): проверяем вертикальную стену справа от текущей ячейки (player_y, player_x)
        if dx == 1 and maze["vertical_walls"][player_y][player_x + 1]:
            return
        # dx=-1 (влево): проверяем вертикальную стену слева от текущей ячейки (player_y, player_x)
        if dx == -1 and maze["vertical_walls"][player_y][player_x]:
            return
        # dy=1 (вниз): проверяем горизонтальную стену снизу от текущей ячейки (player_y, player_x)
        if dy == 1 and maze["horizontal_walls"][player_y + 1][player_x]:
            return
        # dy=-1 (вверх): проверяем горизонтальную стену сверху от текущей ячейки (player_y, player_x)
        if dy == -1 and maze["horizontal_walls"][player_y][player_x]:
            return

        player_x, player_y = new_x, new_y
        player.left = player_x * cell_size
        player.top = player_y * cell_size
        player.update()

        if (player_x, player_y) == (exit_x, exit_y):
            timer_active[0] = False
            game_active[0] = False
            final_time = time.time() - start_time

            is_record = final_time < best_times[difficulty_level]
            if is_record:
                best_times[difficulty_level] = final_time
                save_best_times(best_times)

            time_text.value = f"Ваше время: {format_time(final_time)}"
            record_text.value = "НОВЫЙ РЕКОРД!" if is_record else f"Лучшее время ({difficulty_level}): {format_time(best_times[difficulty_level])}"

            overlay_dark.visible = True
            victory_dialog.visible = True
            time_text.update()
            record_text.update()
            overlay_dark.update()
            victory_dialog.update()

    def timer_thread():
        while timer_active[0]:
            try:
                current_time = time.time() - start_time
                if timer_text_ref.current and not game_paused[0]:
                    timer_text_ref.current.value = f"Время: {format_time(current_time)}"
                    page.update()
                time.sleep(0.05)
            except:
                break

    def pause_game():
        if not game_active[0]:
            return
        game_paused[0] = True
        timer_active[0] = False
        overlay_dark.visible = True
        pause_menu.visible = True
        overlay_dark.update()
        pause_menu.update()

    def resume_game():
        game_paused[0] = False
        timer_active[0] = True
        overlay_dark.visible = False
        pause_menu.visible = False
        overlay_dark.update()
        pause_menu.update()
        threading.Thread(target=timer_thread, daemon=True).start()

    def on_key(e: ft.KeyboardEvent):
        key = e.key.lower()
        if key == "escape":
            if game_paused[0]:
                resume_game()
            else:
                pause_game()
        elif not game_paused[0]:
            if key == "w":
                move_player(0, -1)
            elif key == "s":
                move_player(0, 1)
            elif key == "a":
                move_player(-1, 0)
            elif key == "d":
                move_player(1, 0)

    threading.Thread(target=timer_thread, daemon=True).start()
    page.on_keyboard_event = on_key

    page.add(
        ft.Row([timer_text, level_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Stack([game_container, overlay_dark,
                  ft.Container(content=victory_dialog, alignment=ft.alignment.center, expand=True),
                  ft.Container(content=pause_menu, alignment=ft.alignment.center, expand=True)])
    )


# --- Запуск ---
def main(page: ft.Page):
    main_menu(page)


ft.app(target=main)