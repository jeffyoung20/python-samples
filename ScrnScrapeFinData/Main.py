from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

from BondData import getBondData
from StockData import getStockData


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
    driver.implicitly_wait(0.5)
    goldSelector = "#market-data-scroll-container > a:nth-child(1) > div:nth-child(1) > span.MarketCard-stockPosition"
    goldPrice = driver.find_element(by=By.CSS_SELECTOR, value=goldSelector).text
    # print(goldPrice)
    dataCnbc['gold']= goldPrice

    # OIL
    oil_button = [btn for btn in menuButtons if btn.text == 'OIL'][0]
    oil_button.click()
    driver.implicitly_wait(0.5)
    oilSelector = "#market-data-scroll-container > a:nth-child(1) > div:nth-child(1) > span.MarketCard-stockPosition"
    oilPrice = driver.find_element(by=By.CSS_SELECTOR, value=oilSelector).text
    # print(oilPrice)
    dataCnbc['oil_wti']= oilPrice

    # BITCOIN
    crypto_button = [btn for btn in menuButtons if btn.text == 'CRYPTO'][0]
    crypto_button.click()
    driver.implicitly_wait(0.5)
    bitcoinSelector = "#market-data-scroll-container > a:nth-child(1) > div:nth-child(1) > span.MarketCard-stockPosition"
    bitcoinPrice = driver.find_element(by=By.CSS_SELECTOR, value=bitcoinSelector).text
    # print(bitcoinPrice)
    dataCnbc['bitcoin']= bitcoinPrice

    return dataCnbc


# ***** Vanguard MMF *****
def getVanguardData(driver):
    data = {}
    url = "https://investor.vanguard.com/investment-products/mutual-funds/profile/vmrxx"
    driver.get(url)
    driver.implicitly_wait(0.5)
    yieldPctVanguard = driver.find_element(by=By.CSS_SELECTOR, value="#Dashboard > div.container > div > div.col-md-6.col-lg-4.ml-xs-4 > dashboard-stats > div > div:nth-child(3) > div:nth-child(2) > div > h4 > div > h4:nth-child(1)")
    # print(yieldPctVanguard.text)
    data['Vanguard_VMRXX']= yieldPctVanguard.text
    return data


# ***** GET ALL Financial Data ***** 
def getFinancialData(driver):
    stats = {}

    # ***** Bond Data (Bloomburg)*****
    dataBonds = getBondData()
    # tipsData = { "tipsData": dataBonds[0] }
    # trsyData = { "treasuryData": dataBonds[1] }
    bondData = {
        "BondData": {
            "tipsData": dataBonds[1],
            "treasuryData": dataBonds[0]
        }
    }
    stats.update(bondData)

    # ***** Stock Data (WSJ)*****
    dataStocks = getStockData()
    stats.update({"stockData": dataStocks})

    # ***** CNBC *****
    dataCnbc = getCnbcData(driver)
    stats.update(dataCnbc)

    # ***** Vanguard Money Market Rate (VMRXX) *****
    statsVanguard = getVanguardData(driver)
    stats.update(statsVanguard)

    return stats

def printCsvLine(stats):
    print(f"{stats['Vanguard_VMRXX']}|",
            "TBD-Ally|",
            "TBD-Marcus|",
            f"{stats['BondData']['tipsData']['5 Year']}|",
            f"{stats['BondData']['treasuryData']['12 Month']}|",
            f"{stats['BondData']['treasuryData']['2 Year']}|",
            f"{stats['BondData']['treasuryData']['5 Year']}|",
            f"{stats['BondData']['treasuryData']['10 Year']}|",
            f"{stats['gold']}|",
            f"{stats['bitcoin']}|",
            f"{stats['oil_wti']}|",
            f"{stats['stockData']['sp500-yield']}|",
            f"{stats['stockData']['sp500-forward-pe']}")



# ********** MAIN **********
if __name__ == "__main__":
    print("\n ***** Start Extract *****")

    # keeps chrome open
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    stats = getFinancialData(driver)

    #Results
    print("\n ***** Results *****")
    print(json.dumps(stats,indent=2))

    #Data (csv)  for excel
    printCsvLine(stats)

    # Closes Chrome
    # driver.quit()
    driver.close()

    print("\n\n ***** The end *****")


