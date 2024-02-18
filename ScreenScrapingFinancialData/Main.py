from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

from DataScripts.DataBonds import getBondData
from DataScripts.DataStocks import getStockData
from DataScripts.DataCommodities import getCnbcData
from DataScripts.DataBanks import getNerdWalletBankSavings as getBankSavingsRates


# ***** Vanguard MMF *****
def getVanguardData(driver):
    data = {}
    url = "https://investor.vanguard.com/investment-products/mutual-funds/profile/vmrxx"
    driver.implicitly_wait(1.0)
    driver.get(url)
    yieldPctVanguard = driver.find_element(by=By.CSS_SELECTOR, value="#Dashboard > div.container > div > div.col-md-6.col-lg-4.ml-xs-4 > dashboard-stats > div > div:nth-child(3) > div:nth-child(2) > div > h4 > div > h4:nth-child(1)")
    # print(yieldPctVanguard.text)
    data['Vanguard_VMRXX']= yieldPctVanguard.text
    return data


# ***** GET ALL Financial Data ***** 
def getFinancialData(driver):
    stats = {}

    # ***** Bond Data (Bloomburg)*****
    try:
        print("Getting Bond Data....")
        dataBonds = getBondData()
        # tipsData = { "tipsData": dataBonds[0] }
        # trsyData = { "treasuryData": dataBonds[1] }
        bondData = {
            "BondData": {
                "tipsData": dataBonds[1],
                "treasuryData": dataBonds[0]
            }
        }
    except Exception as e:
        bondData = {
            "BondData": "error"
        }
    stats.update(bondData)


    # ***** Stock Data (WSJ)*****
    try:
        print("Getting Stock Data....")
        dataStocks = getStockData()
        stats.update({"stockData": dataStocks})
    except Exception as e:
        stats.update({"stockData": "Error"})

    # ***** Get Bank Savings Rates *****
    try:
        print("Getting Banks Data....")
        statsBanks = getBankSavingsRates(driver)
        stats.update(statsBanks)
    except:
        stats.update({"bankSavingsRates": "error"} )


    # ***** Commondity (CNBC) *****
    try:
        print("Getting Commodity Data....")
        dataCnbc = getCnbcData(driver)
        stats.update({"commodities": dataCnbc})
    except Exception as e:
        stats.update({"commodities": "error"})


    # ***** Vanguard Money Market Rate (VMRXX) *****
    try:
        print("Getting Mutual Fund Sweep Rates....")
        statsVanguard = getVanguardData(driver)
        stats.update(statsVanguard)
    except:
        stats.update({'Vanguard_VMRXX': "error"})


    return stats



# ********** MAIN **********
if __name__ == "__main__":
    print("\n ***** Start Extract *****")

    # keeps chrome open
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(1.0)


    stats = getFinancialData(driver)

    #Results
    print("\n ***** Results *****")
    print(json.dumps(stats,indent=2))

    # Closes Chrome
    # driver.quit()
    driver.close()

    print("\n\n ***** The end *****")


