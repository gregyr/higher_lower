from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json

import high_quality_img as hqi

#---Helpers---#
def clean_price(pricetag:str):
    """
    Säubert den Preis zu einem Floatformat
    """
    remove_letters = "ab€"
    new_string = ""
    for i in pricetag:
        if i not in remove_letters:
            if i == ",":
                new_string += "."
            else:
                new_string += i
    
    return new_string
            
def remove_duplicates(list):
    """
    Entfernt doppelte Produkte
    """
    new_list = []

    for item in list:
        if item not in new_list:
            new_list.append(item)
    return new_list

def export_to_json(data, filename="data.json"):
    """
    Exportiert das dictionary an Artikeln in eine JSON
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully exported data to {filename}")

    except Exception as e:
        print(f"Error exporting to JSON: {e}")

#---Scraping funktionen---#

def scraper(driver) :
    """
    Scraped die gerade geladene Seite <br>
    Kann nicht eine komplette Seite scannen, da diese automatisch generiert wird und nicht preloaded ist. <br>
    Preis sollte vielleicht als Float gespeichert werden statt eines Strings
    """
    scraped_data = []
    try:
        articles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
        )

        for article in articles:
            try:
                list_item = article.find_element(By.CSS_SELECTOR, "li.find_tile")

                #Preis den nochmal spezifizieren um den wirklichen UVP zu scrapen statt Rabatt
                #Möglicher weise Produkt namen vereinfachen
                product_name = list_item.find_element(By.CLASS_NAME, "find_tile__name")
                product_price = list_item.find_element(By.CSS_SELECTOR, ".find_tile__priceValue.find_tile__priceValue--red")

                product_image = list_item.find_element(By.CSS_SELECTOR, "div.find_tile__productImageContainer picture img.find_tile__productImage")

                
                image_url = product_image.get_attribute("src")
                if not image_url:
                    image_url = product_image.get_attribute("data-src")
                alt_image = product_image.get_attribute("alt")
                
                high_quality_img_url = hqi.get_high_quality_link(image_url, alt_image)

                data = {
                    "name": product_name.text.strip(),
                    "price": clean_price(product_price.text).strip(),
                    "img": image_url,
                    "high_q_img": high_quality_img_url
                }
                scraped_data.append(data)
                print(f"Name: {product_name.text.strip()}")

            except NoSuchElementException:
                print("Could not find name, price, or image for a product. Skipping.")

    except TimeoutException:
        print("Timed out waiting for products to load.")

    return scraped_data


def scrape_full_page(url, driver):
    """
    Scraped eine komplette Seite indem sie sie durchscrollt
    """
    driver.get(url)

    max_height = driver.execute_script("return document.body.scrollHeight")

    product_data = []

    current_height = 0

    #scrolls to end
    while current_height < max_height:  
        current_height += 4500
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        print(f"Scrolled to {current_height}")

        product_data.extend(scraper(driver))


    product_data = remove_duplicates(product_data)

    #Debugging    
    for item in product_data:
        print(item)
    print(len(product_data))

    return product_data


#---Main execute---#

def main(search_terms:list):
    """
    Scraped die gegebenen Suchterme <br>
    gibt eine JSON mit folgenden Produktdaten aus:
    - Name ("name")
    - Preis ("price")
    - original Bild ("img")
    - high-res Bild ("high_q_img")

    Das high-res Bild ist möglicherweise eine falsche URL, da sie generiert ist um traffic zu reduzieren. <br>
    
    """
    total_data = []

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    for search_term in search_terms:
        total_data.extend(scrape_full_page(f"https://www.otto.de/suche/{search_term}/", driver))

    export_to_json(total_data, 'articles.json')

    print(f"Articles scraped: {len(total_data)}")
    driver.quit()
    


if __name__ == "__main__":
    #läuft über suche also Kategorienamen anpassen
    #["multimedia", "bekleidung", "haushalt", "möbel", "küche"]
    categories = ["multimedia"]
    main(search_terms = categories)