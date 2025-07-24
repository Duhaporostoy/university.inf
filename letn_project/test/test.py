import flet as ft
import random
import time
import threading
import json
import os

# --- Константы ---
# Файл для сохранения лучших времен
RECORD_FILE = "maze_records.json"
# Файл для сохранения пользовательских настроек
SETTINGS_FILE = "user_settings.json"
# Файл для музыки (убедитесь, что он существует)
# MUSIC_FILE = "background_music.mp3"  # Или .wav - Закомментировано, так как музыка отключена

# Настройки сложности
DIFFICULTY_SETTINGS = {
    "Легкий": {"rows": 10, "cols": 10},
    "Средний": {"rows": 20, "cols": 20},
    "Высокий": {"rows": 25, "cols": 40}
}
# Размер ячейки по умолчанию и его границы
DEFAULT_CELL_SIZE = 40
CELL_SIZE_MIN = 15
CELL_SIZE_MAX = 80
# --- Цветовые темы ---
THEMES = {
    "classic": {  # Классическая тема
        "bg_main_menu": "#E6F3FF",
        "bg_game": "#000000",
        "primary": "#2E86AB",
        "button_start": "#5DA7DB",
        "button_exit": "#FF6B6B",
        "button_easy": "#4CAF50",
        "button_medium": "#FF9800",
        "button_hard": "#F44336",
        "player": "#ff0000",  # Игрок 1 по умолчанию
        "player2": "#0000ff",  # Игрок 2 по умолчанию
        "exit": "#00ff00",
        "wall": "#ffffff",
        "path": "#0000ff",
        "timer": "#FFFFFF",
        "level": "#FFFF00",
        "record_new": "#4CAF50",
        "record_text": "#2E86AB",
        "text_default": "#333333",  # Темно-серый текст
        "text_on_light_bg": "#333333",  # Темный текст для светлого фона
        "text_on_dark_bg": "#FFFFFF",  # Светлый текст для темного фона
        "overlay_dark": "#00000099",
        "dialog_bg": "#FFFFFF",
        "settings_label": "#555555",  # Темно-серый для меток
        "dropdown_text_color": "#000000",  # Черный текст в выпадающих списках для контраста
        "dropdown_bg_color": "#FFFFFF",  # Белый фон выпадающих списков
        "switch_label_color": "#000000",  # Черный цвет для текста переключателей
        # Добавляем специфичные цвета для игроков
        "player1_color": "#ff0000",  # Красный для игрока 1
        "player2_color": "#0000ff",  # Синий для игрока 2
    },
    "dark": {  # Темная тема
        "bg_main_menu": "#1E1E1E",
        "bg_game": "#000000",
        "primary": "#4A90E2",
        "button_start": "#3A7BC8",
        "button_exit": "#C44536",
        "button_easy": "#3A7C3A",
        "button_medium": "#C97C3A",
        "button_hard": "#C44536",
        "player": "#ff4d4d",  # Игрок 1 по умолчанию
        "player2": "#4d4dff",  # Игрок 2 по умолчанию
        "exit": "#4dff4d",
        "wall": "#aaaaaa",
        "path": "#333399",
        "timer": "#FFFFFF",
        "level": "#FFFF99",
        "record_new": "#4dff4d",
        "record_text": "#4A90E2",
        "text_default": "#CCCCCC",  # Светло-серый текст
        "text_on_light_bg": "#333333",
        "text_on_dark_bg": "#FFFFFF",
        "overlay_dark": "#000000CC",
        "dialog_bg": "#2D2D2D",
        "settings_label": "#AAAAAA",  # Светло-серый для меток
        "dropdown_text_color": "#FFFFFF",  # Белый текст в выпадающих списках
        "dropdown_bg_color": "#3E3E3E",  # Темно-серый фон выпадающих списков
        "switch_label_color": "#FFFFFF",  # Белый цвет для текста переключателей
        # Добавляем специфичные цвета для игроков
        "player1_color": "#ff4d4d",  # Красный для игрока 1
        "player2_color": "#4d4dff",  # Синий для игрока 2
    },
    "high_contrast": {  # Высококонтрастная тема
        "bg_main_menu": "#FFFFFF",
        "bg_game": "#000000",
        "primary": "#000000",
        "button_start": "#0066CC",
        "button_exit": "#CC0000",
        "button_easy": "#009900",
        "button_medium": "#FF9900",
        "button_hard": "#CC0000",
        "player": "#FF0000",  # Игрок 1 по умолчанию
        "player2": "#0000FF",  # Игрок 2 по умолчанию
        "exit": "#00FF00",
        "wall": "#FFFFFF",
        "path": "#0000FF",
        "timer": "#FFFFFF",
        "level": "#FFFF00",
        "record_new": "#00FF00",
        "record_text": "#000000",
        "text_default": "#000000",  # Черный текст
        "text_on_light_bg": "#000000",
        "text_on_dark_bg": "#FFFFFF",
        "overlay_dark": "#000000CC",
        "dialog_bg": "#EEEEEE",
        "settings_label": "#333333",  # Темный для меток
        "dropdown_text_color": "#000000",  # Черный текст в выпадающих списках для контраста
        "dropdown_bg_color": "#FFFFFF",  # Белый фон выпадающих списков
        "switch_label_color": "#000000",  # Черный цвет для текста переключателей
        # Добавляем специфичные цвета для игроков
        "player1_color": "#FF0000",  # Красный для игрока 1
        "player2_color": "#0000FF",  # Синий для игрока 2
    },
    # --- Новые темы ---
    "ocean": {  # Океан
        "bg_main_menu": "#B0D8FF",
        "bg_game": "#001f3f",
        "primary": "#0074D9",
        "button_start": "#39CCCC",
        "button_exit": "#FF4136",
        "button_easy": "#2ECC40",
        "button_medium": "#FFDC00",
        "button_hard": "#B10DC9",
        "player": "#FF4136",  # Игрок 1 по умолчанию
        "player2": "#39CCCC",  # Игрок 2 по умолчанию
        "exit": "#2ECC40",
        "wall": "#AAAAAA",
        "path": "#0074D9",
        "timer": "#FFFFFF",
        "level": "#FFDC00",
        "record_new": "#2ECC40",
        "record_text": "#001f3f",
        "text_default": "#111111",
        "text_on_light_bg": "#111111",
        "text_on_dark_bg": "#FFFFFF",
        "overlay_dark": "#00000099",
        "dialog_bg": "#FFFFFF",
        "settings_label": "#333333",
        "dropdown_text_color": "#000000",
        "dropdown_bg_color": "#FFFFFF",
        "switch_label_color": "#000000",
        # Добавляем специфичные цвета для игроков
        "player1_color": "#FF4136",  # Оранжево-красный для игрока 1
        "player2_color": "#39CCCC",  # Бирюзовый для игрока 2
    },
    "forest": {  # Лес
        "bg_main_menu": "#A8E6CF",
        "bg_game": "#1B5E20",
        "primary": "#4CAF50",
        "button_start": "#8BC34A",
        "button_exit": "#F44336",
        "button_easy": "#009688",
        "button_medium": "#FFC107",
        "button_hard": "#795548",
        "player": "#F44336",  # Игрок 1 по умолчанию
        "player2": "#FFC107",  # Игрок 2 по умолчанию
        "exit": "#FFEB3B",
        "wall": "#8D6E63",
        "path": "#4CAF50",
        "timer": "#FFFFFF",
        "level": "#FF9800",
        "record_new": "#FFEB3B",
        "record_text": "#1B5E20",
        "text_default": "#222222",
        "text_on_light_bg": "#222222",
        "text_on_dark_bg": "#FFFFFF",
        "overlay_dark": "#00000099",
        "dialog_bg": "#FFFFFF",
        "settings_label": "#444444",
        "dropdown_text_color": "#000000",
        "dropdown_bg_color": "#FFFFFF",
        "switch_label_color": "#000000",
        # Добавляем специфичные цвета для игроков
        "player1_color": "#F44336",  # Красный для игрока 1
        "player2_color": "#FFC107",  # Желтый для игрока 2
    },
    "sunset": {  # Закат
        "bg_main_menu": "#FFD1DC",
        "bg_game": "#4A235A",
        "primary": "#FF6B35",
        "button_start": "#F79F1F",
        "button_exit": "#EA2027",
        "button_easy": "#006266",
        "button_medium": "#EE5A24",
        "button_hard": "#5758BB",
        "player": "#EA2027",  # Игрок 1 по умолчанию
        "player2": "#F79F1F",  # Игрок 2 по умолчанию
        "exit": "#009432",
        "wall": "#6D214F",
        "path": "#12CBC4",
        "timer": "#FFFFFF",
        "level": "#0652DD",
        "record_new": "#009432",
        "record_text": "#4A235A",
        "text_default": "#333333",
        "text_on_light_bg": "#333333",
        "text_on_dark_bg": "#FFFFFF",
        "overlay_dark": "#00000099",
        "dialog_bg": "#FFFFFF",
        "settings_label": "#555555",
        "dropdown_text_color": "#000000",
        "dropdown_bg_color": "#FFFFFF",
        "switch_label_color": "#000000",
        # Добавляем специфичные цвета для игроков
        "player1_color": "#EA2027",  # Красный для игрока 1
        "player2_color": "#F79F1F",  # Оранжевый для игрока 2
    }
}
# Названия тем для отображения в настройках
THEME_NAMES = {
    "classic": "Классическая",
    "dark": "Темная",
    "high_contrast": "Высококонтрастная",
    "ocean": "Океан",
    "forest": "Лес",
    "sunset": "Закат"
}
# --- Локализация ---
# Поддерживаемые языки
SUPPORTED_LANGUAGES = {
    "ru": "Русский",
    "en": "English"
}
# Словарь переводов
TRANSLATIONS = {
    # Main Menu
    "main_menu_title": {"ru": "Главное меню", "en": "Main Menu"},
    "game_title": {"ru": "Игра Лабиринт", "en": "Maze Game"},
    "records": {"ru": "Лучшие времена:", "en": "Best Times:"},
    "easy": {"ru": "Легкий", "en": "Easy"},
    "medium": {"ru": "Средний", "en": "Medium"},
    "hard": {"ru": "Высокий", "en": "Hard"},
    "no_data": {"ru": "Нет данных", "en": "No Data"},
    "start_game": {"ru": "Начать игру", "en": "Start Game"},
    "settings": {"ru": "Настройки", "en": "Settings"},
    "exit": {"ru": "Выход", "en": "Exit"},
    # Mode Selection
    "mode_selection_title": {"ru": "Выбор режима", "en": "Mode Selection"},
    "select_mode": {"ru": "Выберите режим игры", "en": "Select Game Mode"},
    "single_player": {"ru": "Одиночный режим", "en": "Single Player"},
    "competitive": {"ru": "Соревновательный режим", "en": "Competitive Mode"},
    "back": {"ru": "Назад", "en": "Back"},
    # Difficulty Selection
    "difficulty_selection_title": {"ru": "Выбор сложности", "en": "Difficulty Selection"},
    "select_difficulty": {"ru": "Выберите уровень сложности", "en": "Select Difficulty Level"},
    "easy_level": {"ru": "Легкий уровень", "en": "Easy Level"},
    "medium_level": {"ru": "Средний уровень", "en": "Medium Level"},
    "hard_level": {"ru": "Высокий уровень", "en": "Hard Level"},
    "random_start_position": {"ru": "Случайная стартовая позиция", "en": "Random Start Position"},
    # Game Screen
    "level": {"ru": "Уровень", "en": "Level"},
    "time": {"ru": "Время", "en": "Time"},
    "pause": {"ru": "Пауза", "en": "Pause"},
    "continue": {"ru": "Продолжить", "en": "Continue"},
    "restart_level": {"ru": "Перезапустить уровень", "en": "Restart Level"},
    "exit_to_lobby": {"ru": "Выйти в лобби", "en": "Exit to Lobby"},
    "congratulations": {"ru": "Поздравляем!", "en": "Congratulations!"},
    "you_won": {"ru": "Вы прошли лабиринт!", "en": "You completed the maze!"},
    "your_time": {"ru": "Ваше время", "en": "Your Time"},
    "new_record": {"ru": "НОВЫЙ РЕКОРД!", "en": "NEW RECORD!"},
    "best_time": {"ru": "Лучшее время", "en": "Best Time"},
    "new_level": {"ru": "Новый уровень", "en": "New Level"},
    "to_menu": {"ru": "В меню", "en": "To Menu"},
    # Competitive Mode Specific
    "player": {"ru": "Игрок", "en": "Player"},
    "winner": {"ru": "Победитель", "en": "Winner"},
    # Settings Screen
    "settings_title": {"ru": "Настройки", "en": "Settings"},
    "cell_size_label": {"ru": "Размер ячейки лабиринта:", "en": "Maze Cell Size:"},
    "language": {"ru": "Язык", "en": "Language"},
    "records_label": {"ru": "Рекорды:", "en": "Records:"},
    "reset_records": {"ru": "Сбросить рекорды", "en": "Reset Records"},
    "save_and_exit": {"ru": "Сохранить и выйти", "en": "Save and Exit"},
    "cancel": {"ru": "Отмена", "en": "Cancel"},
    "back_to_menu": {"ru": "Назад в меню", "en": "Back to Menu"},
    "records_reset": {"ru": "Рекорды сброшены!", "en": "Records Reset!"},
    "category_language": {"ru": "Язык", "en": "Language"},
    "category_controls": {"ru": "Управление", "en": "Controls"},
    "category_appearance": {"ru": "Внешний вид", "en": "Appearance"},
    "category_gameplay": {"ru": "Геймплей", "en": "Gameplay"},
    "section_in_development": {"ru": "Раздел находится в разработке.", "en": "Section under development."},
    "theme_label": {"ru": "Тема оформления:", "en": "Theme:"},
    "appearance_title": {"ru": "Внешний вид", "en": "Appearance"},
    "gameplay_title": {"ru": "Геймплей", "en": "Gameplay"},
    "save": {"ru": "Сохранить", "en": "Save"},
    # Theme Names for Dropdown
    "theme_classic": {"ru": "Классическая", "en": "Classic"},
    "theme_dark": {"ru": "Темная", "en": "Dark"},
    "theme_high_contrast": {"ru": "Высококонтрастная", "en": "High Contrast"},
    "theme_ocean": {"ru": "Океан", "en": "Ocean"},
    "theme_forest": {"ru": "Лес", "en": "Forest"},
    "theme_sunset": {"ru": "Закат", "en": "Sunset"},
    # Timer Setting
    "show_timer": {"ru": "Показывать таймер", "en": "Show Timer"},
    # Music Settings
    "music": {"ru": "Музыка", "en": "Music"},
    # Controls Settings
    "controls_title": {"ru": "Управление", "en": "Controls"},
    "move_up": {"ru": "Движение вверх", "en": "Move Up"},
    "move_down": {"ru": "Движение вниз", "en": "Move Down"},
    "move_left": {"ru": "Движение влево", "en": "Move Left"},
    "move_right": {"ru": "Движение вправо", "en": "Move Right"},
    "pause_game": {"ru": "Пауза", "en": "Pause"},
    "key_not_set": {"ru": "Не назначено", "en": "Not Set"},
    "press_key_to_assign": {"ru": "Нажмите клавишу для назначения...", "en": "Press key to assign..."},
    "key_already_used": {"ru": "Клавиша уже используется!", "en": "Key already in use!"},
    "reset_to_defaults": {"ru": "Сбросить по умолчанию", "en": "Reset to Defaults"},
    # Exit Confirmation
    "exit_confirmation": {"ru": "Подтверждение выхода", "en": "Exit Confirmation"},
    "exit_question": {"ru": "Вы уверены, что хотите выйти?", "en": "Are you sure you want to exit?"},
    "yes": {"ru": "Да", "en": "Yes"},
    "no": {"ru": "Нет", "en": "No"},
}


