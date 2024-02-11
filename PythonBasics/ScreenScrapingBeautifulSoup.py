from time import sleep
import requests
from bs4 import BeautifulSoup
import json

def getData(soup, hdrString):
    tblContainer = soup.find("h2", string=hdrString).parent.parent
    tblRows = tblContainer.find_all("tr", class_="data-table-row")
    rates = {}
    for row in tblRows:
        key = row.find_all('th')[0].text.split()
        key = f"{key[1]} {key[2]}"
        value = row.find_all('td')[2].text
        rates[key] = value
    return rates

def getBondData():
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    URL = "https://www.bloomberg.com/markets/rates-bonds/government-bonds/us"
    page = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    ratesTbonds = getData(soup, 'Treasury Yields')
    ratesTips = getData(soup, 'Treasury Inflation Protected Securities (TIPS)')
    return ratesTbonds, ratesTips

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
    return {"dow": dataDow, "others":dataOthers}

if __name__ == "__main__":
    print("\n\n***** Treasury Market Data *****")
    ratesTbonds, ratesTips = getBondData()
    print(ratesTbonds)
    print(ratesTips)

    print("\n\n***** Stock Market Data *****")
    data = getStockData()
    # for row in data:
    #     print(data[row]) 
    futurePE = data['others'][2]['formattedPriceEarningsRatioEstimate']
    yieldVal = data['others'][2]['yield']


    print("\n\n***** Values *****")
    print(f"Future PE: {futurePE}")
    print(f"yield: {yieldVal}")


    print("\n\n ***** The end *****")


