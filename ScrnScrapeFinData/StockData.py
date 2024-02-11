from time import sleep
import requests
from bs4 import BeautifulSoup
import json

def getStockData():
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    URL = "https://www.wsj.com/market-data/stocks/peyields"
    page = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    scripts = soup.find_all("script")
    jsCode = [text for script in scripts for text in script.contents]
    line = [code for code in jsCode if 'window.__STATE__ ' in code][0]
    pageDataStr = line[line.find("{"):line.rfind("}")+1]
    pageData = json.loads(pageDataStr)
    dataDow =pageData['data']['mdc_peAndYields_{"indexType":"DOW"}']['data']['data']['instruments']
    dataOthers = pageData['data']['mdc_peAndYields_{"indexType":"OTHERS"}']['data']['data']['instruments']
    # return {"dow": dataDow, "others":dataOthers}
    return {
        "sp500-forward-pe":  dataOthers[2]['formattedPriceEarningsRatioEstimate'],
        "sp500-yield": dataOthers[2]['yield']
    }

if __name__ == "__main__":
    print("\n\n***** Stock Market Data *****")
    data = getStockData()
    # for row in data:
    #     print(data[row]) 
    # futurePE = data['others'][2]['formattedPriceEarningsRatioEstimate']
    # yieldVal = data['others'][2]['yield']


    print("\n\n***** Values *****")
    print(data)
    # print(f"Future PE: {futurePE}")
    # print(f"yield: {yieldVal}")


    print("\n\n ***** The end *****")


