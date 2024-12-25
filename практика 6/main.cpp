#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>

using namespace std;

int main() {
    int n = 10; // Размер матрицы
    const int cellSize = 50; // Размер клетки
    const int windowSize = n * cellSize; // Размер окна

    // Создание окна
    sf::RenderWindow window(sf::VideoMode(windowSize, windowSize), "Matrix");

    vector<sf::RectangleShape> cells(n * n); // Ячейки матрицы

    // Создание ячеек
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int index = i * n + j; // Индекс текущей ячейки
            cells[index].setSize(sf::Vector2f(cellSize - 2, cellSize - 2)); // Ободок ячеек
            cells[index].setPosition(j * cellSize + 1, i * cellSize + 1); // Смещение ячеек

            // Закрашивание в шахматном порядке
            if ((i + j) % 2 == 0) {
                cells[index].setFillColor(sf::Color::Green); // Зеленый цвет
            }
            else {
                cells[index].setFillColor(sf::Color::White); // Белый цвет
            }
        }
    }

    // Основной цикл
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) { // Закрытие окна
                window.close();
            }
        }

        window.clear(sf::Color::Black); // Очистка окна черным цветом

        // Отрисовка всех ячеек
        for (const auto& cell : cells) {
            window.draw(cell);
        }

        window.display(); // Отображение содержимого окна
    }

    return 0;
}