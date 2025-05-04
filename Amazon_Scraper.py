import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time






import re

def replace_substr_in_url(url):
    # Define the pattern to match the substring to be replaced
    pattern = r'_SX\d+_SY\d+_CR,\d+,\d+,\d+,\d+_'

    # Use re.sub to replace the matched pattern with "_SX689_"
    modified_url = re.sub(pattern, '_SX689_', url)

    return modified_url






chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')


# Replace 'your_url_here' with the actual URL you want to scrape

#list=["B00J5BHOWM","B00INVR056","B00J5BHQT8","B00J58ODLU","B00JVLX7YA","B00IHZIAMK","B00IHZIBME","B00J5BHT8G","B00J5BHVCU"]

with open('asin.txt', 'r') as urls_file:
    list = urls_file.read().splitlines()



driver = webdriver.Chrome(options=chrome_options)
csv_filename = 'product_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title','Product_price', 'Info', 'Additional Details', 'Product Details','Product_link', 'Asin', 'Image Link','Seller Name','Seller link'])
    for i in list:
        url = f'https://www.amazon.in/dp/{i}'
        # Set up the Chrome browser with webdriver_manager

        try:
            # Navigate to the URL
            driver.get(url)
            time.sleep(2)

            # Find the element with id="title"
            title_element = driver.find_element(By.ID, 'title')
            title = title_element.text

            # Find the div with id="productFactsDesktopExpander"
            info_element = driver.find_element(By.ID, 'featurebullets_feature_div')
            info = info_element.text

            # Find all div elements with class="a-fixed-left-grid product-facts-detail"
            additional_details_elements = driver.find_elements(By.CLASS_NAME, 'a-fixed-left-grid.product-facts-detail')
            additional_details = [detail.text for detail in additional_details_elements]

            # Find the div with id="detailBullets_feature_div"
            try:
                product_details_element = driver.find_element(By.ID, 'detailBullets_feature_div')
                product_details = product_details_element.text
            except:
                product_details=""
            # Find the img with id="landingImage" and get the src \
            elements_xpath = '//*[@class="a-button-text"]//img'
            image_src = []
            try:
                # Wait for a maximum of 10 seconds for at least one element to be present
                elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, elements_xpath))
                )

                # Now you can interact with the list of elements
                # For example, you can loop through the elements and get their attributes
                for index, element in enumerate(elements, start=1):
                    element_src = element.get_attribute("src")
                    
                    image_src.append(replace_substr_in_url(element_src))
                    #print(f"Element {index} source:", element_src)

            except Exception as e:
                print("An error occurred while waiting for the elements:", str(e))
            
            

            # Save the data to a CSV file
            try:
                product_price = driver.find_element(By.ID,'corePrice_feature_div')
                product_price = product_price.text
            except: 
                product_price = ""
            time.sleep(20)
            try:
                Seller = driver.find_element(By.XPATH,'//div[@id="merchant-info"]')
                #print(Seller.text)
                seller = (str(Seller.text)).split("and")[0]
                print(seller)
            except:
                seller = ""
                
            try:
                seller_link = Seller.find_element(By.XPATH,'.//a[@class="a-link-normal"]')['href']
                print(seller_link)
            except:
                seller_link = ""
            
            csv_writer.writerow([title,product_price, info, '\n'.join(additional_details), product_details,url,i, image_src,seller,seller_link])

        except Exception as e:
            print(f"An error occurred: {e}")
            # Save the link in a text file if extraction fails
            with open('failed_links.txt', 'a') as failed_links_file:
                failed_links_file.write(f"{url}\n")


