#include <SFML/Graphics.hpp>
#include <functional>
#include <string>
#include <cmath>

// Функция для отрисовки графика
void drawGraph(sf::RenderWindow& window, std::function<float(float)> func, float xMin, float xMax, float scaleX, float scaleY, sf::Color color) {
    sf::VertexArray graph(sf::LinesStrip);

    for (float x = xMin; x <= xMax; x += 0.1f) {
        float y = func(x); // Вычисление значения функции

        // Преобразование координат в экранные
        float screenX = 400 + x * scaleX;
        float screenY = 550 - y * scaleY;

        // Добавление точки в массив вершин
        graph.append(sf::Vertex(sf::Vector2f(screenX, screenY), color));
    }

    window.draw(graph);
}

// Определение зоны
int determineZone(float x, float y) {
    float y1 = abs(x); // График y = |x|
    float y2 = 3; // График y = 3

    if (y < y1 && y > y2 && x < -3) {
        return 3;
    }
    else if (y > y1 && y < y2) { //
        return 1;
    }
    else if (y < y1 && y < y2) { //
        return 5;
    }
    else if (y < y1 && y > y2 && x > 3) {
        return 4;
    }
    else if (y > y1 && y > y2) { //
        return 2;
    }

    return 0;
}

int main() {
    // Создание окна
    sf::RenderWindow window(sf::VideoMode(800, 600), "Graphing application");

    // Переменная для хранения пользовательской точки
    sf::CircleShape userPoint(5); // Радиус 5 пикселей
    userPoint.setFillColor(sf::Color::Yellow);
    bool userPointExists = false; // Переменная для проверки существования пользовательской точки

    // Загрузка шрифта
    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) return -1;

    // Текст для отображения координат точки
    sf::Text coordinatesText("", font, 20);
    coordinatesText.setFillColor(sf::Color::White);
    coordinatesText.setPosition(10, 10);

    // Оси X и Y
    sf::VertexArray xAxis(sf::Lines, 2);
    xAxis[0].position = sf::Vector2f(0, 550); // Начало оси X
    xAxis[0].color = sf::Color::White; // Цвет оси
    xAxis[1].position = sf::Vector2f(800, 550); // Конец оси X
    xAxis[1].color = sf::Color::White;

    sf::VertexArray yAxis(sf::Lines, 2);
    yAxis[0].position = sf::Vector2f(400, 0); // Начало оси Y
    yAxis[0].color = sf::Color::White; // Цвет оси
    yAxis[1].position = sf::Vector2f(400, 600); // Конец оси Y
    yAxis[1].color = sf::Color::White;

    // Масштабирование
    float scaleX = 40.0f;
    float scaleY = 50.0f;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();

            // Проверка клика мышью
            if (event.type == sf::Event::MouseButtonPressed) {
                if (event.mouseButton.button == sf::Mouse::Left) {
                    // Получение позиции клика
                    sf::Vector2i mousePos = sf::Mouse::getPosition(window);

                    // Преобразование экранных координат в "математические"
                    float mathX = (mousePos.x - 400) / scaleX;
                    float mathY = -(mousePos.y - 550) / scaleY;

                    // Установка новой пользовательской точки
                    userPoint.setPosition(mousePos.x - userPoint.getRadius(), mousePos.y - userPoint.getRadius());
                    userPointExists = true; // Помечаем, что точка существует

                    // Определение зоны
                    int zone = determineZone(mathX, mathY);

                    // Обновление текста с координатами точки
                    coordinatesText.setString("Coordinates: (" + std::to_string(mathX) + ", " + std::to_string(mathY) +
                        ")\nZone: " + std::to_string(zone));
                }
            }
        }

        // Очистка экрана
        window.clear();

        // Отрисовка осей
        window.draw(xAxis);
        window.draw(yAxis);

        // Отрисовка графика y1 = |x|
        drawGraph(window, [](float x) { return abs(x); }, -10, 10, scaleX, scaleY, sf::Color::Red);

        // Отрисовка графика y2 = 3
        drawGraph(window, [](float x) { return 3; }, -10, 10, scaleX, scaleY, sf::Color::Blue);

        // Отрисовка пользовательской точки, если она существует
        if (userPointExists) {
            window.draw(userPoint);
            window.draw(coordinatesText);
        }

        // Отображение нового кадра
        window.display();
    }

    return 0;
}