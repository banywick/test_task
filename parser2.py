from selenium import webdriver
from bs4 import BeautifulSoup

article = "264347015"

def fetch_product_info(article):
    url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
    # Настройка веб-драйвера
    driver = webdriver.Chrome()  # или webdriver.Firefox() для Firefox
    driver.get(url)

    # Получение HTML страницы
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Поиск элементов с помощью BeautifulSoup
    final_price_element = soup.find('ins', class_='price-block__final-price')
    old_price_element = soup.find('del', class_='price-block__old-price')

    if final_price_element:
        final_price = final_price_element.text.strip()
    else:
        final_price = "Не найдено"

    if old_price_element:
        old_price = old_price_element.text.strip()
    else:
        old_price = "Не найдено"

    print(f"Final Price: {final_price}")
    print(f"Old Price: {old_price}")

    driver.quit()

fetch_product_info(article)
