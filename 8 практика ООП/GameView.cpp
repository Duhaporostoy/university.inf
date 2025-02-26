#include "GameView.h"

GameView* NewGameView(const sf::Vector2i& windowSize)
{
    GameView* view = new GameView();
    view->windowSize = windowSize;
    view->window.create(sf::VideoMode(windowSize.x, windowSize.y), "Game Window");
    view->camera.setSize(static_cast<float>(windowSize.x), static_cast<float>(windowSize.y));
    view->camera.setCenter(static_cast<float>(windowSize.x) / 2.f, static_cast<float>(windowSize.y) / 2.f);
    view->window.setView(view->camera);
    return view;
}

void EnterGameLoop(GameView& view, OnUpdate onUpdate, OnDraw onDraw, void* pData)
{
    while (view.window.isOpen())
    {
        sf::Event event;
        while (view.window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
            {
                view.window.close();
            }
        }

        float deltaSec = view.clock.restart().asSeconds();
        onUpdate(pData, view, deltaSec);
        onDraw(pData, view);
        view.window.display();
    }
}

void SetCameraCenter(GameView& view, const sf::Vector2f& center)
{
    view.camera.setCenter(center);
    view.window.setView(view.camera);
}

void DestroyGameView(GameView*& pView)
{
    delete pView;
    pView = nullptr;
}
