import flet as ft
import random
import sys

# Параметры лабиринта
CELL_SIZE = 40
MAZE_ROWS = 10
MAZE_COLS = 10

# Инициализация сетки: все стены на месте
def init_maze(rows, cols):
    maze = {
        "cells": [[False] * cols for _ in range(rows)],
        "vertical_walls": [[True] * (cols + 1) for _ in range(rows)],
        "horizontal_walls": [[True] * cols for _ in range(rows + 1)]
    }
    return maze

# DFS генерация
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

def main(page: ft.Page):
    page.bgcolor = "#000000"
    page.window_always_on_top = True

    maze = init_maze(MAZE_ROWS, MAZE_COLS)
    generate_maze_dfs(maze, MAZE_ROWS, MAZE_COLS)

    canvas = ft.Stack(width=CELL_SIZE * MAZE_COLS, height=CELL_SIZE * MAZE_ROWS)

    # Отрисовка проходов (синие клетки)
    for y in range(MAZE_ROWS):
        for x in range(MAZE_COLS):
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

    # Отрисовка стен (белые линии)
    for y in range(MAZE_ROWS + 1):
        for x in range(MAZE_COLS):
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
    for y in range(MAZE_ROWS):
        for x in range(MAZE_COLS + 1):
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

    # Позиция игрока
    player_x = 0
    player_y = 0
    exit_x = MAZE_COLS - 1
    exit_y = MAZE_ROWS - 1

    player = ft.Container(
        left=player_x * CELL_SIZE,
        top=player_y * CELL_SIZE,
        width=CELL_SIZE,
        height=CELL_SIZE,
        bgcolor="#ff0000",  # красный
    )
    canvas.controls.append(player)

    def move(dx, dy):
        nonlocal player_x, player_y
        new_x = player_x + dx
        new_y = player_y + dy

        if not (0 <= new_x < MAZE_COLS and 0 <= new_y < MAZE_ROWS):
            return

        # Проверка на стены
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
            page.window_destroy()  # выход из программы

    def on_key(e: ft.KeyboardEvent):
        key = e.key.lower()
        if key == "w":
            move(0, -1)
        elif key == "s":
            move(0, 1)
        elif key == "a":
            move(-1, 0)
        elif key == "d":
            move(1, 0)

    page.on_keyboard_event = on_key
    page.add(canvas)

ft.app(target=main)
