import sys
import csv
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import time

# default path to file to store data
path_to_file = "/Users/andychang/Documents/2020_Lectures/DCP3510 - AI/project/crawl/data/reviews.csv"

# default number of scraped pages
num_page = 1

# default tripadvisor website of restaurant
url = "https://www.tripadvisor.com.tw/Restaurant_Review-g13808853-d1633095-Reviews-Fuhang_Soy_Milk-Zhongzheng_District_Taipei.html"

# if you pass the inputs in the command line
if (len(sys.argv) == 4):
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# Import the webdriver
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get(url)

# Get restaurant name
breadcrumbs = driver.find_elements_by_xpath("//li[@class='breadcrumb']")
restaurant = breadcrumbs[-1].text
# Find the last page index of all reviews
try: 
    last_page_index = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[6]/div/div[1]/div[4]/div/div[5]/div/div[13]/div/div/div/a[8]").text
    num_page = int(last_page_index)
except selenium.common.exceptions.NoSuchElementException as e:
    print("already last page!")
    num_page = 1
print("pages:",num_page)

header = ['date','rating','restaurant','title','review']
# Open the file to save the review
csvFile = open(path_to_file, 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)
csvWriter.writerow(header)
# change the value inside the range to save more or less reviews
for i in range(0, num_page):
    
    # expand the review 
    time.sleep(2)
    try:
        driver.find_element_by_xpath("//span[@class='taLnk ulBlueLinks']").click()
        time.sleep(1)
    except selenium.common.exceptions.NoSuchElementException as e:
        # all reviews are not collapsed
        pass
    except StaleElementReferenceException as e:
        time.sleep(2)
        driver.find_element_by_xpath("//span[@class='taLnk ulBlueLinks']").click()

    
    
    container = driver.find_elements_by_xpath(".//div[@class='review-container']")
    print('page:', i, 'length:', len(container))
    for j in range(len(container)):
        # print(j)

        # Bypass translated reviews
        try:
            container[j].find_element_by_css_selector('div.translation.footer')
            # print("footer found, skip!")
            continue
        except selenium.common.exceptions.NoSuchElementException as e:
            # print("translation not found!")
            pass
            # not translated
        
        title = container[j].find_element_by_xpath(".//span[@class='noQuotes']").text
        date = container[j].find_element_by_xpath(".//span[contains(@class, 'ratingDate')]").get_attribute("title")
        rating = container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3][0]
        review = container[j].find_element_by_xpath(".//p[@class='partial_entry']").text.replace("\n", " ")

        csvWriter.writerow([date, rating, restaurant, title, review]) 

    # change the page
    driver.find_element_by_xpath('.//a[@class="nav next ui_button primary"]').click()

driver.close()
