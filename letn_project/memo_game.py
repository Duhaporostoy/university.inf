import flet as ft
import random
import asyncio

CELL_SIZE = 30
MOVE_INTERVAL = 0.1  # Интервал перемещения при удержании клавиши

# Инициализация стен лабиринта
def init_maze(rows, cols):
    return {
        "cells": [[False] * cols for _ in range(rows)],
        "vertical_walls": [[True] * (cols + 1) for _ in range(rows)],
        "horizontal_walls": [[True] * cols for _ in range(rows + 1)]
    }

# Генерация лабиринта через DFS
def generate_maze_dfs(maze, rows, cols):
    visited = [[False] * cols for _ in range(rows)]

    def carve(x, y):
        visited[y][x] = True
        maze["cells"][y][x] = True
        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(dirs)

        for dx, dy in dirs:
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

# Главное приложение
def main(page: ft.Page):
    page.bgcolor = "#000000"
    page.title = "Maze Game"

    async def start_game(rows, cols):
        page.clean()

        maze = init_maze(rows, cols)
        generate_maze_dfs(maze, rows, cols)

        canvas = ft.Stack(width=cols * CELL_SIZE, height=rows * CELL_SIZE)

        # Рисуем проходы
        for y in range(rows):
            for x in range(cols):
                if maze["cells"][y][x]:
                    canvas.controls.append(
                        ft.Container(
                            left=x * CELL_SIZE,
                            top=y * CELL_SIZE,
                            width=CELL_SIZE,
                            height=CELL_SIZE,
                            bgcolor="#0000ff",
                        )
                    )

        # Рисуем стены
        for y in range(rows + 1):
            for x in range(cols):
                if maze["horizontal_walls"][y][x]:
                    canvas.controls.append(
                        ft.Container(
                            left=x * CELL_SIZE,
                            top=y * CELL_SIZE - 1,
                            width=CELL_SIZE,
                            height=2,
                            bgcolor="#ffffff"
                        )
                    )
        for y in range(rows):
            for x in range(cols + 1):
                if maze["vertical_walls"][y][x]:
                    canvas.controls.append(
                        ft.Container(
                            left=x * CELL_SIZE - 1,
                            top=y * CELL_SIZE,
                            width=2,
                            height=CELL_SIZE,
                            bgcolor="#ffffff"
                        )
                    )

        # Игрок
        player_x, player_y = 0, 0
        exit_x, exit_y = cols - 1, rows - 1

        player = ft.Container(
            left=0,
            top=0,
            width=CELL_SIZE,
            height=CELL_SIZE,
            bgcolor="#ff0000",
        )
        canvas.controls.append(player)
        page.add(canvas)

        # Состояние удержания клавиши
        held_key = None
        is_moving = False

        # Проверка и выполнение перемещения
        def try_move(dx, dy):
            nonlocal player_x, player_y
            new_x = player_x + dx
            new_y = player_y + dy

            if not (0 <= new_x < cols and 0 <= new_y < rows):
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
            player.left = player_x * CELL_SIZE
            player.top = player_y * CELL_SIZE
            player.update()

            if (player_x, player_y) == (exit_x, exit_y):
                page.window_destroy()

        # Асинхронное удержание клавиши
        async def continuous_move():
            nonlocal is_moving
            is_moving = True
            while held_key:
                if held_key == "w":
                    try_move(0, -1)
                elif held_key == "s":
                    try_move(0, 1)
                elif held_key == "a":
                    try_move(-1, 0)
                elif held_key == "d":
                    try_move(1, 0)
                await asyncio.sleep(MOVE_INTERVAL)
            is_moving = False

        def on_key_down(e: ft.KeyboardEvent):
            nonlocal held_key
            if held_key is None:
                held_key = e.key.lower()
                if not is_moving:
                    page.run_task(continuous_move())

        def on_key_up(e: ft.KeyboardEvent):
            nonlocal held_key
            if held_key == e.key.lower():
                held_key = None

        page.on_keyboard_event = lambda e: (
            on_key_down(e) if e.event_type == "keydown" else on_key_up(e)
        )


ft.app(target=main)

