import aiohttp
from bs4 import BeautifulSoup

from models import HTML, FoodMenuItem

__all__ = ('parse_food_menu_html', 'get_food_menu_html')


def parse_food_menu_html(html: HTML) -> list[FoodMenuItem]:
    soup = BeautifulSoup(html, 'lxml')

    food_item_tags = soup.find_all('div', attrs={'class': 'features-image'})

    food_items: list[FoodMenuItem] = []
    for food_item in food_item_tags:
        image_url = food_item.find('img')['src']
        name = food_item.find('h5', attrs={'class': 'item-title'}).text.strip()
        calories = (
            food_item.find('h6', attrs={'class': 'item-subtitle'})
            .text
            .strip()
            .split()[-1]
        )
        food_items.append(
            FoodMenuItem(
                image_url=image_url,
                name=name,
                calories=calories,
            )
        )

    return food_items


async def get_food_menu_html() -> HTML:
    url = 'https://beslenme.manas.edu.kg'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            html = await response.text()
    return HTML(html)
