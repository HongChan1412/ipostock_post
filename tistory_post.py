# from contextlib import nullcontext
from selenium import webdriver
# from selenium.webdriver.remote.command import Command
# import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
import pyautogui
import pyperclip
import json
import pywinauto
import pygetwindow as gw
import os
os.environ['WDM_LOG_LEVEL'] = '0'

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    'profile.default_content_setting_values.notifications': 1,
    'profile.default_content_setting_values.clipboard': 1
})
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--start-maximized')  
options.add_argument("disable-gpu")
# options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
options.add_argument('--mute-audio') #브라우저에 음소거 옵션을 적용합니다.
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36')


class MyChrome(webdriver.Chrome):
  def quit(self):
    webdriver.Chrome.quit(self)
    self.session_id = None
    
class tistoryPost():
  def __init__(self, id, pw, url) -> None:
    self.driver = MyChrome(ChromeDriverManager().install(), options=options)
    self.driver.implicitly_wait(30)
    self.id = id
    self.pw = pw
    self.url = url
    
  def click_elemen(self, element):
    try:
      WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(element)).click()
    except:
      self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
      self.driver.execute_script("arguments[0].click();", element)
    
  def login(self):
    self.driver.get(f'https://{self.url}.tistory.com/manage')
    time.sleep(1)   
    self.click_elemen(self.driver.find_element(By.CLASS_NAME, "btn_login.link_kakao_id"))
    time.sleep(1)
    if self.driver.find_elements(By.ID, "rc-anchor-container"):
      return False
    self.driver.find_element(By.ID, "id_email_2").send_keys(self.id)
    time.sleep(1)
    self.driver.find_element(By.ID, "id_password_3").send_keys(self.pw)
    time.sleep(1)
    self.click_elemen(self.driver.find_element(By.CSS_SELECTOR, "button.btn_g.btn_confirm.submit"))
    time.sleep(1)
  
    if self.driver.current_url != f"https://www.tistory.com/auth/login/?redirectUrl=https%3A%2F%2F{self.url}.tistory.com%2Fmanage":

      print("로그인 성공")
      time.sleep(1)
      self.driver.get(f"https://{self.url}.tistory.com/manage/newpost/?type=post&returnURL=/manage/posts")
      time.sleep(1)
      
      try:
        popup = Alert(self.driver)
        popup.dismiss()
      except:
        print("Alert창이 존재하지 않음")
      
      return True
    else:
      return False
    
  def input_img(self, stock_logoAddress):
    self.click_elemen(self.driver.find_element(By.CLASS_NAME, "mce-ico.mce-i-image"))
    time.sleep(1)
    self.click_elemen(self.driver.find_element(By.ID, "attach-image"))
    while True:
      titles = gw.getAllTitles()
      if "열기" in titles:
        break
      time.sleep(1)
    time.sleep(5)
    pyperclip.copy(stock_logoAddress)
    time.sleep(5)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(5)
    pyautogui.hotkey("enter")

  def setquot(self, text):
    text = text.replace("\n", "<br>")
    quot = f'\
  <table style="BORDER-COLLAPSE: collapse" cellspacing="1" cellpadding="1" width="100%" bgcolor="#ffffff">\
    <tbody>\
        <tr>\
          <td style="BORDER-BOTTOM: #1874cd 1px solid; BORDER-LEFT: #1874cd 10px solid" width="100%"><font color="#1874cd"><strong><span style="FONT-SIZE: 14pt"><font>{text}</font></span></strong></font></td>\
        </tr>\
    </tbody>\
  </table><br>'
    return quot
  
  def setTable(self, tableValue, size ,**kwargs):
    cont = ""
    cont += '<table style="border-collapse: collapse; width: 100%;" border="1" data-ke-align="alignLeft" data-ke-style="style9">\
  <tbody>\
  <tr>'
    if 'column' in kwargs:
      for i in range(kwargs['column']):
        cont += f'<td style="text-align: center; background-color: #03c75a; color: white; font-weight: bold;">{tableValue[i]}</td>'
      cont += '</tr>'
      
      for i in range(len(tableValue)):
        if i > kwargs['column'] and (i+1)%kwargs['column'] == 0:
          cont += '<tr>'
          for j in reversed(range(kwargs['column'])):
            print(i-j)
            cont += f'<td style="font-size: {size}px; text-align: center;">{tableValue[i-j]}</td>'
          cont += '</tr>'
      cont += '</tbody></table>'
      
      return cont
          
    for i in range(len(tableValue['column_list'])):
      cont += f'<td style="text-align: center; background-color: #03c75a; color: white; font-weight: bold;">{tableValue["column_list"][i]}</td>'
    cont += '</tr>'
    
    for i in range(len(tableValue['var_list'])):
      cont += '<tr>'
      for j in tableValue['var_list'][i]:
        cont += f'<td style="font-size: {size}px; text-align: center;">{j}</td>'
      cont += '</tr>'
    cont += '</tbody></table>'
    
    return cont

  def input_hashtag(self, text):
    stock_hashtag = [text,text+"공모",text+"청약",text+"공모주",text+"상장",text+"주간사",text+"주관사",text+"공모가",text+"일정",text+"정보"]
    return stock_hashtag

  def htmlConvert(self, stock_dict):
    content = ""
    
    # content += '<br>' + '<p><a style="box-shadow: 5px 5px 15px 5px rgba(0,0,0,0.2)" href="https://url.kr/ay59du" target="_blank"><img src="https://moneyseo.cafe24.com/wp-content/uploads/2022/08/재테크카페에반다하-배너.png" alt=""></a></p>'

    content += '<br>' + '<p><a href="https://url.kr/ay59du" target="_blank"><img src="https://moneyseo.cafe24.com/wp-content/uploads/2022/08/재테크카페에반다하-배너.png" alt=""></a></p>'

    text = f"""
{stock_dict['stock_name']} 공모주 청약정보에 대해서 알려드리겠습니다
"""
    content += '<br>' + '<p>' + text.replace("\n", "<br>") + '</p><br>'
    
    content += '<br>' + self.setquot(f"{stock_dict['stock_name']} 청약정보")
    
    text = f"""
{stock_dict['stock_name']}
총 공모 주식수 : {stock_dict['stock_numPublicOffer']}
일반투자자 공모주식수 : {stock_dict['stock_numNormalOffer']}

청약일 : {stock_dict['stock_subscriptionDay']}
환불일 : {stock_dict['stock_refundDay']}
상장일 : {stock_dict['stock_listingDay']}
주간사 : {stock_dict['stock_manager']}
"""
    content += '<br>' + '<p>' + text.replace("\n", "<br>") + '</p><br>'
    
    content += '<br>' + self.setquot(f"{stock_dict['stock_name']} 공모정보")
    
    text = f"""
희망공모가격 : {stock_dict['stock_hopePrice']}
희망공모금액 : {stock_dict['stock_hopeMount']}
청약경쟁률 : {stock_dict['stock_competition']}
"""
    
    content += '<br>' + '<p>' + text.replace("\n", "<br>") + '</p><br>'
    
    content += '<br>' + self.setquot(stock_dict['stock_managerInfo'])

    content += '<br>' + self.setquot(f"{stock_dict['stock_name']} 기업정보")
    
    text = f"""
종목코드 : {stock_dict['stock_code']}
분류 : {stock_dict['stock_categori']}
"""

    content += '<br>' + '<p>' + text.replace("\n", "<br>") + '</p><br>'
    if stock_dict['stock_business']:
      content += '<br>' + self.setquot(f"{stock_dict['stock_name']}  사업현황")
      
      text = ""
      for i in stock_dict['stock_business']:
        text += i + "\n"
      
      content += '<br>' + '<p>' + text.replace("\n", "<br>") + '</p><br>'
      
    if stock_dict['stock_index']:
      content += '<br>' + self.setquot(f"{stock_dict['stock_name']}  주가지표")
      
      content += self.setTable(stock_dict['stock_index'], 16, column = 3)

    content += '<br>' + self.setquot(f"{stock_dict['stock_name']} 재무정보")

    content += self.setTable(stock_dict['stock_finance'], 16)
    
    # content += '<br>' + '<p><a style="box-shadow: 5px 5px 15px 5px rgba(0,0,0,0.2)" href="https://url.kr/ay59du" target="_blank"><img src="https://moneyseo.cafe24.com/wp-content/uploads/2022/08/재테크카페에반다하-배너.png" alt=""></a></p>'
  
    content += '<br>' + '<p><a href="https://url.kr/ay59du" target="_blank"><img src="https://moneyseo.cafe24.com/wp-content/uploads/2022/08/재테크카페에반다하-배너.png" alt=""></a></p>'

    content += '<br>' + self.setquot("공모주일정")
    
    content += self.setTable(stock_dict['stock_schedule'], 14)
    
    content += '<br>' + self.setquot(f"{stock_dict['stock_name']} 공시정보")
    
    for i in stock_dict['stock_gongsi']:
      content += '<br>' + f'<a href="{i[i.find("https"):]}" target="_blank" rel="noopener">{i[:i.find("https")-1]}</a>' + '<br>'

    content += '<br>' + self.setquot(f"{stock_dict['stock_name']} 청약 참고사항")
    
    text = stock_dict['stock_notes']
    
    content += '<br>' + '<p>' + text.replace("\n", "<br>") + '</p><br>'

    content += '<br>' + '<h2 data-ke-size="size26"><span style="color: #ff0000"><b>👇재테크카페 바로가기👇 아래 사진 클릭!</b></span></h2>'

    # content += '<br>' + '<p><a style="box-shadow: 5px 5px 15px 5px rgba(0,0,0,0.2)" href="https://url.kr/ay59du" target="_blank"><img src="https://moneyseo.cafe24.com/wp-content/uploads/2022/08/재테크에반하다.png" alt=""></a></p>'

    content += '<br>' + '<p><a href="https://url.kr/ay59du" target="_blank"><img src="https://moneyseo.cafe24.com/wp-content/uploads/2022/08/재테크에반하다.png" alt=""></a></p>'

    content += '<br>' + '<p data-ke-size="size16"><b>* 이 페이지의 모든 정보는 사실과 다를 수 있으며 투자조언으로 활용하실 수 없습니다.</b></p>'

    return content

  def do_post(self, stock_name):
    try:
      with open(f"{stock_name}.json","r",encoding="utf-8") as read_file:
        stock_dict = json.load(read_file)
      
      isLoad = False
      if self.login():
        time.sleep(10)
        while not isLoad:
          titles = gw.getAllTitles()
          for i in titles:
            if "글쓰기" in i:
              isLoad = True
          time.sleep(1)
        win = pyautogui.getWindowsWithTitle("글쓰기")[0]   #카페 글쓰기 창 포커스(활성화)
        if win.isActive == False:   #창이 활성화되어있지 않으면 최소화/복구로 활성화 .activate()오류
          pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
          win.activate()

        self.click_elemen(self.driver.find_element(By.CSS_SELECTOR , "#editor-mode-layer-btn-open > i"))
        time.sleep(1)
        self.click_elemen(self.driver.find_element(By.ID, "editor-mode-html-text"))
        time.sleep(1)

        if stock_dict['stock_logo']:
          self.input_img(stock_dict['stock_logoAddress'])

        time.sleep(5)
        self.click_elemen(self.driver.find_element(By.CLASS_NAME, "CodeMirror-lines"))
        pyautogui.hotkey("alt", "right")
        time.sleep(0.5)
        pyautogui.hotkey("enter")

        content = self.htmlConvert(stock_dict)

        pyperclip.copy(str(content))
        time.sleep(1)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)

        self.click_elemen(self.driver.find_element(By.ID, "tagText"))
        time.sleep(1)

        for i in self.input_hashtag(stock_dict['stock_name']):
          pyperclip.copy(i)
          time.sleep(0.5)
          pyautogui.hotkey("ctrl", "v")
          time.sleep(0.5)
          pyautogui.hotkey(",")
          time.sleep(1)

        title = f"{stock_dict['stock_name']} 공모주 청약정보 | 청약정보/공모정보/기업정보/공시정보/참고사항/공모주전체일정"
        self.driver.find_element(By.CSS_SELECTOR, "textarea.textarea_tit").send_keys(title)
        time.sleep(1)

        self.click_elemen(self.driver.find_element(By.CLASS_NAME, "btn.btn-default"))
        time.sleep(1)
        self.click_elemen(self.driver.find_element(By.CSS_SELECTOR, "input#open20.form-radio.klink-linknew"))
        time.sleep(1)
        self.click_elemen(self.driver.find_elements(By.CSS_SELECTOR, "div.mce-widget.mce-btn.select-menu > button.mce-btn-type1")[1])
        time.sleep(1)
        self.click_elemen(self.driver.find_element(By.XPATH, "//*[contains(text(), '경제')]"))
        time.sleep(1)
        self.click_elemen(self.driver.find_element(By.XPATH, "//*[contains(text(), '공개 발행')]"))
        time.sleep(1)

        try:
          popup = Alert(self.driver)
          if "최대" in str(popup.text):
            popup.accept()
            self.driver.quit()
            return False
        except:
          self.driver.quit()
          return True
      else:
        print("로그인 실패")
        self.driver.quit()
        return False
    except Exception as e:
      print("오류 발생", e)
      self.driver.quit()
      return False
  