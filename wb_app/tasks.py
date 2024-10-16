from celery import shared_task
import requests
from .models import Product
import requests
from bs4 import BeautifulSoup

@shared_task
def fetch_product_info(article):
    url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
    response = requests.get(url)
    # Проверяем, что запрос был успешным
    if response.status_code == 200:
    # Парсим HTML-код страницы
        soup = BeautifulSoup(response.content, 'html.parser')

        # Извлекаем данные о товаре
        # Название товара
        product_name = soup.find('h1', {'class': 'same-part-kt__header'}).text.strip()

        # Цена товара
        product_price = soup.find('span', {'class': 'price-block__final-price'}).text.strip()

        # Описание товара
        product_description = soup.find('div', {'class': 'collapsable__content j-description'}).text.strip()

        # Выводим собранные данные
        print(f'Название товара: {product_name}')
        print(f'Цена товара: {product_price}')
        print(f'Описание товара: {product_description}')
    else:
        print(f'Ошибка при запросе: {response.status_code}')
        # Сохранение данных в базу данных
        # product = Product(article=article, name=data['name'], price=data['price'], stock=data['stock'], warehouses=data['warehouses'])
        # product.save()
