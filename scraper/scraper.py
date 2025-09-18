from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import time

import high_quality_img as hqi
import helper_functions as helper

LOGGER.setLevel(logging.WARNING)

def scraper(driver:webdriver.Chrome):
    """
    Scraped die gerade geladene Seite <br>
    Kann nicht eine komplette Seite scannen, da diese automatisch generiert wird und nicht preloaded ist. <br>
    --> Preis sollte vielleicht als Float gespeichert werden statt eines Strings
    """
    scraped_data = []
    product_count = 0

    try:
        articles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
        )

        for article in articles:
            try:
                list_item = article.find_element(By.CSS_SELECTOR, "li.find_tile")

                product_name = list_item.find_element(By.CLASS_NAME, "find_tile__name")

                try:
                    product_price = list_item.find_element(By.CSS_SELECTOR, ".find_tile__priceValue--strikethrough")
                except NoSuchElementException:
                    product_price = list_item.find_element(By.CSS_SELECTOR, ".find_tile__priceValue")

                product_image = list_item.find_element(By.CSS_SELECTOR, "div.find_tile__productImageContainer picture img.find_tile__productImage")

                
                image_url = product_image.get_attribute("src")
                if not image_url:
                    image_url = product_image.get_attribute("data-src")
                alt_image = product_image.get_attribute("alt")
                
                high_quality_img_url = hqi.get_high_quality_link(image_url, alt_image)

                data = {
                    "name": product_name.text.strip(),
                    "price": helper.clean_price(product_price.text),
                    "img": image_url,
                    "high_q_img": high_quality_img_url
                }
                scraped_data.append(data)

            except NoSuchElementException:
                #print("Some elements not found in this article, skipping...")
                pass

    except TimeoutException:
        print("Timed out waiting for products to load.")

    return scraped_data


def scrape_full_page(url:str, driver:webdriver.Chrome):
    """
    Scraped eine komplette Seite indem sie sie durchscrollt
    """
    print(f"Scraping {url}\n")
    driver.get(url)

    max_height = driver.execute_script("return document.body.scrollHeight")

    product_data = []

    current_height = 0

    #scrolls to end
    while current_height < max_height:  
        current_height += 4500
        percentage = min(100, int((current_height / max_height) * 100))
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        print(f"\033[FProgress: {percentage}% of category!" )

        product_data.extend(scraper(driver))


    product_data = helper.remove_duplicates(product_data)

    #Debugging    
    #for item in product_data:
    #    print(item)
    #print(len(product_data))

    return product_data


#---Main execute---#

def scrape_main(search_terms:list, export_path:str='articles.json', await_debug:bool=False):
    """
    Scraped die gegebenen Suchterme <br>
    gibt eine JSON mit folgenden Produktdaten aus:
    - Name ("name")
    - Preis ("price")
    - original Bild ("img")
    - high-res Bild ("high_q_img")

    Das high-res Bild ist möglicherweise eine falsche URL, da sie generiert ist um traffic zu reduzieren. <br>
    
    """
    category_dict = {}

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    print("Initializing WebDriver...")
    if await_debug:
        time.sleep(13) # Await all debug prints from selenium to finish

    for search_term in search_terms:
        products = scrape_full_page(f"https://www.otto.de/suche/{search_term}/", driver)
        category_dict[search_term] = products

    helper.export_to_json(category_dict, export_path)

    for product in category_dict:
        print(f"Category: {product}, Articles: {len(category_dict[product])}")

    total_count = sum(len(products) for products in category_dict.values())
    print(f"Total articles scraped: {total_count}")
    driver.quit()
    


if __name__ == "__main__":
    #läuft über suche also Kategorienamen anpassen
    #["multimedia", "bekleidung", "haushalt", "möbel", "küche"]
    categories = ["kostueme", "utensilien"]
    scrape_main(search_terms = categories, export_path='articles.json', await_debug=False)