import random
import time

# Определяем константы для состояния ячеек
Close = False
Open = True

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Left = Close
        self.Right = Close
        self.Top = Close
        self.Bottom = Close
        self.Visited = False

def main():
    width = 30
    height = 30

    # Создаем лабиринт как двумерный список объектов Cell
    labyrinth = [[Cell(x, y) for y in range(height)] for x in range(width)]

    # Заполняем начальные данные для ячеек (в конструкторе уже установлены значения по умолчанию)
    # Но Visited нужно обнулить, так как в конструкторе оно False, что нам и нужно.
    # Этот шаг в Python не обязателен, но оставлен для соответствия логике C++ кода.
    for x in range(width):
        for y in range(height):
            labyrinth[x][y].Visited = False

    # Выбираем первую ячейку, откуда начнем движение
    random.seed(time.time()) # Инициализируем генератор случайных чисел
    startX = random.randint(0, width - 1)
    startY = random.randint(0, height - 1)

    labyrinth[startX][startY].Visited = True

    # Заносим нашу ячейку в path и начинаем строить путь
    path = []
    path.append(labyrinth[startX][startY])

    while path:
        _cell = path[-1] # Получаем верхний элемент стека (top)

        # Смотрим варианты, в какую сторону можно пойти
        nextStep = []
        if _cell.x > 0 and not labyrinth[_cell.x - 1][_cell.y].Visited:
            nextStep.append(labyrinth[_cell.x - 1][_cell.y])
        if _cell.x < width - 1 and not labyrinth[_cell.x + 1][_cell.y].Visited:
            nextStep.append(labyrinth[_cell.x + 1][_cell.y])
        if _cell.y > 0 and not labyrinth[_cell.x][_cell.y - 1].Visited:
            nextStep.append(labyrinth[_cell.x][_cell.y - 1])
        if _cell.y < height - 1 and not labyrinth[_cell.x][_cell.y + 1].Visited:
            nextStep.append(labyrinth[_cell.x][_cell.y + 1])

        if nextStep:
            # Выбираем сторону из возможных вариантов
            next_cell = random.choice(nextStep) # Более питонический способ выбрать случайный элемент

            # Открываем сторону, в которую пошли на ячейках
            if next_cell.x != _cell.x:
                if _cell.x - next_cell.x > 0:
                    labyrinth[_cell.x][_cell.y].Left = Open
                    labyrinth[next_cell.x][next_cell.y].Right = Open
                else:
                    labyrinth[_cell.x][_cell.y].Right = Open
                    labyrinth[next_cell.x][next_cell.y].Left = Open
            if next_cell.y != _cell.y:
                if _cell.y - next_cell.y > 0:
                    labyrinth[_cell.x][_cell.y].Top = Open
                    labyrinth[next_cell.x][next_cell.y].Bottom = Open
                else:
                    labyrinth[_cell.x][_cell.y].Bottom = Open
                    labyrinth[next_cell.x][next_cell.y].Top = Open

            next_cell.Visited = True
            path.append(next_cell)

        else:
            # Если пойти никуда нельзя, возвращаемся к предыдущему узлу
            path.pop()

    # Визуализация лабиринта
    for y in range(height):
        # Верхняя граница ячеек
        for x in range(width):
            print("+", end="")
            if labyrinth[x][y].Top == Open:
                print(" ", end="")
            else:
                print("-", end="")
        print("+")

        # Левая граница и внутренняя часть
        for x in range(width):
            if labyrinth[x][y].Left == Open:
                print(" ", end="")
            else:
                print("|", end="")

            print(" ", end="")

        # Правая граница строки
        print("|")

    # Нижняя граница последней строки
    for x in range(width):
        print("+-", end="")
    print("+")

if __name__ == "__main__":
    main()