# from contextlib import nullcontext
from selenium import webdriver
# from selenium.webdriver.remote.command import Command
# import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys 
from urllib import request
from html_table_parser import parser_functions
import pandas as pd
import numpy as np
import requests
import json
import os
from webdriver_manager.chrome import ChromeDriverManager
import urllib
os.environ['WDM_LOG_LEVEL'] = '0'
options = webdriver.ChromeOptions()
options.add_argument('blink-settings=imagesEnabled=false') #이미지 로딩 X
options.add_argument('headless') #창 띄우지않음
options.add_argument("lang=ko_KR")
options.add_argument('--incognito')
options.add_argument('--no-sandbox')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-setuid-sandbodx")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")
options.add_argument("--disable-browser-side-navigation")
options.add_experimental_option("prefs", {
    'profile.default_content_setting_values.notifications': 1,
    'profile.default_content_setting_values.clipboard': 1
})
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
options.add_argument('--mute-audio') #브라우저에 음소거 옵션을 적용합니다.
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36')

class MyChrome(webdriver.Chrome):
  def quit(self):
    webdriver.Chrome.quit(self)
    self.session_id = None

class crawl:
  def __init__(self) -> None:
    self.driver = MyChrome(ChromeDriverManager().install(), options=options)
    self.driver.implicitly_wait(30)

  def click_elemen(self, element):
    try:
      element.click()
    except:
      self.driver.execute_script("arguments[0].click();", element)

  def get_request_parser(self, url):
    response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup 

  def get_stock(self, stock_name):
    try:
      stock_dict = {'stock_name': stock_name}
      
      url = f"http://www.ipostock.co.kr/sub03/ipo04.asp?str3=&str4={stock_name}&x=0&y=0"
      self.driver.get(url)
      time.sleep(1)
      i = 1

      while True:
        element = self.driver.find_elements(By.XPATH, f'//*[@id="print"]/table[1]/tbody/tr[4]/td/table/tbody/tr[4]/td/table/tbody/tr[{i}]/td[3]/a')
        if element:
          if element[0].text.replace(".","") in stock_name:
            self.click_elemen(element[0])
            break
        else:
          self.driver.quit()
          return False
        i += 2

      #print("공모주",stock_name)
      stock_dict['stock_code'] = self.driver.find_element(By.CLASS_NAME, 'view_txt01').text
      stock_dict['stock_categori'] = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td[2]').text.split('] ')[1] #분류
      #print("수요예측일",self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td[2]').get_attribute("innerHTML") #수요예측일
      stock_dict['stock_subscriptionDay'] = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[3]/td[2]').get_attribute("innerHTML") #공모청약일
      stock_dict['stock_refundDay'] = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[4]/td[2]').get_attribute("innerHTML") #환불일
      # print("납입일", self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[5]/td[2]').get_attribute("innerHTML")) #납일일
      stock_listingDay = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[6]/td[2]').get_attribute("innerHTML") #싱장일
      if not stock_listingDay:
        stock_listingDay = "미정"
      stock_dict['stock_listingDay'] = stock_listingDay
      # stock_dict['stock_listingDay'] = stock_listingDay
      # print("심사청구일",self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td[2]').get_attribute("innerHTML").replace("&nbsp;","")) #심사청구일
      # print("심사승인일",self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td[4]').get_attribute("innerHTML")) #심사승인일
      # print("액면가",self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td[2]').get_attribute("innerHTML").replace("&nbsp;",""))#액면가
      stock_dict['stock_numPublicOffer'] = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr[1]/td[2]/b').get_attribute("innerHTML").replace("&nbsp;","")#공모주식수
      # print("전문투자자",self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr[2]/td[3]').get_attribute("innerHTML"),self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr[2]/td[4]').get_attribute("innerHTML")) #전문투자자
      # print("우리사주조합",self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr[3]/td[2]').get_attribute("innerHTML"),self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr[3]/td[3]').get_attribute("innerHTML")) #우리사주조합
      stock_dict['stock_numNormalOffer'] = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr[4]/td[2]/b').get_attribute("innerHTML")+" "+self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr[4]/td[3]/b').get_attribute("innerHTML").split('<')[0] #일반청약자
      # print("해외투자자",self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr[5]/td[2]').get_attribute("innerHTML"),self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr[5]/td[3]').get_attribute("innerHTML")) #해외투자자
      stock_dict['stock_hopePrice'] = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[2]').get_attribute("innerHTML").replace("&nbsp;","")#희망공모가격
      stock_dict['stock_hopeMount'] = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]').get_attribute("innerHTML").replace("&nbsp;","")#희망공모금액
      # print("확정공모가격",self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]/font/strong').get_attribute("innerHTML"))#확정공모가격
      # print("확정공모금액",self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[2]/strong/font').get_attribute("innerHTML"))#확정공모금액
      # print("청약증거금율",self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[5]/td[2]').get_attribute("innerHTML").replace("&nbsp;",""))#청약증거금율
      stock_competition = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[6]/td[2]/strong/font').get_attribute("innerHTML")#청약경쟁률
      if not stock_competition:
        stock_competition = "정보없음"
      stock_dict['stock_competition'] = stock_competition
      stock_manager = "" #주간사
      stock_managerInfo = "" #주간사 별 주식수 및 일반 청약한도
      element = self.driver.find_elements(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]/table[2]/tbody/tr')
      for i in range(len(element)):
        if i == 0:
          continue
        if i+1 == len(element):
          stock_managerInfo += f"{element[i].text}"
          stock_manager += f"{element[i].text.split(' ')[0]}"
        else:
          stock_managerInfo += f"{element[i].text}\n"
          stock_manager += f"{element[i].text.split(' ')[0]}, "
          
      stock_dict['stock_manager'] = stock_manager
      stock_dict['stock_managerInfo'] = stock_managerInfo   
      stock_dict['stock_notes'] = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[6]/td/table/tbody/tr/td[2]').text.replace("&nbsp","")#참고사항

      try:
        element = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td/a/img')
      except:
        element = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td/img')
      
      if element.get_attribute('src') in ["http://www.ipostock.co.kr/img/no_img.gif","http://www.ipostock.co.kr/upload/img/corp/"]:
        stock_logo = False
        stock_dict['stock_logoAddress'] = ""
      else:
        stock_logo = True
        stock_dict['stock_logoAddress'] = os.getcwd()+f"\\{stock_dict['stock_name']}_logoImg.png"
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(element.get_attribute('src'), stock_dict['stock_logoAddress']) #기업 로고 이미지 다운로드
      stock_dict['stock_logo'] = stock_logo
      
      # stock_info = []
      # stock_info.append(self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[1]').screenshot_as_png)
      # stock_info.append(self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]').screenshot_as_png)
      # stock_info.append(self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]').screenshot_as_png)
      # stock_info.append(self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]').screenshot_as_png)
      # stock_info.append(self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[6]/td').screenshot_as_png)
      # for i in range(len(stock_info)):
      #   with open(f'stock_info{i+1}.jpg', 'wb') as file:
      #     file.write(stock_info[i])

      # url_opt = self.driver.current_url[self.driver.current_url.find('code=')+5:self.driver.current_url.rfind('&schk')]

      # self.driver.get(f"http://www.ipostock.co.kr/view_pg/view_05.asp?code={url_opt}&gmenu=") #모의수요예측
      # time.sleep(1)
      # stock_prediction = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[5]/td/table[2]/tbody/tr[2]/td[2]').screenshot_as_png
      # with open('stock_prediction.png', 'wb') as file:
      #   file.write(stock_prediction)

      # self.driver.get(f"http://www.ipostock.co.kr/view_pg/view_03.asp?code={url_opt}&gmenu=") #재무정보 스크린샷
      # time.sleep(1)  
      # stock_finance = self.driver.find_element(By.XPATH, '//*[@id="print"]/table/tbody/tr[6]').screenshot_as_png
      # with open('stock_finance.png', 'wb') as file:
      #   file.write(stock_finance)

      # stock_financeText = [] #재무정보 텍스트
      # self.driver.get(f"http://test.38.co.kr/forum2/dart.php?code={stock_dict['stock_code']}")
      # time.sleep(1)
      # stock_financeText.append(self.driver.find_element(By.XPATH, '//*[@id="report"]/table[2]/thead/tr/th[1]').text)
      # stock_financeText.append(self.driver.find_element(By.XPATH, '//*[@id="report"]/table[2]/thead/tr/th[2]').text)
      # stock_financeText.append(self.driver.find_element(By.XPATH, '//*[@id="report"]/table[2]/thead/tr/th[3]').text)
        
      # element_row = self.driver.find_elements(By.XPATH, '//*[@id="report"]/table[2]/tbody/tr')
      # element_column = self.driver.find_elements(By.XPATH, f'//*[@id="report"]/table[2]/tbody/tr[1]/td')

      # for i in range(len(element_row)):
      #   for j in range(len(element_column)):
      #     stock_financeText.append(self.driver.find_element(By.XPATH, f'//*[@id="report"]/table[2]/tbody/tr[{i+1}]/td[{j+1}]').text.strip(" "))

      # stock_dict['stock_finance'] = stock_financeText
      
      url = "http://www.38.co.kr/html/forum/com_list/"
      self.driver.get(url)
      time.sleep(1)
      self.driver.find_element(By.ID, "string").send_keys(stock_name+Keys.RETURN)
      time.sleep(1)
      stock_dict['stock_code'] = self.driver.find_element(By.XPATH, "/html/body/table[3]/tbody/tr/td/table[1]/tbody/tr/td[1]/table[3]/tbody/tr[1]/td[2]").text
      
      url = "http://www.38.co.kr/html/news/?m=gongsi"
      self.driver.get(url)
      time.sleep(1)

      self.driver.find_element(By.CLASS_NAME, 'binput').send_keys(stock_name+Keys.RETURN)
      pageString = self.driver.page_source  
      bsObj = BeautifulSoup(pageString, 'html.parser') 
      text = bsObj.find_all("a", {"class":"news"})

      stock_gongsi = [] #공시정보
      for i in text:
        num = i['href']
        res_num = (num[num.find("'")+1:num.rfind("'")])
        if int(res_num[:4]) < 2022:
          continue 
        res_link = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo="+res_num
        stock_gongsi.append(f"{i.text} {res_link}")

      stock_dict['stock_gongsi'] = stock_gongsi
      
      self.driver.get(f"http://forum.38.co.kr/html/forum/board/?code={stock_dict['stock_code']}")
      time.sleep(1)
        
      self.click_elemen(self.driver.find_element(By.XPATH, "//*[contains(text(), '공모기업분석 보기')]"))
      time.sleep(1)

      pageString = self.driver.page_source  
      bsObj = BeautifulSoup(pageString, 'html.parser')

      stock_index = []
      if "주 가 지 표" in bsObj.text:
        element_row = self.driver.find_elements(By.XPATH, '/html/body/table[3]/tbody/tr/td/table[1]/tbody/tr/td[1]/table[15]/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr')
        element_column = self.driver.find_elements(By.XPATH, '/html/body/table[3]/tbody/tr/td/table[1]/tbody/tr/td[1]/table[15]/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[1]/td')
        for i in range(len(element_row)):
          for j in range(len(element_column)):
            element = self.driver.find_element(By.XPATH, f'/html/body/table[3]/tbody/tr/td/table[1]/tbody/tr/td[1]/table[15]/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[{i+1}]/td[{j+1}]')
            stock_index.append(element.text.strip(" ").replace("\n",""))
      else:
        stock_index = False

      stock_dict['stock_index'] = stock_index

      stock_business = []
      if "사업현황" in bsObj.text:
        text = bsObj.find_all('p')
        for i in text:
          if "사업현황" in i.text:
            continue
          elif "매출현황" in i.text:
            break
          else:
            if i.text:
              stock_business.append(i.text.replace("\n",""))
      else:
        stock_business = False

      stock_dict['stock_business'] = stock_business

      # self.driver.get('http://www.38.co.kr/html/fund/?o=k')
      # time.sleep(1)

      # stock_schedule = [] #공모주일정
      # element = self.driver.find_element(By.XPATH, '/html/body/table[3]/tbody/tr/td/table[1]/tbody/tr/td[1]/table[4]/tbody/tr[2]/td/table/thead/tr[1]')
      # text = element.text.strip(" ").split(" ")
      # stock_schedule.append(text[0])
      # stock_schedule.append(text[1])
      # stock_schedule.append(text[3])
      # stock_schedule.append(text[5])

      # element = self.driver.find_elements(By.XPATH, '/html/body/table[3]/tbody/tr/td/table[1]/tbody/tr/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr')
      # for i in reversed(element):
      #   text = i.text.strip(" ").split(" ")
      #   if (datetime.now() - datetime.strptime(text[1].split("~")[0], "%Y.%m.%d")).days < 0:
      #     stock_schedule.append(text[0])
      #     stock_schedule.append(text[1])
      #     stock_schedule.append(text[3])
      #     stock_schedule.append(text[4])

      # stock_dict['stock_schedule'] = stock_schedule
      
      soup = self.get_request_parser(f"http://test.38.co.kr/forum2/dart.php?code={stock_dict['stock_code']}")
      data = soup.find_all("table")[1]
      table = parser_functions.make2d(data)
      df = pd.DataFrame(data=table[1:], columns=table[0])
      stock_dict['stock_finance'] = {'column_list' :df.columns.values.tolist(), 'var_list' : df.values.tolist()}
      
      soup = self.get_request_parser("http://www.38.co.kr/html/fund/?o=k")
      data = soup.find("table",{"summary":"공모주 청약일정"})
      table = parser_functions.make2d(data)
      df = pd.DataFrame(data=table[1:], columns=table[0]).drop(["확정공모가","청약경쟁률","분석"],axis='columns')
      df.replace("",np.nan, inplace=True)
      df = df.dropna().reset_index(drop=True)
      df['공모주일정']
      for i in range(len(df['공모주일정'])):
        if (datetime.now() - datetime.strptime(df['공모주일정'][i].split("~")[0], "%Y.%m.%d")).days >= 0:
          df['공모주일정'][i] = np.nan
          
      df = df.dropna().loc[::-1].reset_index(drop=True)
      stock_dict['stock_schedule'] = {'column_list':df.columns.values.tolist(), 'var_list':df.values.tolist()}

      with open(f"{stock_dict['stock_name']}.json", "w", encoding="utf-8") as make_file:
        json.dump(stock_dict, make_file, ensure_ascii=False, indent="\t")
      
      self.driver.quit()
      return True
    
    except Exception as e:
      print(e)
      self.driver.quit()
      return False
      
