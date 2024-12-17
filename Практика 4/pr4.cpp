#include <iostream> 
#include <cmath>
#include <algorithm>

int main()
{
    float x, y;

    // Запрос ввода значений x и y
    std::cout << "Enter x and y values: ";
    std::cin >> x >> y;

    // Вычисление значения R
    double R = pow((x + y), (3 * sin(x)));

    // Вычисление значения S
    double S = sqrt(fabs(x)) / log(y);

    // Вычисление максимального значения между R и S
    double C = std::max(R, S);

    // Вывод результатов
    std::cout << "R = " << R << std::endl;
    std::cout << "S = " << S << std::endl;
    std::cout << "C = " << C << std::endl;

    // Ожидание нажатия любой клавиши перед завершением программы
    system("pause");

    return 0; // Завершение программы
}