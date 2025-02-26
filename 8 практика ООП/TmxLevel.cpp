#include "TmxLevel.h"
#include "tinyxml2.h"
#include <sstream>
#include <string>
#include <SFML/Graphics.hpp>

bool TmxLevel::LoadFromFile(const std::string& filepath)
{
    tinyxml2::XMLDocument doc;
    if (doc.LoadFile(filepath.c_str()) != tinyxml2::XML_SUCCESS)
    {
        return false;
    }

    tinyxml2::XMLElement* mapElement = doc.FirstChildElement("map");
    if (!mapElement)
    {
        return false;
    }

    mapElement->QueryIntAttribute("width", &m_width);
    mapElement->QueryIntAttribute("height", &m_height);
    mapElement->QueryIntAttribute("tilewidth", &m_tileWidth);
    mapElement->QueryIntAttribute("tileheight", &m_tileHeight);

    tinyxml2::XMLElement* tilesetElement = mapElement->FirstChildElement("tileset");
    if (tilesetElement)
    {
        tinyxml2::XMLElement* imageElement = tilesetElement->FirstChildElement("image");
        if (imageElement)
        {
            const char* imagePath = imageElement->Attribute("source");
            if (imagePath && !m_tilesetImage.loadFromFile(imagePath))
            {
                return false;
            }
        }
    }

    tinyxml2::XMLElement* layerElement = mapElement->FirstChildElement("layer");
    while (layerElement)
    {
        TmxLayer layer;
        tinyxml2::XMLElement* dataElement = layerElement->FirstChildElement("data");
        if (dataElement)
        {
            const char* encoding = dataElement->Attribute("encoding");
            if (encoding && std::string(encoding) == "csv")
            {
                const char* tileData = dataElement->GetText();
                std::stringstream ss(tileData);
                std::string tile;
                int x = 0, y = 0;
                while (std::getline(ss, tile, ','))
                {
                    int tileID = std::stoi(tile) - m_firstTileID;
                    if (tileID >= 0)
                    {
                        sf::Sprite sprite;
                        sprite.setTexture(m_tilesetImage);
                        sprite.setTextureRect(sf::IntRect(
                            tileID % (m_tilesetImage.getSize().x / m_tileWidth) * m_tileWidth,
                            tileID / (m_tilesetImage.getSize().x / m_tileWidth) * m_tileHeight,
                            m_tileWidth, m_tileHeight));
                        sprite.setPosition(static_cast<float>(x * m_tileWidth), static_cast<float>(y * m_tileHeight));
                        layer.tiles.push_back(sprite);
                    }
                    x++;
                    if (x >= m_width)
                    {
                        x = 0;
                        y++;
                    }
                }
            }
        }
        m_layers.push_back(layer);
        layerElement = layerElement->NextSiblingElement("layer");
    }

    tinyxml2::XMLElement* objectGroupElement = mapElement->FirstChildElement("objectgroup");
    while (objectGroupElement)
    {
        tinyxml2::XMLElement* objectElement = objectGroupElement->FirstChildElement("object");
        while (objectElement)
        {
            TmxObject obj;
            obj.id = objectElement->IntAttribute("id");
            obj.name = objectElement->Attribute("name");
            obj.type = objectElement->Attribute("type");
            obj.rect.left = objectElement->FloatAttribute("x");
            obj.rect.top = objectElement->FloatAttribute("y");
            obj.rect.width = objectElement->FloatAttribute("width");
            obj.rect.height = objectElement->FloatAttribute("height");

            tinyxml2::XMLElement* propertiesElement = objectElement->FirstChildElement("properties");
            if (propertiesElement)
            {
                tinyxml2::XMLElement* propertyElement = propertiesElement->FirstChildElement("property");
                while (propertyElement)
                {
                    std::string key = propertyElement->Attribute("name");
                    std::string value = propertyElement->Attribute("value");
                    obj.properties[key] = value;
                    propertyElement = propertyElement->NextSiblingElement("property");
                }
            }

            obj.sprite.setTexture(m_tilesetImage);
            obj.sprite.setTextureRect(sf::IntRect(0, 0, m_tileWidth, m_tileHeight));
            obj.sprite.setPosition(obj.rect.left, obj.rect.top);

            m_objects.push_back(obj);
            objectElement = objectElement->NextSiblingElement("object");
        }
        objectGroupElement = objectGroupElement->NextSiblingElement("objectgroup");
    }

    return true;
}
