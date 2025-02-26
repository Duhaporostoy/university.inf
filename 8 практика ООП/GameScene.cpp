#include "GameScene.h"
#include "GameView.h"

GameScene* NewGameScene()
{
    GameScene* scene = new GameScene();
    scene->level.LoadFromFile("path/to/your/map.tmx");
    scene->player = scene->level.GetFirstObject("player");
    scene->enemies = scene->level.GetAllObjects("enemy");
    scene->coins = scene->level.GetAllObjects("coin");
    return scene;
}

void UpdateGameScene(void* pData, GameView& view, float deltaSec)
{
    GameScene* scene = static_cast<GameScene*>(pData);
    // Обновление логики игры
    // Пример: перемещение игрока
    sf::Vector2f movement = { 0.f, 0.f }; // Замените на реальное значение
    scene->player.MoveBy(movement);
}

void DrawGameScene(void* pData, GameView& view)
{
    GameScene* scene = static_cast<GameScene*>(pData);
    scene->level.Draw(view.window);
    view.window.draw(scene->player.sprite);
    for (const TmxObject& enemy : scene->enemies)
    {
        view.window.draw(enemy.sprite);
    }
    for (const TmxObject& coin : scene->coins)
    {
        view.window.draw(coin.sprite);
    }
}

void DestroyGameScene(GameScene*& pScene)
{
    delete pScene;
    pScene = nullptr;
}
