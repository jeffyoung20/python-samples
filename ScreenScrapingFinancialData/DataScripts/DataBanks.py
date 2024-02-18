from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json



# ***** Nerd wallet *****
def getNerdWalletBankSavings(driver):
    dataCnbc = {}
    url = "https://www.nerdwallet.com/best/banking/high-yield-online-savings-accounts"
    driver.get(url)

    bankRatesSelector = "tr._2lPc6W "
    listBanks = driver.find_elements(by=By.CSS_SELECTOR, value=bankRatesSelector)
    bankInfo = []
    for bank in listBanks:
        try:
            bankName = bank.find_element(by=By.CSS_SELECTOR, value="a").text
            bankRate = bank.find_elements(by=By.CSS_SELECTOR, value="td")[2].text
            bankInfo.append ({
                "bank-name": bankName,
                "bank-rate": bankRate
            }) 
        except:
            pass
    response = {
        "bankSavingsRates": bankInfo
    }
    return response


# ********** MAIN **********
if __name__ == "__main__":
    print("\n ***** Start Extract *****")

    # keeps chrome open
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(1.0)

    data = getNerdWalletBankSavings(driver)
    print(json.dumps(data, indent=2))

    # Closes Chrome
    # driver.quit()
    driver.close()

