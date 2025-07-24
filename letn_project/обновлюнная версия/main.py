import flet as ft
import random
import time
import threading
import json
import os
import sys

# Файл для сохранения лучших времен и настроек
RECORD_FILE = "maze_records.json"
SETTINGS_FILE = "maze_settings.json"

# Настройки по умолчанию
DEFAULT_SETTINGS = {
    "controls": {
        "up": "W",
        "down": "S",
        "left": "A",
        "right": "D"
    },
    "player_color": "red",
    "player_shape": "square"
}

# Цвета персонажа
PLAYER_COLORS = {
    "red": "#ff0000",
    "yellow": "#ffff00",
    "black": "#000000",
    "purple": "#800080"
}

# Константы для стилей
DEFAULT_FONT_SIZE = 18  # Увеличенный размер шрифта по умолчанию
DEFAULT_FONT_COLOR = "#000000"  # Чёрный цвет текста
TITLE_FONT_SIZE = 28  # Увеличенный размер заголовков
BUTTON_FONT_SIZE = 18  # Увеличенный размер шрифта кнопок


def load_best_times():
    """Загружает лучшие времена из файла"""
    default_times = {
        "Легкий": float('inf'),
        "Средний": float('inf'),
        "Высокий": float('inf')
    }
    try:
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, 'r') as f:
                data = json.load(f)
                # Объединяем загруженные данные с дефолтными на случай, если какого-то уровня не было
                return {**default_times, **data}
    except Exception as e:
        print(f"Ошибка загрузки рекордов: {e}")
        pass
    return default_times


def save_best_times(best_times):
    """Сохраняет лучшие времена в файл"""
    try:
        with open(RECORD_FILE, 'w') as f:
            json.dump(best_times, f)
    except Exception as e:
        print(f"Ошибка сохранения рекордов: {e}")
        pass


def reset_best_times():
    """Сбрасывает лучшие времена к значениям по умолчанию"""
    global best_times
    default_times = {
        "Легкий": float('inf'),
        "Средний": float('inf'),
        "Высокий": float('inf')
    }
    best_times.update(default_times)
    save_best_times(best_times)


def load_settings():
    """Загружает настройки из файла"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                # Объединяем загруженные данные с дефолтными
                return {**DEFAULT_SETTINGS, **data}
    except Exception as e:
        print(f"Ошибка загрузки настроек: {e}")
        pass
    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """Сохраняет настройки в файл"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")
        pass


# Глобальная переменная для хранения лучших времен
best_times = load_best_times()
# Глобальная переменная для хранения настроек
game_settings = load_settings()

# Настройки сложности
DIFFICULTY_SETTINGS = {
    "Легкий": {"rows": 10, "cols": 10},
    "Средний": {"rows": 20, "cols": 20},
    "Высокий": {"rows": 25, "cols": 40}
}

CELL_SIZE = 40


def init_maze(rows, cols):
    maze = {
        "cells": [[False] * cols for _ in range(rows)],
        "vertical_walls": [[True] * (cols + 1) for _ in range(rows)],
        "horizontal_walls": [[True] * cols for _ in range(rows + 1)]
    }
    return maze


def generate_maze_dfs(maze, rows, cols):
    visited = [[False] * cols for _ in range(rows)]

    def carve(x, y):
        visited[y][x] = True
        maze["cells"][y][x] = True
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                if dx == 1:
                    maze["vertical_walls"][y][x + 1] = False
                elif dx == -1:
                    maze["vertical_walls"][y][x] = False
                elif dy == 1:
                    maze["horizontal_walls"][y + 1][x] = False
                elif dy == -1:
                    maze["horizontal_walls"][y][x] = False
                carve(nx, ny)

    carve(0, 0)


def format_time(seconds):
    """Форматирует время в формате MM:SS.ms"""
    if seconds == float('inf') or seconds <= 0:
        return "Нет данных"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 100)
    return f"{minutes:02d}:{secs:02d}.{millis:02d}"


