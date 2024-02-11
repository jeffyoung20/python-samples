from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

#********************************************************************
# Get Finacial Data from CNBC website using Menu Bar to navigate
# Data Returned
#   1. Gold Price
#   2. Oil Price
#   3. Bitcoin Price

# keeps chrome open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

stats = {}

# ***** CNBC *****
url = "https://cnbc.com"
driver.get(url)
driver.implicitly_wait(0.5)
menuButtons = driver.find_elements(by=By.CSS_SELECTOR, value="button.MarketsBannerMenu-marketOption")

# GOLD
gold_button = [btn for btn in menuButtons if btn.text == 'GOLD'][0]
gold_button.click()
driver.implicitly_wait(0.5)
goldSelector = "#market-data-scroll-container > a:nth-child(1) > div:nth-child(1) > span.MarketCard-stockPosition"
goldPrice = driver.find_element(by=By.CSS_SELECTOR, value=goldSelector).text
print(goldPrice)
stats['gold']= goldPrice

# OIL
oil_button = [btn for btn in menuButtons if btn.text == 'OIL'][0]
oil_button.click()
driver.implicitly_wait(0.5)
oilSelector = "#market-data-scroll-container > a:nth-child(1) > div:nth-child(1) > span.MarketCard-stockPosition"
oilPrice = driver.find_element(by=By.CSS_SELECTOR, value=oilSelector).text
print(oilPrice)
stats['oil_wti']= oilPrice

# BITCOIN
crypto_button = [btn for btn in menuButtons if btn.text == 'CRYPTO'][0]
crypto_button.click()
driver.implicitly_wait(0.5)
bitcoinSelector = "#market-data-scroll-container > a:nth-child(1) > div:nth-child(1) > span.MarketCard-stockPosition"
bitcoinPrice = driver.find_element(by=By.CSS_SELECTOR, value=bitcoinSelector).text
print(bitcoinPrice)
stats['bitcoin']= bitcoinPrice


#Results
print("\n ***** Results *****")
print(json.dumps(stats,indent=2))

# Closes Chrome
# driver.quit()
driver.close()



