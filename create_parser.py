from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

article = "170662179"

def fetch_product_info(article):
    url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
    # Настройка веб-драйвера
    driver = webdriver.Chrome()  # или webdriver.Firefox() для Firefox
    driver.get(url)

    try:
        # Ожидание загрузки названия товара
        try:
            product_title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'product-page__title')))
            product_title = product_title.text
        except:
            rating = "Название не найдено"

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
                EC.presence_of_element_located((By.XPATH, "//div[@class='product-page__common-info']//span" ))).get_attribute('innerText')
            rating = rating_element
        except:
            rating = "Рейтинг не найден"


        # Ожидание загрузки количества отзывов
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.product-review.j-wba-card-item')))
            feedback_count = element.get_attribute('data-feedbacks-count')
        except:
            feedback_count = "Количество отзывов не найдено"


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
            price = "Цена не найдена"

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
        except:
            price = "ошибка формирования опции"


        # print(f'Опции: {product_dict}')
        # print(f'Цена товара: {new_price}')
        # print(f'Название бренда: {brand_name}')
        # print(f'Цвет товара: {color}')
        # print(f'Название товара: {product_title}')
        # print(f'Рейтинг товара: {rating}')
        # print(f'Количество оценок: {feedback_count}')
    finally:
        driver.quit()

fetch_product_info(article)