# --- Вспомогательные функции ---
def format_time(seconds):
    """Форматирует время в формате MM:SS.ms"""
    # Получаем текущий язык для локализации "Нет данных"
    global user_settings
    current_lang = user_settings.get("language", "ru")
    no_data_text = TRANSLATIONS["no_data"].get(current_lang, "Нет данных")
    if seconds == float('inf') or seconds <= 0:
        return no_data_text
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 100)
    return f"{minutes:02d}:{secs:02d}.{millis:02d}"


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


def load_user_settings():
    """Загружает пользовательские настройки из файла"""
    default_settings = {
        "cell_size": DEFAULT_CELL_SIZE,
        "theme": "classic",  # Добавляем тему по умолчанию
        "language": "ru",  # Добавляем язык по умолчанию
        "random_start": False,  # Случайная стартовая позиция по умолчанию
        # Настройки управления по умолчанию
        "controls": {
            "up": "w",
            "down": "s",
            "left": "a",
            "right": "d",
            "pause": "escape"
        },
        # Настройки музыки по умолчанию
        "music_enabled": True,
        "music_volume": 0.5,
    }
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                # Объединяем загруженные данные с дефолтными
                merged_settings = default_settings.copy()
                merged_settings.update(data)
                # Убедимся, что все необходимые поля управления присутствуют
                if "controls" not in merged_settings:
                    merged_settings["controls"] = default_settings["controls"]
                else:
                    # Объединяем с дефолтными контролами, если какие-то отсутствуют
                    default_controls = default_settings["controls"]
                    user_controls = merged_settings["controls"]
                    merged_controls = default_controls.copy()
                    merged_controls.update(user_controls)
                    merged_settings["controls"] = merged_controls
                return merged_settings
    except Exception as e:
        print(f"Ошибка загрузки настроек: {e}")
        pass
    return default_settings.copy()


