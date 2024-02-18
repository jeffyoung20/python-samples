from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

# ***** CNBC *****
def getCnbcData(driver):
    dataCnbc = {}
    url = "https://cnbc.com"
    driver.get(url)
    driver.implicitly_wait(0.5)
    menuButtons = driver.find_elements(by=By.CSS_SELECTOR, value="button.MarketsBannerMenu-marketOption")

    # GOLD
    gold_button = [btn for btn in menuButtons if btn.text == 'GOLD'][0]
    gold_button.click()
    goldSelector = "#market-data-scroll-container > a:nth-child(1) > div:nth-child(1) > span.MarketCard-stockPosition"
    goldPrice = driver.find_element(by=By.CSS_SELECTOR, value=goldSelector).text
    # print(goldPrice)
    dataCnbc['gold']= goldPrice

    # OIL
    oil_button = [btn for btn in menuButtons if btn.text == 'OIL'][0]
    oil_button.click()
    oilSelector = "#market-data-scroll-container > a:nth-child(1) > div:nth-child(1) > span.MarketCard-stockPosition"
    oilPrice = driver.find_element(by=By.CSS_SELECTOR, value=oilSelector).text
    # print(oilPrice)
    dataCnbc['oil_wti']= oilPrice

    # BITCOIN
    crypto_button = [btn for btn in menuButtons if btn.text == 'CRYPTO'][0]
    crypto_button.click()
    bitcoinSelector = "#market-data-scroll-container > a:nth-child(1) > div:nth-child(1) > span.MarketCard-stockPosition"
    bitcoinPrice = driver.find_element(by=By.CSS_SELECTOR, value=bitcoinSelector).text
    # print(bitcoinPrice)
    dataCnbc['bitcoin']= bitcoinPrice

    return dataCnbc


# ********** MAIN **********
if __name__ == "__main__":
    # keeps chrome open
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    data = getCnbcData(driver)
    print(json.dumps(data, indent=2))

    # Closes Chrome
    # driver.quit()
    driver.close()