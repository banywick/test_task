from celery import shared_task
import requests
from .models import Product

@shared_task
def fetch_product_info(article):
    url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
    response = requests.get(url)
    # Парсинг данных с сайта (здесь нужно использовать библиотеку для парсинга, например BeautifulSoup)
    # Пример:
    # data = parse_data(response.content)
    # Сохранение данных в базу данных
    # product = Product(article=article, name=data['name'], price=data['price'], stock=data['stock'], warehouses=data['warehouses'])
    # product.save()
