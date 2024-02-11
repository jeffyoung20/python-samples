from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json


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


# ***** Vanguard Money Market Rate (VMRXX) *****
url = "https://investor.vanguard.com/investment-products/mutual-funds/profile/vmrxx"
driver.get(url)
driver.implicitly_wait(0.5)
yieldPctVanguard = driver.find_element(by=By.CSS_SELECTOR, value="#Dashboard > div.container > div > div.col-md-6.col-lg-4.ml-xs-4 > dashboard-stats > div > div:nth-child(3) > div:nth-child(2) > div > h4 > div > h4:nth-child(1)")
print(yieldPctVanguard.text)
stats['Vanguard_VMRXX']= yieldPctVanguard.text


#Results
print("\n ***** Results *****")
print(json.dumps(stats,indent=2))

# Closes Chrome
# driver.quit()
driver.close()

print("\n\n ***** The end *****")


