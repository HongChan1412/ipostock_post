import requests
from bs4 import BeautifulSoup

class calendar():
  def get_calendar():
    response = requests.get("http://www.38.co.kr/html/fund/index.htm?o=k")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find_all('font',{'color':'#0066CC'})
    stocks = []
    not_stocks = ['스팩','리츠']
    for i in reversed(text):
      for j in not_stocks:
        if j in i.text:
          break
        stocks.append(i.text)
        break
    return stocks