def main_menu(page: ft.Page):
    page.title = "Лабиринт - Главное меню"
    page.bgcolor = "#E6F3FF"  # Нежный голубой фон
    page.window_always_on_top = True
    page.window_maximized = True  # Полноэкранный режим
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.clean()

    def start_game(e):
        mode_selection_screen(page)

    def settings(e):
        settings_screen(page)

    def exit_game(e):
        # Более надежный способ закрытия
        try:
            page.window.close()
        except:
            try:
                page.window.destroy()
            except:
                sys.exit()

    # Отображение лучших времен для каждого уровня
    records_text = ft.Column(
        [
            ft.Text("Лучшие времена:", size=TITLE_FONT_SIZE, color=DEFAULT_FONT_COLOR, weight=ft.FontWeight.BOLD),
            ft.Text(f"Легкий: {format_time(best_times['Легкий'])}", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
            ft.Text(f"Средний: {format_time(best_times['Средний'])}", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
            ft.Text(f"Высокий: {format_time(best_times['Высокий'])}", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
        ],
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    menu = ft.Column(
        [
            ft.Text("Игра Лабиринт", size=48, weight=ft.FontWeight.BOLD, color="#2E86AB"),
            records_text,
            ft.ElevatedButton(
                "Начать игру",
                on_click=start_game,
                width=250,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor="#5DA7DB",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            ft.ElevatedButton(
                "Настройки",
                on_click=settings,
                width=250,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor="#5DA7DB",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            ft.ElevatedButton(
                "Выход",
                on_click=exit_game,
                width=250,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor="#FF6B6B",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )
    page.add(menu)


def mode_selection_screen(page: ft.Page):
    """Экран выбора режима игры"""
    page.title = "Лабиринт - Выбор режима"
    page.bgcolor = "#E6F3FF"
    page.clean()

    def select_single_player(e):
        difficulty_selection_screen(page)

    def select_competitive(e):
        # Пока не реализовано
        pass

    def back_to_menu(e):
        main_menu(page)

    menu = ft.Column(
        [
            ft.Text("Выберите режим игры", size=TITLE_FONT_SIZE, weight=ft.FontWeight.BOLD, color="#2E86AB"),
            ft.ElevatedButton(
                "Одиночный режим",
                on_click=select_single_player,
                width=300,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor="#5DA7DB",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            ft.ElevatedButton(
                "Соревновательный режим",
                on_click=select_competitive,
                width=300,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor="#AAAAAA",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                disabled=True  # Пока не реализовано
            ),
            ft.ElevatedButton(
                "Назад",
                on_click=back_to_menu,
                width=300,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor="#FF6B6B",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )
    page.add(menu)


def difficulty_selection_screen(page: ft.Page):
    """Экран выбора сложности"""
    page.title = "Лабиринт - Выбор сложности"
    page.bgcolor = "#E6F3FF"
    page.clean()

    def start_with_difficulty(difficulty):
        settings = DIFFICULTY_SETTINGS[difficulty]
        # Генерируем seed для этого запуска уровня
        level_seed = random.randint(1, 1000000)
        game_screen(page, settings["rows"], settings["cols"], difficulty, seed=level_seed)

    def back_to_mode_selection(e):
        mode_selection_screen(page)

    menu = ft.Column(
        [
            ft.Text("Выберите уровень сложности", size=TITLE_FONT_SIZE, weight=ft.FontWeight.BOLD, color="#2E86AB"),
            ft.ElevatedButton(
                "Легкий уровень",
                on_click=lambda e: start_with_difficulty("Легкий"),
                width=300,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor="#4CAF50",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            ft.ElevatedButton(
                "Средний уровень",
                on_click=lambda e: start_with_difficulty("Средний"),
                width=300,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor="#FF9800",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            ft.ElevatedButton(
                "Высокий уровень",
                on_click=lambda e: start_with_difficulty("Высокий"),
                width=300,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor="#F44336",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            ft.ElevatedButton(
                "Назад",
                on_click=back_to_mode_selection,
                width=300,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor="#FF6B6B",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )
    page.add(menu)


def settings_screen(page: ft.Page):
    global game_settings
    page.title = "Лабиринт - Настройки"
    page.bgcolor = "#E6F3FF"  # Нежный голубой фон
    page.window_maximized = True
    page.clean()

    # Элементы для настройки управления
    up_key_field = ft.TextField(label="Вверх", value=game_settings["controls"]["up"], width=120)
    down_key_field = ft.TextField(label="Вниз", value=game_settings["controls"]["down"], width=120)
    left_key_field = ft.TextField(label="Влево", value=game_settings["controls"]["left"], width=120)
    right_key_field = ft.TextField(label="Вправо", value=game_settings["controls"]["right"], width=120)

    # Элементы для настройки цвета персонажа
    color_options = [
        ft.dropdown.Option("red", "Красный"),
        ft.dropdown.Option("yellow", "Жёлтый"),
        ft.dropdown.Option("black", "Чёрный"),
        ft.dropdown.Option("purple", "Фиолетовый")
    ]
    color_dropdown = ft.Dropdown(
        label="Цвет персонажа",
        options=color_options,
        value=game_settings["player_color"],
        width=220
    )

    # Элементы для настройки формы персонажа
    shape_options = [
        ft.dropdown.Option("square", "Квадрат"),
        ft.dropdown.Option("circle", "Круг")
    ]
    shape_dropdown = ft.Dropdown(
        label="Форма персонажа",
        options=shape_options,
        value=game_settings["player_shape"],
        width=220
    )

    def save_settings_click(e):
        # Сохраняем настройки управления
        game_settings["controls"]["up"] = up_key_field.value.upper()
        game_settings["controls"]["down"] = down_key_field.value.upper()
        game_settings["controls"]["left"] = left_key_field.value.upper()
        game_settings["controls"]["right"] = right_key_field.value.upper()

        # Сохраняем настройки персонажа
        game_settings["player_color"] = color_dropdown.value
        game_settings["player_shape"] = shape_dropdown.value

        # Сохраняем в файл
        save_settings(game_settings)

        # Показываем уведомление
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Настройки сохранены!", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()

    def reset_records_click(e):
        # Сбрасываем рекорды
        reset_best_times()
        # Показываем уведомление
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Рекорды сброшены!", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
            action="OK",
        )
        page.snack_bar.open = True
        page.update()

    def back_to_menu(e):
        main_menu(page)

    settings_content = ft.Column(
        [
            ft.Text("Настройки", size=TITLE_FONT_SIZE, color="#2E86AB", weight=ft.FontWeight.BOLD),

            # Настройки управления
            ft.Text("Управление", size=TITLE_FONT_SIZE, color="#2E86AB", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Column([
                    ft.Text("Клавиша движения вверх:", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
                    up_key_field
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([
                    ft.Text("Клавиша движения вниз:", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
                    down_key_field
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.Column([
                    ft.Text("Клавиша движения влево:", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
                    left_key_field
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([
                    ft.Text("Клавиша движения вправо:", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
                    right_key_field
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER),

            # Настройки персонажа
            ft.Text("Персонаж", size=TITLE_FONT_SIZE, color="#2E86AB", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Column([
                    ft.Text("Цвет персонажа:", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
                    color_dropdown
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([
                    ft.Text("Форма персонажа:", size=DEFAULT_FONT_SIZE, color=DEFAULT_FONT_COLOR),
                    shape_dropdown
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER),

            # Сброс рекордов
            ft.Text("Рекорды", size=TITLE_FONT_SIZE, color="#2E86AB", weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                "Сбросить рекорды",
                on_click=reset_records_click,
                width=250,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor="#FF6B6B",
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),

            # Кнопки
            ft.Row([
                ft.ElevatedButton(
                    "Сохранить настройки",
                    on_click=save_settings_click,
                    style=ft.ButtonStyle(
                        bgcolor="#4CAF50",
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                ),
                ft.ElevatedButton(
                    "Назад в меню",
                    on_click=back_to_menu,
                    style=ft.ButtonStyle(
                        bgcolor="#5DA7DB",
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=25  # Увеличенный интервал
    )

    page.add(settings_content)


def game_screen(page: ft.Page, maze_rows, maze_cols, difficulty_level, seed=None):
    """
    Экран игры
    :param page: страница Flet
    :param maze_rows: количество строк в лабиринте
    :param maze_cols: количество столбцов в лабиринте
    :param difficulty_level: уровень сложности ("Легкий", "Средний", "Высокий")
    :param seed: seed для генерации лабиринта (для перезапуска того же лабиринта)
    """
    # Определяем seed для перезапуска
    # Если seed не был передан изначально, создаем новый для перезапуска
    restart_seed = seed if seed is not None else random.randint(1, 1000000)
    page.bgcolor = "#000000"
    page.window_maximized = True
    page.clean()

    # Инициализация лабиринта
    maze = init_maze(maze_rows, maze_cols)
    # Устанавливаем seed для генерации, если он передан
    if seed is not None:
        random.seed(seed)
    generate_maze_dfs(maze, maze_rows, maze_cols)
    # Сбросим seed, чтобы не повлияло на другие части программы
    # Это важно, если seed не передавался изначально
    if seed is not None:
        random.seed()

    # Переменные для таймера
    start_time = time.time()
    timer_active = [True]
    timer_text_ref = ft.Ref[ft.Text]()

    # Локальная переменная для отслеживания состояния игры
    game_active = [True]  # Используем список для возможности изменения
    # Переменная для отслеживания паузы
    game_paused = [False]

    # Рассчитываем размер ячеек в зависимости от размера лабиринта
    cell_size = CELL_SIZE
    if maze_rows > 20 or maze_cols > 20:
        cell_size = max(20, CELL_SIZE - (max(maze_rows, maze_cols) // 5))

    canvas = ft.Stack(width=cell_size * maze_cols, height=cell_size * maze_rows)
    # Центрируем лабиринт на странице
    game_container = ft.Container(
        content=canvas,
        alignment=ft.alignment.center,
        expand=True  # <-- ВАЖНО: expand=True только у основного контента
    )

    # Таймер отображения
    timer_text = ft.Text(
        f"Время: 00:00.00",
        size=24,
        color="#FFFFFF",
        weight=ft.FontWeight.BOLD,
        ref=timer_text_ref
    )
    # Отображение текущего уровня сложности
    level_text = ft.Text(
        f"Уровень: {difficulty_level}",
        size=20,
        color="#FFFF00",  # Желтый цвет
        weight=ft.FontWeight.BOLD
    )

    # Рисуем полы ячеек
    for y in range(maze_rows):
        for x in range(maze_cols):
            if maze["cells"][y][x]:
                canvas.controls.append(
                    ft.Container(
                        left=x * cell_size,
                        top=y * cell_size,
                        width=cell_size,
                        height=cell_size,
                        bgcolor="#0000ff",
                    )
                )

    # Рисуем горизонтальные стены
    for y in range(maze_rows + 1):
        for x in range(maze_cols):
            if maze["horizontal_walls"][y][x]:
                canvas.controls.append(
                    ft.Container(
                        left=x * cell_size,
                        top=y * cell_size - 1,
                        width=cell_size,
                        height=2,
                        bgcolor="#ffffff"
                    )
                )

    # Рисуем вертикальные стены
    for y in range(maze_rows):
        for x in range(maze_cols + 1):
            if maze["vertical_walls"][y][x]:
                canvas.controls.append(
                    ft.Container(
                        left=x * cell_size - 1,
                        top=y * cell_size,
                        width=2,
                        height=cell_size,
                        bgcolor="#ffffff"
                    )
                )

    # Инициализация игрока и выхода
    player_x = 0
    player_y = 0
    exit_x = maze_cols - 1
    exit_y = maze_rows - 1

    # Создаем выход
    exit_cell = ft.Container(
        left=exit_x * cell_size,
        top=exit_y * cell_size,
        width=cell_size,
        height=cell_size,
        bgcolor="#00ff00",
    )
    canvas.controls.append(exit_cell)

    # Создаем игрока с учетом настроек
    player_color = PLAYER_COLORS.get(game_settings["player_color"], "#ff0000")
    player_shape = ft.BoxShape.CIRCLE if game_settings["player_shape"] == "circle" else ft.BoxShape.RECTANGLE

    player = ft.Container(
        left=player_x * cell_size,
        top=player_y * cell_size,
        width=cell_size,
        height=cell_size,
        bgcolor=player_color,
        shape=player_shape,
    )
    canvas.controls.append(player)

    # Затемнение фона (изначально скрыто)
    overlay_dark = ft.Container(
        visible=False,
        expand=True,  # <-- Распространяется на весь Stack
        bgcolor="#00000099",  # Полупрозрачный черный
    )

    # Панель победы (изначально скрыта)
    time_text = ft.Text("", size=18, color="#2E86AB", text_align=ft.TextAlign.CENTER)
    record_text = ft.Text("", size=16, color="#4CAF50", text_align=ft.TextAlign.CENTER)
    # Обернем в Container с alignment.center, чтобы центрировать внутри Stack
    victory_dialog_wrapper = ft.Container(
        content=ft.Container(
            width=400,
            height=300,
            bgcolor="#FFFFFF",
            border_radius=20,
            content=ft.Column(
                [
                    ft.Text("Поздравляем!", size=32, color="#2E86AB", weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("Вы прошли лабиринт!", size=20, color="#333333", text_align=ft.TextAlign.CENTER),
                    ft.Text(f"Уровень: {difficulty_level}", size=16, color="#2E86AB", text_align=ft.TextAlign.CENTER),
                    time_text,
                    record_text,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Новый уровень",
                                on_click=lambda e: restart_game(page, maze_rows, maze_cols, difficulty_level),
                                width=150,
                                height=45,
                                style=ft.ButtonStyle(
                                    bgcolor="#4CAF50",
                                    color="#FFFFFF",
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                )
                            ),
                            ft.ElevatedButton(
                                "В меню",
                                on_click=lambda e: main_menu(page),
                                width=150,
                                height=45,
                                style=ft.ButtonStyle(
                                    bgcolor="#FF6B6B",
                                    color="#FFFFFF",
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        spacing=20
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center  # <-- Центрируем внутренний контент
        ),
        visible=False,
        alignment=ft.alignment.center,  # <-- Центрируем wrapper внутри Stack
        expand=True  # <-- Распространяется на весь Stack
    )
    # victory_dialog_wrapper.visible = False # Управление через wrapper

    # Меню паузы (изначально скрыто) - УБРАЛИ кнопку "Настройки"
    # Обернем в Container с alignment.center, чтобы центрировать внутри Stack
    pause_menu_wrapper = ft.Container(
        content=ft.Container(
            width=400,
            height=250,  # Уменьшили высоту, так как убрали одну кнопку
            bgcolor="#FFFFFF",
            border_radius=20,
            content=ft.Column(
                [
                    ft.Text("Пауза", size=32, color="#2E86AB", weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton(
                        "Продолжить",
                        on_click=lambda e: resume_game(),
                        width=250,
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor="#4CAF50",
                            color="#FFFFFF",
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    ),
                    ft.ElevatedButton(
                        "Перезапустить уровень",
                        on_click=lambda e: restart_game(page, maze_rows, maze_cols, difficulty_level),
                        width=250,
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor="#FF9800",
                            color="#FFFFFF",
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    ),
                    # Кнопка "Настройки" УДАЛЕНА
                    ft.ElevatedButton(
                        "Выйти в лобби",
                        on_click=lambda e: main_menu(page),
                        width=250,
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor="#FF6B6B",
                            color="#FFFFFF",
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center  # <-- Центрируем внутренний контент
        ),
        visible=False,
        alignment=ft.alignment.center,  # <-- Центрируем wrapper внутри Stack
        expand=True  # <-- Распространяется на весь Stack
    )

    # pause_menu_wrapper.visible = False # Управление через wrapper

    def restart_game(page, rows, cols, difficulty):
        timer_active[0] = False  # Останавливаем таймер
        # Перезапуск игры с теми же параметрами И тем же seed
        game_screen(page, rows, cols, difficulty, seed=restart_seed)

    def move(dx, dy):
        # Блокируем движение, если игра не активна или на паузе
        if not game_active[0] or game_paused[0]:
            return
        nonlocal player_x, player_y
        new_x = player_x + dx
        new_y = player_y + dy
        if not (0 <= new_x < maze_cols and 0 <= new_y < maze_rows):
            return
        if dx == 1 and maze["vertical_walls"][player_y][player_x + 1]:
            return
        if dx == -1 and maze["vertical_walls"][player_y][player_x]:
            return
        if dy == 1 and maze["horizontal_walls"][player_y + 1][player_x]:
            return
        if dy == -1 and maze["horizontal_walls"][player_y][player_x]:
            return
        player_x, player_y = new_x, new_y
        player.left = player_x * cell_size
        player.top = player_y * cell_size
        player.update()

        # Проверка победы
        if (player_x, player_y) == (exit_x, exit_y):
            # Останавливаем таймер
            timer_active[0] = False
            final_time = time.time() - start_time
            # Блокируем управление только после победы
            game_active[0] = False
            # Проверяем рекорд для текущего уровня сложности
            is_record = final_time < best_times[difficulty_level]
            if is_record:
                best_times[difficulty_level] = final_time
                save_best_times(best_times)  # Сохраняем все рекорды в файл
            # Обновляем текст в диалоге
            time_text.value = f"Ваше время: {format_time(final_time)}"
            record_text.value = "НОВЫЙ РЕКОРД!" if is_record else f"Лучшее время ({difficulty_level}): {format_time(best_times[difficulty_level])}"
            # Показываем оверлей и диалог
            overlay_dark.visible = True
            # victory_dialog.visible = True # <-- Изменено
            victory_dialog_wrapper.visible = True  # <-- Используем wrapper
            # Обновляем элементы
            time_text.update()
            record_text.update()
            page.update()  # <-- Обновляем всю страницу для надежности

    def timer_thread():
        """Функция таймера, выполняющаяся в отдельном потоке"""
        while timer_active[0]:
            try:
                current_time = time.time() - start_time
                if timer_text_ref.current and not game_paused[0]:
                    timer_text_ref.current.value = f"Время: {format_time(current_time)}"
                    page.update()  # Обновляем всю страницу
                time.sleep(0.05)  # Обновляем каждые 50 мс для более плавного отображения
            except:
                break

    def pause_game():
        """Поставить игру на паузу"""
        if not game_active[0]:  # Не ставим на паузу если игра уже закончена
            return
        game_paused[0] = True
        timer_active[0] = False  # Останавливаем таймер
        # Показываем оверлей и меню паузы
        overlay_dark.visible = True
        # pause_menu.visible = True # <-- Изменено
        pause_menu_wrapper.visible = True  # <-- Используем wrapper
        page.update()  # <-- Обновляем всю страницу для надежности

    def resume_game():
        """Продолжить игру"""
        game_paused[0] = False
        timer_active[0] = True  # Возобновляем таймер
        # Скрываем оверлей и меню паузы
        overlay_dark.visible = False
        # pause_menu.visible = False # <-- Изменено
        pause_menu_wrapper.visible = False  # <-- Используем wrapper
        page.update()  # <-- Обновляем всю страницу для надежности
        # Перезапускаем таймер в новом потоке
        threading.Thread(target=timer_thread, daemon=True).start()

    def on_key(e: ft.KeyboardEvent):
        key = e.key.upper()  # Преобразуем в верхний регистр для сравнения
        if key == "ESCAPE":
            if game_paused[0]:
                resume_game()
            else:
                pause_game()
        elif not game_paused[0]:  # Обрабатываем движение только если не на паузе
            # Используем настройки управления
            controls = game_settings["controls"]
            if key == controls["up"]:
                move(0, -1)
            elif key == controls["down"]:
                move(0, 1)
            elif key == controls["left"]:
                move(-1, 0)
            elif key == controls["right"]:
                move(1, 0)

    # Запускаем таймер в отдельном потоке
    threading.Thread(target=timer_thread, daemon=True).start()
    page.on_keyboard_event = on_key

    # Добавляем элементы на страницу
    # Основной контент игры
    # Используем Stack и правильно упорядочиваем слои
    # 1. Основной лабиринт
    # 2. Оверлей затемнения
    # 3. Диалоги (они сами скрыты)
    game_content = ft.Stack([
        game_container,  # <-- Основной контент
        overlay_dark,  # <-- Оверлей (expand=True)
        victory_dialog_wrapper,  # <-- Диалог победы (expand=True, но контент центрирован)
        pause_menu_wrapper,  # <-- Меню паузы (expand=True, но контент центрирован)
    ], expand=True)  # <-- Stack расширяется на всю страницу

    # Добавляем все элементы на страницу
    page.clean()  # <-- Важно очистить перед добавлением нового содержимого
    page.add(
        ft.Row([timer_text, level_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        game_content  # <-- Добавляем Stack как основной контент
        # Диалоги теперь внутри Stack, управляются через visible
    )
    page.update()  # <-- Принудительное обновление после добавления


def main(page: ft.Page):
    main_menu(page)


ft.app(target=main)