def save_user_settings(settings):
    """Сохраняет пользовательские настройки в файл"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")
        pass


# --- Функция для получения перевода ---
def get_translation(key: str) -> str:
    """Получает перевод для заданного ключа на текущем языке."""
    global user_settings
    current_lang = user_settings.get("language", "ru")
    if key in TRANSLATIONS:
        if current_lang in TRANSLATIONS[key]:
            return TRANSLATIONS[key][current_lang]
        else:
            # Если перевода на текущий язык нет, пробуем английский
            if "en" in TRANSLATIONS[key]:
                return TRANSLATIONS[key]["en"]
            else:
                return key
    else:
        return key


# --- Функция для получения цветов текущей темы ---
def get_current_colors():
    """Получает цвета для текущей темы из настроек пользователя."""
    global user_settings
    current_theme_key = user_settings.get("theme", "classic")
    # Возвращаем цвета для текущей темы или классической, если тема не найдена
    return THEMES.get(current_theme_key, THEMES["classic"])


# --- Глобальное состояние ---
best_times = load_best_times()
user_settings = load_user_settings()


# --- Логика лабиринта ---
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


# --- Экраны настроек ---
def settings_main(page: ft.Page):
    """Главная страница настроек с навигацией по категориям"""
    # Получаем цвета текущей темы
    Colors = get_current_colors()
    page.title = f"{get_translation('game_title')} - {get_translation('settings_title')}"
    page.bgcolor = Colors["bg_main_menu"]
    page.window_maximized = True
    page.clean()
    page.scroll = ft.ScrollMode.AUTO
    # --- Горизонтальная навигация (вкладки) ---
    categories = [
        {"name_key": "category_appearance", "key": "appearance", "func": settings_appearance},
        {"name_key": "category_controls", "key": "controls", "func": settings_controls},
        {"name_key": "category_gameplay", "key": "gameplay", "func": settings_gameplay},
    ]
    # Создаем кнопки для каждой категории
    tab_buttons = []
    for category in categories:
        btn = ft.ElevatedButton(
            get_translation(category["name_key"]),
            on_click=lambda e, func=category["func"]: func(page),
            style=ft.ButtonStyle(
                bgcolor=Colors["button_start"],
                color="#FFFFFF",
                shape=ft.RoundedRectangleBorder(radius=5),
                padding=ft.Padding(10, 10, 10, 10)
            )
        )
        tab_buttons.append(btn)

    # Кнопка "Назад в меню"
    def back_to_menu(e):
        main_menu(page)

    back_button = ft.ElevatedButton(
        get_translation("back_to_menu"),
        icon=ft.Icons.ARROW_BACK,
        on_click=back_to_menu,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_exit"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    # --- Сборка основного содержимого ---
    tabs_row = ft.Row(
        controls=tab_buttons,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )
    bottom_row = ft.Row(
        controls=[back_button],
        alignment=ft.MainAxisAlignment.START,
    )
    # Основной контент - приветствие
    main_content_area = ft.Container(
        content=ft.Column(
            [
                ft.Text(get_translation("settings_title"), size=32, color=Colors["primary"], weight=ft.FontWeight.BOLD),
                ft.Text(get_translation("select_mode"), size=20, color=Colors["text_default"]),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        alignment=ft.alignment.center,
        expand=True
    )
    # Собираем всё вместе
    main_layout = ft.Column(
        [
            ft.Divider(height=1, color=Colors["primary"]),
            tabs_row,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            main_content_area,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            bottom_row,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True
    )
    page.add(main_layout)


def settings_appearance(page: ft.Page):
    """Экран настроек - Внешний вид"""
    # Получаем цвета текущей темы
    Colors = get_current_colors()
    # Перезагружаем настройки для получения актуального языка
    global user_settings
    user_settings = load_user_settings()
    page.title = f"{get_translation('game_title')} - {get_translation('settings_title')} - {get_translation('appearance_title')}"
    page.bgcolor = Colors["bg_main_menu"]
    page.clean()
    page.scroll = ft.ScrollMode.AUTO
    # --- Настройка размера ячейки ---
    current_cell_size = user_settings.get("cell_size", DEFAULT_CELL_SIZE)
    preview_cell = ft.Container(
        width=float(current_cell_size),
        height=float(current_cell_size),
        bgcolor=Colors["path"],
        border=ft.border.all(1, Colors["wall"]),
    )
    cell_size_value_text = ft.Text(f"{current_cell_size}px", size=16, color=Colors["settings_label"])

    def update_preview(value):
        int_value = int(value)
        cell_size_value_text.value = f"{int_value}px"
        preview_cell.width = float(int_value)
        preview_cell.height = float(int_value)
        cell_size_value_text.update()
        preview_cell.update()

    cell_size_slider = ft.Slider(
        min=CELL_SIZE_MIN,
        max=CELL_SIZE_MAX,
        value=current_cell_size,
        label="{value}px",
        on_change=lambda e: update_preview(e.control.value),
        width=300
    )
    # --- Выбор темы ---
    current_theme = user_settings.get("theme", "classic")
    theme_options = []
    for theme_key, theme_name in THEME_NAMES.items():
        # Получаем локализованное имя темы
        localized_theme_name = get_translation(f"theme_{theme_key}") or theme_name
        # Явно задаем цвет текста для каждой опции
        option_text_widget = ft.Text(localized_theme_name, color=Colors["dropdown_text_color"], size=16)
        theme_options.append(ft.dropdown.Option(key=theme_key, text=localized_theme_name, content=option_text_widget))
    theme_dropdown = ft.Dropdown(
        label=get_translation("theme_label"),
        options=theme_options,
        value=current_theme,
        width=300,
        color=Colors["dropdown_text_color"],  # Цвет текста внутри Dropdown
        bgcolor=Colors["dropdown_bg_color"],  # Цвет фона Dropdown
    )

    # --- Кнопка сохранения и возврата ---
    def save_and_back(e):
        global user_settings
        user_settings["cell_size"] = int(cell_size_slider.value)
        user_settings["theme"] = theme_dropdown.value
        save_user_settings(user_settings)
        settings_main(page)  # Возвращаемся к главной странице настроек

    save_button = ft.ElevatedButton(
        get_translation("save"),
        icon=ft.Icons.SAVE,
        on_click=save_and_back,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_start"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    # --- Кнопка отмены ---
    def cancel(e):
        settings_main(page)  # Возвращаемся к главной странице настроек

    cancel_button = ft.ElevatedButton(
        get_translation("cancel"),
        icon=ft.Icons.CANCEL,
        on_click=cancel,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_exit"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    # --- Сборка экрана настроек внешнего вида ---
    settings_content = ft.Column(
        [
            ft.Text(get_translation("appearance_title"), size=32, color=Colors["primary"], weight=ft.FontWeight.BOLD),
            # Настройка размера ячейки
            ft.Divider(),
            ft.Text(get_translation("cell_size_label"), size=20, color=Colors["primary"]),
            ft.Row(
                [
                    cell_size_slider,
                    ft.Column([preview_cell, cell_size_value_text],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                              spacing=5)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            # Выбор темы
            ft.Divider(),
            ft.Text(get_translation("theme_label"), size=20, color=Colors["primary"]),
            theme_dropdown,
            # Кнопки управления
            ft.Divider(height=30),
            save_button,
            cancel_button,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )
    page.add(settings_content)


def settings_gameplay(page: ft.Page):
    """Экран настроек - Геймплей"""
    # Получаем цвета текущей темы
    Colors = get_current_colors()
    # Перезагружаем настройки для получения актуального языка
    global user_settings
    user_settings = load_user_settings()
    page.title = f"{get_translation('game_title')} - {get_translation('settings_title')} - {get_translation('gameplay_title')}"
    page.bgcolor = Colors["bg_main_menu"]
    page.clean()
    page.scroll = ft.ScrollMode.AUTO
    # --- Выбор языка ---
    current_language = user_settings.get("language", "ru")
    language_options = []
    for code, name in SUPPORTED_LANGUAGES.items():
        # Явно задаем цвет текста для каждой опции
        option_text_widget = ft.Text(name, color=Colors["dropdown_text_color"], size=16)
        language_options.append(ft.dropdown.Option(key=code, text=name, content=option_text_widget))
    language_dropdown = ft.Dropdown(
        label=get_translation("language"),
        options=language_options,
        value=current_language,
        width=300,
        color=Colors["dropdown_text_color"],  # Цвет текста внутри Dropdown
        bgcolor=Colors["dropdown_bg_color"],  # Цвет фона Dropdown
    )

    # --- Кнопка сохранения и возврата ---
    def save_and_back(e):
        global user_settings
        user_settings["language"] = language_dropdown.value
        save_user_settings(user_settings)
        settings_main(page)  # Возвращаемся к главной странице настроек

    save_button = ft.ElevatedButton(
        get_translation("save"),
        icon=ft.Icons.SAVE,
        on_click=save_and_back,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_start"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    # --- Кнопка отмены ---
    def cancel(e):
        settings_main(page)  # Возвращаемся к главной странице настроек

    cancel_button = ft.ElevatedButton(
        get_translation("cancel"),
        icon=ft.Icons.CANCEL,
        on_click=cancel,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_exit"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    # --- Сборка экрана настроек геймплея ---
    settings_content = ft.Column(
        [
            ft.Text(get_translation("gameplay_title"), size=32, color=Colors["primary"], weight=ft.FontWeight.BOLD),
            # Выбор языка
            ft.Divider(),
            ft.Text(get_translation("language"), size=20, color=Colors["primary"]),
            language_dropdown,
            # Кнопки управления
            ft.Divider(height=30),
            save_button,
            cancel_button,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )
    page.add(settings_content)


def settings_controls(page: ft.Page):
    """Экран настроек - Управление"""
    # Получаем цвета текущей темы
    Colors = get_current_colors()
    global user_settings
    user_settings = load_user_settings()  # Перезагружаем настройки
    page.title = f"{get_translation('game_title')} - {get_translation('settings_title')} - {get_translation('controls_title')}"
    page.bgcolor = Colors["bg_main_menu"]
    page.clean()
    page.scroll = ft.ScrollMode.AUTO
    # Получаем текущие настройки управления
    current_controls = user_settings.get("controls", {})
    # Создаем копию для редактирования
    temp_controls = current_controls.copy()
    # Словарь для хранения ссылок на кнопки и текстовые элементы
    control_widgets = {}
    # Флаг для отслеживания состояния ожидания нажатия клавиши
    waiting_for_key = [False]
    # Переменная для хранения имени действия, которое настраивается
    action_being_set = [None]
    # Список действий и их переводов
    actions = [
        ("up", "move_up"),
        ("down", "move_down"),
        ("left", "move_left"),
        ("right", "move_right"),
        ("pause", "pause_game"),
    ]

    # Функция для обновления отображения клавиши
    def update_key_display(action_key, key_name):
        display_text = key_name.upper() if key_name else get_translation("key_not_set")
        if control_widgets[action_key]["text"]:
            control_widgets[action_key]["text"].value = display_text
            control_widgets[action_key]["text"].update()

    # Функция для проверки, используется ли клавиша
    def is_key_used(key_name, exclude_action=None):
        for act, k in temp_controls.items():
            if act != exclude_action and k == key_name:
                return True
        return False

    # Функция для обработки нажатия клавиши
    def on_key_assignment(e: ft.KeyboardEvent):
        if waiting_for_key[0] and action_being_set[0]:
            key_pressed = e.key.lower()
            # Исключаем системные клавиши, которые могут мешать
            if key_pressed in ["shift", "control", "alt", "meta"]:
                return
            if is_key_used(key_pressed, exclude_action=action_being_set[0]):
                # Показываем ошибку
                error_text = control_widgets[action_being_set[0]]["error"]
                if error_text:
                    error_text.value = get_translation("key_already_used")
                    error_text.visible = True
                    error_text.update()

                    # Скрываем ошибку через 2 секунды
                    def hide_error():
                        time.sleep(2)
                        if error_text:
                            error_text.visible = False
                            error_text.update()

                    threading.Thread(target=hide_error, daemon=True).start()
            else:
                temp_controls[action_being_set[0]] = key_pressed
                update_key_display(action_being_set[0], key_pressed)
                # Скрываем подсказку
                hint_text = control_widgets[action_being_set[0]]["hint"]
                if hint_text:
                    hint_text.visible = False
                    hint_text.update()
            # Сбрасываем состояние
            waiting_for_key[0] = False
            action_being_set[0] = None
            # Убираем обработчик события
            page.on_keyboard_event = None

    # Функция для начала назначения клавиши
    def start_key_assignment(e, action_key):
        if waiting_for_key[0]:
            return  # Уже ожидаем нажатия
        waiting_for_key[0] = True
        action_being_set[0] = action_key
        # Показываем подсказку
        hint_text = control_widgets[action_key]["hint"]
        if hint_text:
            hint_text.visible = True
            hint_text.update()
        # Обновляем отображение клавиши на "..."
        update_key_display(action_key, "...")
        # Устанавливаем временный обработчик событий клавиатуры
        page.on_keyboard_event = on_key_assignment

    # Создаем элементы интерфейса для каждого действия
    controls_list = []
    for action_key, translation_key in actions:
        key_name = temp_controls.get(action_key, "")
        display_text = key_name.upper() if key_name else get_translation("key_not_set")
        # Текст для отображения назначенной клавиши
        key_display_text = ft.Text(display_text, size=16, color=Colors["text_default"])
        # Подсказка "Нажмите клавишу..."
        hint_text = ft.Text(get_translation("press_key_to_assign"), size=12, color=Colors["primary"], visible=False)
        # Текст ошибки
        error_text = ft.Text("", size=12, color=Colors["button_exit"], visible=False)
        # Кнопка для назначения клавиши
        assign_button = ft.ElevatedButton(
            "...",
            on_click=lambda e, ak=action_key: start_key_assignment(e, ak),
            width=100,
            height=40,
            style=ft.ButtonStyle(
                bgcolor=Colors["button_start"],
                color="#FFFFFF",
                shape=ft.RoundedRectangleBorder(radius=5)
            )
        )
        # Сохраняем ссылки на виджеты
        control_widgets[action_key] = {
            "button": assign_button,
            "text": key_display_text,
            "hint": hint_text,
            "error": error_text
        }
        # Строка для действия
        action_row = ft.Row(
            [
                ft.Text(get_translation(translation_key), size=18, color=Colors["primary"], width=150),
                ft.Column(
                    [
                        ft.Row([key_display_text, assign_button], alignment=ft.MainAxisAlignment.START),
                        hint_text,
                        error_text
                    ],
                    spacing=2
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        controls_list.append(action_row)

    # --- Кнопка сохранения и возврата ---
    def save_and_back(e):
        global user_settings
        user_settings["controls"] = temp_controls.copy()
        save_user_settings(user_settings)
        settings_main(page)  # Возвращаемся к главной странице настроек

    save_button = ft.ElevatedButton(
        get_translation("save"),
        icon=ft.Icons.SAVE,
        on_click=save_and_back,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_start"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    # --- Кнопка сброса по умолчанию ---
    def reset_defaults(e):
        global user_settings
        # Получаем дефолтные контролы из функции load_user_settings
        default_settings = load_user_settings()
        default_controls = default_settings.get("controls", {
            "up": "w",
            "down": "s",
            "left": "a",
            "right": "d",
            "pause": "escape"
        })
        temp_controls.clear()
        temp_controls.update(default_controls)
        # Обновляем отображение для всех действий
        for action_key, _ in actions:
            key_name = temp_controls.get(action_key, "")
            update_key_display(action_key, key_name)
            # Скрываем подсказки и ошибки
            hint_widget = control_widgets.get(action_key, {}).get("hint")
            error_widget = control_widgets.get(action_key, {}).get("error")
            if hint_widget:
                hint_widget.visible = False
                hint_widget.update()
            if error_widget:
                error_widget.visible = False
                error_widget.update()
        # Сбрасываем состояние ожидания
        waiting_for_key[0] = False
        action_being_set[0] = None
        page.on_keyboard_event = None

    reset_button = ft.ElevatedButton(
        get_translation("reset_to_defaults"),
        icon=ft.Icons.RESTORE,
        on_click=reset_defaults,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_medium"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    # --- Кнопка отмены ---
    def cancel(e):
        settings_main(page)  # Возвращаемся к главной странице настроек

    cancel_button = ft.ElevatedButton(
        get_translation("cancel"),
        icon=ft.Icons.CANCEL,
        on_click=cancel,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_exit"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    # --- Сборка экрана настроек управления ---
    settings_content = ft.Column(
        [
            ft.Text(get_translation("controls_title"), size=32, color=Colors["primary"], weight=ft.FontWeight.BOLD),
            ft.Divider(),
        ] + controls_list + [
            ft.Divider(height=20),
            reset_button,
            ft.Divider(height=10),
            save_button,
            cancel_button,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )
    page.add(settings_content)


# --- Основные экраны ---
def main_menu(page: ft.Page):
    # Перезагружаем рекорды при входе в главное меню
    global best_times, user_settings
    best_times = load_best_times()
    user_settings = load_user_settings()  # Перезагружаем настройки, включая тему и язык
    # Получаем цвета текущей темы
    Colors = get_current_colors()
    page.title = f"{get_translation('game_title')} - {get_translation('main_menu_title')}"
    page.bgcolor = Colors["bg_main_menu"]
    page.window_always_on_top = True
    page.window_maximized = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.clean()

    # --- Музыка ---
    # Создаем аудиоплеер, если файл существует
    # audio_player = None
    # if os.path.exists(MUSIC_FILE):
    #     try:
    #         import flet.audio as fa
    #         audio_player = fa.Audio(
    #             src=MUSIC_FILE,
    #             autoplay=user_settings.get("music_enabled", True),
    #             volume=user_settings.get("music_volume", 0.5),
    #             on_loaded=lambda e: print("Music loaded"),
    #             on_duration_changed=lambda e: print(f"Duration: {e.data}"),
    #             on_position_changed=lambda e: print(f"Position: {e.data}"),
    #             on_state_changed=lambda e: print(f"State: {e.data}"),
    #             on_seek_complete=lambda e: print("Seek complete"),
    #         )
    #         page.overlay.append(audio_player)
    #         page.update()
    #     except ImportError:
    #         print("flet.audio не доступен")
    #         audio_player = None
    #     except Exception as e:
    #         print(f"Ошибка создания аудиоплеера: {e}")
    #         audio_player = None
    # else:
    #     print(f"Файл музыки не найден: {MUSIC_FILE}")
    #     audio_player = None
    def start_game(e):
        mode_selection_screen(page)

    def settings(e):
        settings_main(page)  # Переходим к главной странице настроек

    # --- Диалог подтверждения выхода ---
    def confirm_exit(e):
        confirm_dialog.open = True
        page.update()

    # Диалоговое окно подтверждения выхода
    def close_exit_dialog(confirm: bool):
        confirm_dialog.open = False
        page.update()
        if confirm:
            # if audio_player:
            #     try:
            #         audio_player.pause()
            #     except:
            #         pass
            page.window.destroy()  # Используем window_destroy для корректного закрытия

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(get_translation("exit_confirmation"), color=Colors["primary"]),
        content=ft.Text(get_translation("exit_question"), color=Colors["text_default"]),
        actions=[
            ft.TextButton(get_translation("yes"), on_click=lambda e: close_exit_dialog(True)),
            ft.TextButton(get_translation("no"), on_click=lambda e: close_exit_dialog(False)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog = confirm_dialog
    # Отображение лучших времен для каждого уровня
    records_text = ft.Column(
        [
            ft.Text(get_translation("records"), size=20, color=Colors["record_text"], weight=ft.FontWeight.BOLD),
            ft.Text(f"{get_translation('easy')}: {format_time(best_times['Легкий'])}", size=16,
                    color=Colors["text_default"]),
            ft.Text(f"{get_translation('medium')}: {format_time(best_times['Средний'])}", size=16,
                    color=Colors["text_default"]),
            ft.Text(f"{get_translation('hard')}: {format_time(best_times['Высокий'])}", size=16,
                    color=Colors["text_default"]),
        ],
        spacing=5
    )
    menu = ft.Column(
        [
            ft.Text(get_translation("game_title"), size=48, weight=ft.FontWeight.BOLD, color=Colors["primary"]),
            records_text,
            ft.ElevatedButton(
                get_translation("start_game"),
                on_click=start_game,
                width=250,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor=Colors["button_start"],
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            ft.ElevatedButton(
                get_translation("settings"),
                on_click=settings,
                width=250,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor=Colors["button_start"],
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            ft.ElevatedButton(
                get_translation("exit"),
                on_click=confirm_exit,  # Используем confirm_exit вместо прямого выхода
                width=250,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor=Colors["button_exit"],
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
    # Получаем цвета текущей темы
    Colors = get_current_colors()
    page.title = f"{get_translation('game_title')} - {get_translation('mode_selection_title')}"
    page.bgcolor = Colors["bg_main_menu"]
    page.clean()

    def select_single_player(e):
        difficulty_selection_screen(page)

    def select_competitive(e):
        # Переход к новому экрану выбора сложности для соревновательного режима
        competitive_difficulty_selection_screen_split(page)

    def back_to_menu(e):
        main_menu(page)

    menu = ft.Column(
        [
            ft.Text(get_translation("select_mode"), size=36, weight=ft.FontWeight.BOLD, color=Colors["primary"]),
            ft.ElevatedButton(
                get_translation("single_player"),
                on_click=select_single_player,
                width=300,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor=Colors["button_start"],
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            ft.ElevatedButton(
                get_translation("competitive"),
                on_click=select_competitive,
                width=300,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor=Colors["button_medium"],  # Используем другой цвет
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                # Убираем disabled=True
            ),
            ft.ElevatedButton(
                get_translation("back"),
                on_click=back_to_menu,
                width=300,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor=Colors["button_exit"],
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


# --- Новый экран выбора сложности для соревновательного режима ---
def competitive_difficulty_selection_screen_split(page: ft.Page):
    """Экран выбора сложности для соревновательного режима (Split Screen)"""
    Colors = get_current_colors()
    page.title = f"{get_translation('game_title')} - {get_translation('difficulty_selection_title')} - {get_translation('competitive')}"
    page.bgcolor = Colors["bg_main_menu"]
    page.clean()

    def start_competitive_game(difficulty):
        settings = DIFFICULTY_SETTINGS[difficulty]
        match_seed = random.randint(1, 1000000)
        # Вызов нового экрана игры
        competitive_game_screen_split(page, settings["rows"], settings["cols"], difficulty, seed=match_seed)

    def back_to_mode_selection(e):
        mode_selection_screen(page)

    easy_button = ft.ElevatedButton(
        get_translation("easy_level"),
        on_click=lambda e: start_competitive_game("Легкий"),
        width=300,
        height=60,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_easy"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    medium_button = ft.ElevatedButton(
        get_translation("medium_level"),
        on_click=lambda e: start_competitive_game("Средний"),
        width=300,
        height=60,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_medium"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    hard_button = ft.ElevatedButton(
        get_translation("hard_level"),
        on_click=lambda e: start_competitive_game("Высокий"),
        width=300,
        height=60,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_hard"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    back_button = ft.ElevatedButton(
        get_translation("back"),
        on_click=back_to_mode_selection,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_exit"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    menu = ft.Column(
        [
            ft.Text(f"{get_translation('select_difficulty')} - {get_translation('competitive')}", size=36,
                    weight=ft.FontWeight.BOLD, color=Colors["primary"]),
            easy_button,
            medium_button,
            hard_button,
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            back_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )
    page.add(menu)


# --- Новый экран соревновательной игры (Split Screen) ---
def competitive_game_screen_split(page: ft.Page, maze_rows, maze_cols, difficulty_level, seed=None):
    """
    Экран соревновательной игры (одновременная игра на одном экране)
    :param page: страница Flet
    :param maze_rows: количество строк в лабиринте
    :param maze_cols: количество столбцов в лабиринте
    :param difficulty_level: уровень сложности
    :param seed: seed для генерации лабиринта
    """
    restart_seed = seed if seed is not None else random.randint(1, 1000000)
    Colors = get_current_colors()

    # Загружаем настройки управления для обоих игроков
    # Игрок 1: Стрелки + Enter для паузы
    # Игрок 2: WASD + Space для паузы
    controls_p1 = {
        "up": "Arrow Up",  # Flet использует полные названия клавиш
        "down": "Arrow Down",
        "left": "Arrow Left",
        "right": "Arrow Right",
        "pause": "Enter"  # Уникальная пауза для игрока 1
    }
    controls_p2 = {
        "up": "W",
        "down": "S",
        "left": "A",
        "right": "D",
        "pause": "Space"  # Уникальная пауза для игрока 2
    }

    current_settings = load_user_settings()
    base_cell_size = current_settings.get("cell_size", DEFAULT_CELL_SIZE)
    page.bgcolor = Colors["bg_game"]
    page.window_maximized = True
    page.clean()

    # --- Состояние игры ---
    game_state = {
        "winner": None,  # "player1", "player2", или None
        "player1_finished": False,
        "player2_finished": False,
        "start_time": time.time(),
        "player1_time": None,
        "player2_time": None,
        "game_active": True,
        "game_paused": False
    }

    # --- Генерация лабиринта ---
    maze = init_maze(maze_rows, maze_cols)
    if seed is not None:
        random.seed(seed)
    generate_maze_dfs(maze, maze_rows, maze_cols)
    if seed is not None:
        random.seed()  # Сброс seed

    # --- Размеры и канвас ---
    size_factor = max(maze_rows, maze_cols)
    if size_factor > 20:
        reduction = (size_factor - 20) // 3
        cell_size = max(CELL_SIZE_MIN, base_cell_size - reduction)
    else:
        cell_size = base_cell_size

    MAX_CANVAS_WIDTH = 1400
    MAX_CANVAS_HEIGHT = 750
    potential_canvas_width = cell_size * maze_cols
    potential_canvas_height = cell_size * maze_rows
    if potential_canvas_width > MAX_CANVAS_WIDTH or potential_canvas_height > MAX_CANVAS_HEIGHT:
        required_cell_size_w = MAX_CANVAS_WIDTH // maze_cols if maze_cols > 0 else cell_size
        required_cell_size_h = MAX_CANVAS_HEIGHT // maze_rows if maze_rows > 0 else cell_size
        cell_size = max(CELL_SIZE_MIN, int(min(required_cell_size_w, required_cell_size_h, cell_size)))

    canvas_width = cell_size * maze_cols
    canvas_height = cell_size * maze_rows
    canvas = ft.Stack(width=canvas_width, height=canvas_height)
    game_container = ft.Container(
        content=canvas,
        alignment=ft.alignment.center,
        expand=True
    )

    # --- UI элементы ---
    timer_text_ref = ft.Ref[ft.Text]()
    timer_text = ft.Text(
        f"{get_translation('time')}: 00:00.00",
        size=24,
        color=Colors["timer"],
        weight=ft.FontWeight.BOLD,
        ref=timer_text_ref,
    )
    level_text = ft.Text(
        f"{get_translation('level')}: {difficulty_level}",
        size=20,
        color=Colors["level"],
        weight=ft.FontWeight.BOLD
    )

    # Индикаторы игроков
    player1_indicator = ft.Text(
        f"{get_translation('player')} 1 (Стрелки)",
        size=18,
        color=Colors.get("player1_color", Colors["player"]),  # Используем player если player1_color не определен
        weight=ft.FontWeight.BOLD
    )
    player2_indicator = ft.Text(
        f"{get_translation('player')} 2 (WASD)",
        size=18,
        color=Colors.get("player2_color", "#0000FF"),  # Используем синий если player2_color не определен
        weight=ft.FontWeight.BOLD
    )

    # --- Отрисовка лабиринта ---
    for y in range(maze_rows):
        for x in range(maze_cols):
            if maze["cells"][y][x]:
                canvas.controls.append(
                    ft.Container(
                        left=x * cell_size,
                        top=y * cell_size,
                        width=cell_size,
                        height=cell_size,
                        bgcolor=Colors["path"],
                    )
                )
    for y in range(maze_rows + 1):
        for x in range(maze_cols):
            if maze["horizontal_walls"][y][x]:
                canvas.controls.append(
                    ft.Container(
                        left=x * cell_size,
                        top=y * cell_size - 1,
                        width=cell_size,
                        height=2,
                        bgcolor=Colors["wall"]
                    )
                )
    for y in range(maze_rows):
        for x in range(maze_cols + 1):
            if maze["vertical_walls"][y][x]:
                canvas.controls.append(
                    ft.Container(
                        left=x * cell_size - 1,
                        top=y * cell_size,
                        width=2,
                        height=cell_size,
                        bgcolor=Colors["wall"]
                    )
                )

    # --- Позиции игроков и выхода ---
    # Начальные позиции
    player1_x, player1_y = 0, 0
    player2_x, player2_y = 0, 0
    exit_x = maze_cols - 1
    exit_y = maze_rows - 1

    # Случайные стартовые позиции (если включено)
    if user_settings.get("random_start", False):
        # Игрок 1
        while True:
            player1_x = random.randint(0, maze_cols - 1)
            player1_y = random.randint(0, maze_rows - 1)
            if (player1_x, player1_y) != (exit_x, exit_y):
                break
        # Игрок 2 (не совпадает с выходом и игроком 1)
        while True:
            player2_x = random.randint(0, maze_cols - 1)
            player2_y = random.randint(0, maze_rows - 1)
            if (player2_x, player2_y) != (exit_x, exit_y) and (player2_x, player2_y) != (player1_x, player1_y):
                break

    # --- Создание элементов игроков и выхода ---
    exit_cell = ft.Container(
        left=exit_x * cell_size,
        top=exit_y * cell_size,
        width=cell_size,
        height=cell_size,
        bgcolor=Colors["exit"],
    )
    canvas.controls.append(exit_cell)

    player1 = ft.Container(
        left=player1_x * cell_size,
        top=player1_y * cell_size,
        width=cell_size,
        height=cell_size,
        bgcolor=Colors.get("player1_color", Colors["player"]),  # Используем player если player1_color не определен
    )
    canvas.controls.append(player1)

    player2 = ft.Container(
        left=player2_x * cell_size,
        top=player2_y * cell_size,
        width=cell_size,
        height=cell_size,
        bgcolor=Colors.get("player2_color", "#0000FF"),  # Используем синий если player2_color не определен
    )
    canvas.controls.append(player2)

    # --- Оверлей и диалоги ---
    overlay_dark = ft.Container(
        visible=False,
        expand=True,
        bgcolor=Colors["overlay_dark"],
    )

    # --- Функции управления игрой ---
    def finish_game(winner):
        """Завершение игры и отображение результатов"""
        if game_state["winner"] is not None:  # Игра уже закончена
            return

        game_state["winner"] = winner
        game_state["game_active"] = False

        # Записываем время, если игрок только что финишировал
        current_time = time.time() - game_state["start_time"]
        if winner == "player1" and not game_state["player1_finished"]:
            game_state["player1_time"] = current_time
            game_state["player1_finished"] = True
        elif winner == "player2" and not game_state["player2_finished"]:
            game_state["player2_time"] = current_time
            game_state["player2_finished"] = True

        # Если второй игрок еще не финишировал, записываем его время как "не финишировал"
        if winner == "player1" and not game_state["player2_finished"]:
            game_state["player2_time"] = None  # Или можно оставить текущее время
        elif winner == "player2" and not game_state["player1_finished"]:
            game_state["player1_time"] = None  # Или можно оставить текущее время

        # Отображение результатов
        winner_text = ft.Text(
            f"{get_translation('winner')}: {get_translation('player')} {1 if winner == 'player1' else 2}",
            size=32,
            color=Colors.get(f"player{1 if winner == 'player1' else 2}_color", "#FFFFFF"),
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        p1_time_text = ft.Text(
            f"{get_translation('player')} 1: {format_time(game_state['player1_time']) if game_state['player1_time'] is not None else 'Не завершено'}",
            size=20,
            color=Colors.get("player1_color", Colors["player"]),
            text_align=ft.TextAlign.CENTER
        )
        p2_time_text = ft.Text(
            f"{get_translation('player')} 2: {format_time(game_state['player2_time']) if game_state['player2_time'] is not None else 'Не завершено'}",
            size=20,
            color=Colors.get("player2_color", "#0000FF"),
            text_align=ft.TextAlign.CENTER
        )

        victory_dialog = ft.Container(
            visible=True,
            width=400,
            height=350,
            bgcolor=Colors["dialog_bg"],
            border_radius=20,
            content=ft.Column(
                [
                    ft.Text(get_translation("congratulations"), size=32, color=Colors["record_text"],
                            weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    winner_text,
                    p1_time_text,
                    p2_time_text,
                    ft.Divider(),
                    ft.ElevatedButton(
                        get_translation("new_level"),
                        on_click=lambda e: restart_match(page, maze_rows, maze_cols, difficulty_level),
                        width=250,
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor=Colors["button_easy"],
                            color="#FFFFFF",
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    ),
                    ft.ElevatedButton(
                        get_translation("to_menu"),
                        on_click=lambda e: main_menu(page),
                        width=250,
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor=Colors["button_exit"],
                            color="#FFFFFF",
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            alignment=ft.alignment.center
        )

        overlay_dark.visible = True
        overlay_dark.update()
        page.add(victory_dialog)  # Добавляем диалог поверх всего

    def move_player(player_num, dx, dy):
        """Движение игрока"""
        if not game_state["game_active"] or game_state["game_paused"]:
            return

        nonlocal player1_x, player1_y, player2_x, player2_y

        if player_num == 1:
            if game_state["player1_finished"]:
                return
            new_x, new_y = player1_x + dx, player1_y + dy
            # Проверки границ и стен
            if not (0 <= new_x < maze_cols and 0 <= new_y < maze_rows):
                return
            if dx == 1 and maze["vertical_walls"][player1_y][player1_x + 1]:
                return
            if dx == -1 and maze["vertical_walls"][player1_y][player1_x]:
                return
            if dy == 1 and maze["horizontal_walls"][player1_y + 1][player1_x]:
                return
            if dy == -1 and maze["horizontal_walls"][player1_y][player1_x]:
                return
            player1_x, player1_y = new_x, new_y
            player1.left = player1_x * cell_size
            player1.top = player1_y * cell_size
            player1.update()

            if (player1_x, player1_y) == (exit_x, exit_y):
                game_state["player1_finished"] = True
                game_state["player1_time"] = time.time() - game_state["start_time"]
                finish_game("player1")

        elif player_num == 2:
            if game_state["player2_finished"]:
                return
            new_x, new_y = player2_x + dx, player2_y + dy
            # Проверки границ и стен
            if not (0 <= new_x < maze_cols and 0 <= new_y < maze_rows):
                return
            if dx == 1 and maze["vertical_walls"][player2_y][player2_x + 1]:
                return
            if dx == -1 and maze["vertical_walls"][player2_y][player2_x]:
                return
            if dy == 1 and maze["horizontal_walls"][player2_y + 1][player2_x]:
                return
            if dy == -1 and maze["horizontal_walls"][player2_y][player2_x]:
                return
            player2_x, player2_y = new_x, new_y
            player2.left = player2_x * cell_size
            player2.top = player2_y * cell_size
            player2.update()

            if (player2_x, player2_y) == (exit_x, exit_y):
                game_state["player2_finished"] = True
                game_state["player2_time"] = time.time() - game_state["start_time"]
                finish_game("player2")

    def timer_thread():
        """Поток таймера"""
        while game_state["game_active"]:
            try:
                if not game_state["game_paused"]:
                    current_time = time.time() - game_state["start_time"]
                    if timer_text_ref.current:
                        timer_text_ref.current.value = f"{get_translation('time')}: {format_time(current_time)}"
                        # page.update() вызывается внутри on_key для оптимизации
                time.sleep(0.05)  # Обновление таймера 20 раз в секунду
            except:
                break

    def pause_game():
        """Пауза в игре"""
        if not game_state["game_active"]:
            return
        game_state["game_paused"] = True
        overlay_dark.visible = True
        overlay_dark.update()
        # Можно добавить диалог паузы, но для простоты просто оверлей

    def resume_game():
        """Продолжение игры"""
        game_state["game_paused"] = False
        overlay_dark.visible = False
        overlay_dark.update()
        game_state["start_time"] = time.time() - (
            game_state["player1_time"] if game_state["player1_time"] else 0)  # Простая логика возобновления

    def restart_match(page, rows, cols, difficulty):
        """Перезапуск матча"""
        # Останавливаем текущую игру
        game_state["game_active"] = False
        # Генерируем НОВЫЙ seed
        new_seed = random.randint(1, 1000000)
        competitive_game_screen_split(page, rows, cols, difficulty, seed=new_seed)

    def on_key(e: ft.KeyboardEvent):
        """Обработка нажатий клавиш для обоих игроков"""
        key = e.key
        # print(f"Key pressed: {key}") # Для отладки

        # Обработка паузы для обоих игроков
        if key == controls_p1["pause"] or key == controls_p2["pause"]:
            if game_state["game_paused"]:
                resume_game()
            else:
                pause_game()
            return  # Важно: return после обработки паузы

        if not game_state["game_active"] or game_state["game_paused"] or game_state["winner"] is not None:
            return

        # Обработка движения Игрока 1 (Стрелки)
        if key == controls_p1["up"]:
            move_player(1, 0, -1)
        elif key == controls_p1["down"]:
            move_player(1, 0, 1)
        elif key == controls_p1["left"]:
            move_player(1, -1, 0)
        elif key == controls_p1["right"]:
            move_player(1, 1, 0)

        # Обработка движения Игрока 2 (WASD)
        elif key == controls_p2["up"]:
            move_player(2, 0, -1)
        elif key == controls_p2["down"]:
            move_player(2, 0, 1)
        elif key == controls_p2["left"]:
            move_player(2, -1, 0)
        elif key == controls_p2["right"]:
            move_player(2, 1, 0)

        # Обновляем таймер после любого движения
        if game_state["game_active"] and not game_state["game_paused"]:
            current_time = time.time() - game_state["start_time"]
            if timer_text_ref.current:
                timer_text_ref.current.value = f"{get_translation('time')}: {format_time(current_time)}"
                page.update()  # Обновляем страницу после каждого движения для немедленного отображения таймера

    # --- Запуск игры ---
    threading.Thread(target=timer_thread, daemon=True).start()
    page.on_keyboard_event = on_key
    # page.window.preventDefault = True # Попытка захватить все события клавиатуры (может не работать везде)

    # --- Добавление элементов на страницу ---
    top_row = ft.Row([player1_indicator, timer_text, player2_indicator, level_text],
                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    page.add(
        top_row,
        ft.Stack([
            game_container,
            overlay_dark,
            # Диалог победы будет добавлен динамически
        ])
    )


# --- Глобальные переменные для хранения состояния переключателей на экране выбора сложности ---
difficulty_screen_settings = {
    "show_timer": True,  # Значение по умолчанию
    "random_start": False  # Значение по умолчанию
}


def difficulty_selection_screen(page: ft.Page):
    """Экран выбора сложности"""
    # Получаем цвета текущей темы
    Colors = get_current_colors()
    page.title = f"{get_translation('game_title')} - {get_translation('difficulty_selection_title')}"
    page.bgcolor = Colors["bg_main_menu"]
    page.clean()
    # Инициализируем состояние переключателей для этого экрана из сохраненных значений
    global user_settings, difficulty_screen_settings
    # Загружаем последние сохраненные настройки пользователя
    user_settings = load_user_settings()
    # Инициализируем состояние переключателей экрана выбора сложности
    difficulty_screen_settings["random_start"] = user_settings.get("random_start", False)
    # Для show_timer используем отдельное состояние экрана, инициализируем из user_settings
    difficulty_screen_settings["show_timer"] = True  # По умолчанию показываем таймер

    def start_with_difficulty(difficulty):
        # Сохраняем текущее состояние переключателей перед запуском игры
        user_settings["random_start"] = random_start_switch.value
        save_user_settings(user_settings)
        settings = DIFFICULTY_SETTINGS[difficulty]
        # Генерируем seed для этого запуска уровня
        level_seed = random.randint(1, 1000000)
        # Передаем настройки отображения таймера в game_screen
        game_screen(page, settings["rows"], settings["cols"], difficulty, seed=level_seed,
                    show_timer=show_timer_switch.value)

    def back_to_mode_selection(e):
        mode_selection_screen(page)

    # Создаем кнопки сложности
    easy_button = ft.ElevatedButton(
        get_translation("easy_level"),
        on_click=lambda e: start_with_difficulty("Легкий"),
        width=300,
        height=60,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_easy"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    medium_button = ft.ElevatedButton(
        get_translation("medium_level"),
        on_click=lambda e: start_with_difficulty("Средний"),
        width=300,
        height=60,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_medium"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    hard_button = ft.ElevatedButton(
        get_translation("hard_level"),
        on_click=lambda e: start_with_difficulty("Высокий"),
        width=300,
        height=60,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_hard"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    # --- Переключатели ---
    # Переключатель случайной стартовой позиции
    random_start_switch = ft.Switch(
        label=get_translation("random_start_position"),
        value=difficulty_screen_settings["random_start"],
        active_color=Colors["button_start"],
        label_style=ft.TextStyle(color=Colors["switch_label_color"]),
    )
    # Переключатель показа таймера (только для текущего уровня)
    show_timer_switch = ft.Switch(
        label=get_translation("show_timer"),
        value=difficulty_screen_settings["show_timer"],
        active_color=Colors["button_start"],
        label_style=ft.TextStyle(color=Colors["switch_label_color"]),
    )
    back_button = ft.ElevatedButton(
        get_translation("back"),
        on_click=back_to_mode_selection,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=Colors["button_exit"],
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    # --- Новое расположение элементов ---
    # Левая колонка - кнопки сложности
    left_column = ft.Column(
        [
            easy_button,
            medium_button,
            hard_button,
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    # Правая колонка - переключатели
    right_column = ft.Column(
        [
            random_start_switch,
            show_timer_switch,
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    # Объединяем левую и правую колонки в одну строку
    main_row = ft.Row(
        [
            ft.Container(
                content=left_column,
                alignment=ft.alignment.center_right,
                expand=True,
            ),
            ft.Container(
                content=right_column,
                alignment=ft.alignment.center_left,
                expand=True,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )
    # Заголовок и кнопка "Назад" остаются в центре
    menu = ft.Column(
        [
            ft.Text(get_translation("select_difficulty"), size=36, weight=ft.FontWeight.BOLD, color=Colors["primary"]),
            main_row,
            ft.Container(
                content=back_button,
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=30),  # Отступ сверху для кнопки "Назад"
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30,
        expand=True,
    )
    page.add(menu)


def game_screen(page: ft.Page, maze_rows, maze_cols, difficulty_level, seed=None, show_timer=True):
    """
    Экран игры
    :param page: страница Flet
    :param maze_rows: количество строк в лабиринте
    :param maze_cols: количество столбцов в лабиринте
    :param difficulty_level: уровень сложности ("Легкий", "Средний", "Высокий")
    :param seed: seed для генерации лабиринта (для перезапуска того же лабиринта)
    :param show_timer: показывать ли таймер (передается из difficulty_selection_screen)
    """
    # Определяем seed для перезапуска
    restart_seed = seed if seed is not None else random.randint(1, 1000000)
    # Получаем цвета текущей темы
    Colors = get_current_colors()
    # Получаем настройки управления
    global user_settings
    controls = user_settings.get("controls", {
        "up": "w",
        "down": "s",
        "left": "a",
        "right": "d",
        "pause": "escape"
    })
    # --- Используем размер ячейки из настроек пользователя ---
    current_settings = load_user_settings()
    base_cell_size = current_settings.get("cell_size", DEFAULT_CELL_SIZE)
    page.bgcolor = Colors["bg_game"]
    page.window_maximized = True
    page.clean()
    maze = init_maze(maze_rows, maze_cols)
    # Устанавливаем seed для генерации, если он передан
    if seed is not None:
        random.seed(seed)
    generate_maze_dfs(maze, maze_rows, maze_cols)
    # Сбросим seed
    if seed is not None:
        random.seed()
    start_time = time.time()
    timer_active = [True]
    timer_text_ref = ft.Ref[ft.Text]()
    game_active = [True]
    game_paused = [False]
    size_factor = max(maze_rows, maze_cols)
    if size_factor > 20:
        reduction = (size_factor - 20) // 3
        cell_size = max(CELL_SIZE_MIN, base_cell_size - reduction)
    else:
        cell_size = base_cell_size
    MAX_CANVAS_WIDTH = 1400
    MAX_CANVAS_HEIGHT = 750
    potential_canvas_width = cell_size * maze_cols
    potential_canvas_height = cell_size * maze_rows
    if potential_canvas_width > MAX_CANVAS_WIDTH or potential_canvas_height > MAX_CANVAS_HEIGHT:
        required_cell_size_w = MAX_CANVAS_WIDTH // maze_cols if maze_cols > 0 else cell_size
        required_cell_size_h = MAX_CANVAS_HEIGHT // maze_rows if maze_rows > 0 else cell_size
        cell_size = max(
            CELL_SIZE_MIN,
            int(min(required_cell_size_w, required_cell_size_h, cell_size))
        )
    canvas_width = cell_size * maze_cols
    canvas_height = cell_size * maze_rows
    canvas = ft.Stack(width=canvas_width, height=canvas_height)
    game_container = ft.Container(
        content=canvas,
        alignment=ft.alignment.center,
        expand=True
    )
    # Создаем таймер, но не добавляем его на страницу сразу
    timer_text = ft.Text(
        f"{get_translation('time')}: 00:00.00",
        size=24,
        color=Colors["timer"],
        weight=ft.FontWeight.BOLD,
        ref=timer_text_ref,
        visible=show_timer  # Устанавливаем видимость на основе параметра
    )
    level_text = ft.Text(
        f"{get_translation('level')}: {difficulty_level}",
        size=20,
        color=Colors["level"],
        weight=ft.FontWeight.BOLD
    )
    for y in range(maze_rows):
        for x in range(maze_cols):
            if maze["cells"][y][x]:
                canvas.controls.append(
                    ft.Container(
                        left=x * cell_size,
                        top=y * cell_size,
                        width=cell_size,
                        height=cell_size,
                        bgcolor=Colors["path"],
                    )
                )
    for y in range(maze_rows + 1):
        for x in range(maze_cols):
            if maze["horizontal_walls"][y][x]:
                canvas.controls.append(
                    ft.Container(
                        left=x * cell_size,
                        top=y * cell_size - 1,
                        width=cell_size,
                        height=2,
                        bgcolor=Colors["wall"]
                    )
                )
    for y in range(maze_rows):
        for x in range(maze_cols + 1):
            if maze["vertical_walls"][y][x]:
                canvas.controls.append(
                    ft.Container(
                        left=x * cell_size - 1,
                        top=y * cell_size,
                        width=2,
                        height=cell_size,
                        bgcolor=Colors["wall"]
                    )
                )
    # --- Начальная позиция игрока ---
    player_x = 0
    player_y = 0
    # --- Позиция выхода ---
    exit_x = maze_cols - 1
    exit_y = maze_rows - 1
    # --- Проверка на случайную стартовую позицию ---
    # Используем значение из глобальной переменной difficulty_screen_settings
    global difficulty_screen_settings
    if difficulty_screen_settings.get("random_start", False):
        # Генерируем случайную позицию, которая не совпадает с выходом
        while True:
            player_x = random.randint(0, maze_cols - 1)
            player_y = random.randint(0, maze_rows - 1)
            if (player_x, player_y) != (exit_x, exit_y):
                break
    exit_cell = ft.Container(
        left=exit_x * cell_size,
        top=exit_y * cell_size,
        width=cell_size,
        height=cell_size,
        bgcolor=Colors["exit"],
    )
    canvas.controls.append(exit_cell)
    player = ft.Container(
        left=player_x * cell_size,
        top=player_y * cell_size,
        width=cell_size,
        height=cell_size,
        bgcolor=Colors["player"],
    )
    canvas.controls.append(player)
    overlay_dark = ft.Container(
        visible=False,
        expand=True,
        bgcolor=Colors["overlay_dark"],
    )
    time_text = ft.Text("", size=18, color=Colors["record_text"], text_align=ft.TextAlign.CENTER)
    record_text = ft.Text("", size=16, color=Colors["record_new"], text_align=ft.TextAlign.CENTER)

    # --- Функция перезапуска уровня (новый случайный лабиринт) ---
    def restart_game_new_level(page, rows, cols, difficulty):
        timer_active[0] = False
        # Генерируем НОВЫЙ seed для нового уровня
        new_seed = random.randint(1, 1000000)
        game_screen(page, rows, cols, difficulty, seed=new_seed, show_timer=show_timer)

    # --- Функция перезапуска того же уровня ---
    def restart_game_same_level(page, rows, cols, difficulty):
        timer_active[0] = False
        # Используем тот же seed
        game_screen(page, rows, cols, difficulty, seed=restart_seed, show_timer=show_timer)

    victory_dialog = ft.Container(
        visible=False,
        width=400,
        height=320,  # Увеличил высоту для дополнительной кнопки
        bgcolor=Colors["dialog_bg"],
        border_radius=20,
        content=ft.Column(
            [
                ft.Text(get_translation("congratulations"), size=32, color=Colors["record_text"],
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
                ft.Text(get_translation("you_won"), size=20, color=Colors["text_default"],
                        text_align=ft.TextAlign.CENTER),
                ft.Text(f"{get_translation('level')}: {difficulty_level}", size=16, color=Colors["record_text"],
                        text_align=ft.TextAlign.CENTER),
                time_text,
                record_text,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            get_translation("restart_level"),  # Перезапустить тот же уровень
                            on_click=lambda e: restart_game_same_level(page, maze_rows, maze_cols, difficulty_level),
                            width=180,
                            height=45,
                            style=ft.ButtonStyle(
                                bgcolor=Colors["button_medium"],
                                color="#FFFFFF",
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            get_translation("new_level"),  # Новый уровень (новый лабиринт)
                            on_click=lambda e: restart_game_new_level(page, maze_rows, maze_cols, difficulty_level),
                            width=180,
                            height=45,
                            style=ft.ButtonStyle(
                                bgcolor=Colors["button_easy"],
                                color="#FFFFFF",
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        ),
                        ft.ElevatedButton(
                            get_translation("to_menu"),
                            on_click=lambda e: main_menu(page),
                            width=180,
                            height=45,
                            style=ft.ButtonStyle(
                                bgcolor=Colors["button_exit"],
                                color="#FFFFFF",
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10  # Уменьшил spacing между элементами
        ),
        alignment=ft.alignment.center
    )
    # Меню паузы (БЕЗ кнопки "Настройки")
    pause_menu = ft.Container(
        visible=False,
        width=400,
        height=250,
        bgcolor=Colors["dialog_bg"],
        border_radius=20,
        content=ft.Column(
            [
                ft.Text(get_translation("pause"), size=32, color=Colors["record_text"], weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton(
                    get_translation("continue"),
                    on_click=lambda e: resume_game(),
                    width=250,
                    height=45,
                    style=ft.ButtonStyle(
                        bgcolor=Colors["button_easy"],
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
                ft.ElevatedButton(
                    get_translation("restart_level"),
                    on_click=lambda e: restart_game_same_level(page, maze_rows, maze_cols, difficulty_level),
                    # Перезапуск того же
                    width=250,
                    height=45,
                    style=ft.ButtonStyle(
                        bgcolor=Colors["button_medium"],
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
                ft.ElevatedButton(
                    get_translation("exit_to_lobby"),
                    on_click=lambda e: main_menu(page),
                    width=250,
                    height=45,
                    style=ft.ButtonStyle(
                        bgcolor=Colors["button_exit"],
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center
    )

    def restart_game(page, rows, cols, difficulty):
        timer_active[0] = False
        # Перезапуск игры с теми же параметрами И тем же seed
        game_screen(page, rows, cols, difficulty, seed=restart_seed, show_timer=show_timer)

    def move(dx, dy):
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
        if (player_x, player_y) == (exit_x, exit_y):
            timer_active[0] = False
            final_time = time.time() - start_time
            game_active[0] = False
            is_record = final_time < best_times[difficulty_level]
            if is_record:
                best_times[difficulty_level] = final_time
                save_best_times(best_times)
            time_text.value = f"{get_translation('your_time')}: {format_time(final_time)}"
            record_text.value = get_translation(
                "new_record") if is_record else f"{get_translation('best_time')} ({difficulty_level}): {format_time(best_times[difficulty_level])}"
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
                # Обновляем таймер только если он должен отображаться и игра не на паузе
                if timer_text_ref.current and not game_paused[0] and show_timer:
                    timer_text_ref.current.value = f"{get_translation('time')}: {format_time(current_time)}"
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
        # Обработка паузы
        if key == controls["pause"].lower():
            if game_paused[0]:
                resume_game()
            else:
                pause_game()
        elif not game_paused[0]:
            # Обработка движения
            if key == controls["up"].lower():
                move(0, -1)
            elif key == controls["down"].lower():
                move(0, 1)
            elif key == controls["left"].lower():
                move(-1, 0)
            elif key == controls["right"].lower():
                move(1, 0)

    threading.Thread(target=timer_thread, daemon=True).start()
    page.on_keyboard_event = on_key
    # Добавляем таймер и игровое поле на страницу
    # Таймер добавляется только если show_timer == True
    # Но мы создаем его всегда, чтобы иметь ссылку на него
    top_row = ft.Row([timer_text, level_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    page.add(
        top_row,
        ft.Stack([
            game_container,
            overlay_dark,
            ft.Container(
                content=victory_dialog,
                alignment=ft.alignment.center,
                expand=True
            ),
            ft.Container(
                content=pause_menu,
                alignment=ft.alignment.center,
                expand=True
            )
        ])
    )


def main(page: ft.Page):
    main_menu(page)


ft.app(target=main)
