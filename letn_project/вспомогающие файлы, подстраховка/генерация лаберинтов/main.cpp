#include <iostream>
#include <cstdlib>
#include <time.h>
#include <stack>
#include <vector>

using namespace std;

enum CellState { Close, Open };
class Cell
{
public:
    int x;
    int y;
    CellState Left;
    CellState Right;
    CellState Top;
    CellState Bottom;
    bool Visited;
};

int main(int argc, char** argv)
{
    const int width = 30,
        height = 30;

    Cell labyrinth[width][height];

    //заполняем начальные данные для ячеек
    for (int y = 0; y < height; y++)
        for (int x = 0; x < width; x++)
        {
            labyrinth[x][y].x = x;
            labyrinth[x][y].y = y;
            labyrinth[x][y].Visited = false;
        }

    //Выбираем первую ячейку откуда начнем движение
    srand(time(NULL));
    int startX = rand() % width;
    int startY = rand() % height;

    labyrinth[startX][startY].Visited = true;

    //Заносим нашу ячейке в path и начинаем строить путь
    stack<Cell> path;
    path.push(labyrinth[startX][startY]);

    while (!path.empty())
    {
        Cell _cell = path.top();

        //смотрим варианты, в какую сторону можно пойти
        vector<Cell> nextStep;
        if (_cell.x > 0 && (labyrinth[_cell.x - 1][_cell.y].Visited == false))
            nextStep.push_back(labyrinth[_cell.x - 1][_cell.y]);
        if (_cell.x < width - 1 && (labyrinth[_cell.x + 1][_cell.y].Visited == false))
            nextStep.push_back(labyrinth[_cell.x + 1][_cell.y]);
        if (_cell.y > 0 && (labyrinth[_cell.x][_cell.y - 1].Visited == false))
            nextStep.push_back(labyrinth[_cell.x][_cell.y - 1]);
        if (_cell.y < height - 1 && (labyrinth[_cell.x][_cell.y + 1].Visited == false))
            nextStep.push_back(labyrinth[_cell.x][_cell.y + 1]);

        if (!nextStep.empty())
        {
            //выбираем сторону из возможных вариантов
            Cell next = nextStep[rand() % nextStep.size()];

            //Открываем сторону, в которую пошли на ячейках
            if (next.x != _cell.x)
            {
                if (_cell.x - next.x > 0)
                {
                    labyrinth[_cell.x][_cell.y].Left = Open;
                    labyrinth[next.x][next.y].Right = Open;
                }
                else
                {
                    labyrinth[_cell.x][_cell.y].Right = Open;
                    labyrinth[next.x][next.y].Left = Open;
                }
            }
            if (next.y != _cell.y)
            {
                if (_cell.y - next.y > 0)
                {
                    labyrinth[_cell.x][_cell.y].Top = Open;
                    labyrinth[next.x][next.y].Bottom = Open;
                }
                else
                {
                    labyrinth[_cell.x][_cell.y].Bottom = Open;
                    labyrinth[next.x][next.y].Top = Open;
                }
            }

            labyrinth[next.x][next.y].Visited = true;
            path.push(next);

        }
        else
        {
            //если пойти никуда нельзя, возвращаемся к предыдущему узлу
            path.pop();
        }
    }
    // Визуализация лабиринта
    for (int y = 0; y < height; y++)
    {
        // Верхняя граница ячеек
        for (int x = 0; x < width; x++)
        {
            cout << "+";
            if (labyrinth[x][y].Top == Open)
                cout << " ";
            else
                cout << "-";
        }
        cout << "+" << endl;

        // Левая граница и внутренняя часть
        for (int x = 0; x < width; x++)
        {
            if (labyrinth[x][y].Left == Open)
                cout << " ";
            else
                cout << "|";

            cout << " ";
        }

        // Правая граница строки
        cout << "|" << endl;
    }

    // Нижняя граница последней строки
    for (int x = 0; x < width; x++)
    {
        cout << "+-";
    }
    cout << "+" << endl;

    return 0;
}