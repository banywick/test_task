from celery import shared_task
import requests
from .models import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def save_product_db(product_title, brand_name, new_price, color, rating, product_dict, feedback_count):
    
    product = Product(
        brand=brand_name,
        name=product_title,
        price=new_price,
        color=color,
        rating=rating,
        number_of_ratings=feedback_count,
        options=product_dict
    )
    product.save() 

@shared_task
def fetch_product_info(article):
    url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
    # Настройка опций для запуска Chrome в фоновом режиме
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Запуск в фоновом режиме
    chrome_options.add_argument("--disable-gpu")  # Отключение GPU для ускорения работы
    chrome_options.add_argument("--no-sandbox")  # Отключение песочницы для работы в контейнерах
    chrome_options.add_argument("--disable-dev-shm-usage")  # Отключение использования /dev/shm
    response = requests.get(url)
    # Проверяем, что запрос был успешным
    if response.status_code == 200:
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Chrome()
        driver.get(url)

        try:
            # Ожидание загрузки названия товара
            try:
                product_title = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'product-page__title')))
                product_title = product_title.text
            except:
                product_title = "Название не найдено"

            try:
                # Ожидание загрузки цвета товара
                color = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'color-name')))
                color = color.text
            except:
                color = "Цвет не найден"

            # Ожидание загрузки рейтинга товара
            try:
                rating_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='product-page__common-info']//span"))).get_attribute('innerText')
                rating = float(rating_element.replace(',', '.'))  # Преобразование строки в float
            except:
                rating = 0.0

            # Ожидание загрузки количества отзывов
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a.product-review.j-wba-card-item')))
                feedback_count = int(element.get_attribute('data-feedbacks-count'))  # Преобразование строки в int
            except:
                feedback_count = 0

            # Ожидание загрузки бренда товара
            try:
                brand_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a.product-page__header-brand.j-wba-card-item.j-wba-card-item-show.j-wba-card-item-observe')))
                brand_name = brand_element.text
            except:
                brand_name = "Бренд не найден"

            # Ожидание загрузки цены товара
            try:
                price = driver.find_element(By.XPATH, "//div[@class='price-block']//ins").get_attribute('innerText')
                new_price = ' '.join(price.split('\xa0')).strip()
            except:
                new_price = 0.0

            # Ожидание загрузки остатка
            try:
                remains_list = []
                values_list = []
                article_product = driver.find_element(By.XPATH, "//div[@class='product-page__options']//td[@class='product-params__cell product-params__cell--copy']").get_attribute('innerText')
                values_list.append(article_product)

                remains = driver.find_elements(By.XPATH, "//div[@class='product-page__options']//tr[@class='product-params__row']//span/span")
                for item in remains:
                    remains_list.append(item.get_attribute('innerText'))

                values = driver.find_elements(By.XPATH, "//div[@class='product-page__options']//td[@class='product-params__cell']/span")
                for item in values:
                    values_list.append(item.get_attribute('innerText'))

                product_dict = dict(zip(remains_list, values_list))
            except Exception as e:
                product_dict = {}
                print(f"Ошибка формирования опции: {e}")


            save_product_db(product_title, brand_name, new_price, color, rating, product_dict, feedback_count)
        finally:
            driver.quit()
    else:
        print(f'Ошибка при запросе: {response.status_code}')
