#include <iostream>
#include "GameView.h"
#include "GameScene.h"

int main(int argc, char* argv[])
{
    (void)argc;
    (void)argv;

    try
    {
        std::unique_ptr<GameView> pGameView = std::make_unique<GameView>(NewGameView({ 800, 600 }));
        std::unique_ptr<GameScene> pGameScene = std::make_unique<GameScene>(NewGameScene());

        EnterGameLoop(*pGameView, UpdateGameScene, DrawGameScene, pGameScene.get());
    }
    catch (const std::exception& ex)
    {
        std::cerr << ex.what() << std::endl;
        return 1;
    }

    return 0;
}
