import requests
from bs4 import BeautifulSoup

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


if __name__ == "__main__":
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    URL = "https://www.bloomberg.com/markets/rates-bonds/government-bonds/us"
    page = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    ratesTbonds = getData(soup, 'Treasury Yields')
    print(ratesTbonds)
    ratesTips = getData(soup, 'Treasury Inflation Protected Securities (TIPS)')
    print(ratesTips)





# print(results)