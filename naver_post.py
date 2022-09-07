# from contextlib import nullcontext
from selenium import webdriver
# from selenium.webdriver.remote.command import Command
# import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from wcwidth import wcswidth
import pyautogui
import pyperclip
import json
import random
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

class naverPost():
  def __init__(self, id, pw, url, proxy) -> None:
    if proxy:
      with open(proxy+".txt", 'r') as proxyLists:
        d = proxyLists.readlines()
        fileLists = list(map(lambda e: e.strip("\n"), d))
        random.shuffle(fileLists)
        options.add_argument('--proxy-server=%s' %fileLists[0])
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
    self.driver.get("https://nid.naver.com/nidlogin.login")
    time.sleep(1)
    self.driver.execute_script("document.getElementsByName('id')[0].value = \'" + self.id + "\'")
    time.sleep(1)
    self.driver.execute_script("document.getElementsByName('pw')[0].value=\'" + self.pw + "\'")
    time.sleep(1)
    self.click_elemen(self.driver.find_element(By.XPATH,'//*[@id="log.login"]'))
    time.sleep(1)
    if self.driver.current_url != "https://nid.naver.com/nidlogin.login":
      self.driver.get(self.url)
      return True
    else:
      return False

  def change_pontSize(self, size):
    self.driver.execute_script("window.scrollTo(0,0)")
    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-font-size-code-toolbar-button.se-property-toolbar-label-select-button'))))
    time.sleep(0.5)
    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, f"se-toolbar-option-text-button.se-toolbar-option-font-size-code-fs{size}-button"))))
    time.sleep(0.5)

  def undo_pontSize(self):
    self.driver.execute_script("window.scrollTo(0,0)")
    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-font-size-code-toolbar-button.se-property-toolbar-label-select-button'))))
    time.sleep(0.5)
    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, f"se-toolbar-option-text-button.se-toolbar-option-font-size-code-fs15-button"))))
    time.sleep(0.5)

  def change_pontBold(self):
    self.driver.execute_script("window.scrollTo(0,0)")
    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-bold-toolbar-button.se-property-toolbar-toggle-button'))))
    time.sleep(0.5)
    
  def undo_pontBold(self):
    self.driver.execute_script("window.scrollTo(0,0)")
    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-bold-toolbar-button.se-property-toolbar-toggle-button.se-is-selected'))))
    time.sleep(0.5)
    
  def input_img(self, stock_logoAddress):
    self.driver.execute_script("window.scrollTo(0,0)")
    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button'))))
    while True:
      titles = gw.getAllTitles()
      if "열기" in titles:
        break
      time.sleep(1)
    time.sleep(10)  
    pyperclip.copy(stock_logoAddress)
    time.sleep(0.5)
    pyautogui.hotkey("ctrl","v")
    time.sleep(0.5)
    pyautogui.hotkey("enter")
    time.sleep(0.5)
      
  def input_lineQuot(self, quotSentence): #라인&따음표
    self.driver.execute_script("window.scrollTo(0,0)")
    
    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-document-toolbar-select-option-button.se-text-icon-toolbar-select-option-button'))))
    time.sleep(0.5)
    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-toolbar-option-icon-button.se-toolbar-option-insert-quotation-quotation_underline-button'))))
    time.sleep(0.5)

    pyperclip.copy(quotSentence)
    time.sleep(0.5)
    pyautogui.hotkey("ctrl","v")
    time.sleep(0.5)
    pyautogui.hotkey("down")
    time.sleep(0.5)
    pyautogui.hotkey("down")
    time.sleep(0.5)
    pyautogui.hotkey("enter")
    time.sleep(0.5)
      
  def input_verticalLine(self, quotSentence, quotSource): #버티컬라인
    self.driver.execute_script("window.scrollTo(0,0)")

    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-document-toolbar-select-option-button.se-text-icon-toolbar-select-option-button'))))
    time.sleep(0.5)
    self.click_elemen(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-toolbar-option-icon-button.se-toolbar-option-insert-quotation-quotation_line-button'))))
    time.sleep(0.5)

    pyperclip.copy(quotSentence)
    time.sleep(0.5)
    pyautogui.hotkey("ctrl","v")
    time.sleep(0.5)
    pyautogui.hotkey("down")
    time.sleep(0.5)
    pyperclip.copy(quotSource)
    time.sleep(0.5)
    pyautogui.hotkey("ctrl","v")
    time.sleep(0.5)
    pyautogui.hotkey("down")
    time.sleep(0.5)
    pyautogui.hotkey("enter")
    time.sleep(0.5)

  def fmt(self, text, num):
    text = str(text)
    l = wcswidth(text)
    s = num-l
    
    if s <= 0:
      return 0
    return s

  def input_text(self, **kwargs):
    time.sleep(0.5)
    if str(type(kwargs['content'])) == "<class 'str'>": 
      if 'size' in kwargs:
        self.change_pontSize(kwargs['size'])
      if 'bold' in kwargs:
        self.change_pontBold()
      pyperclip.copy(kwargs['content'])
      time.sleep(0.5)
      pyautogui.hotkey("ctrl","v")
      time.sleep(0.5)
      if 'size' in kwargs:
        self.undo_pontSize()
      if 'bold' in kwargs:
        self.undo_pontBold()
    elif str(type(kwargs['content'])) == "<class 'dict'>":
      for i in range(len(kwargs['content']['column_list'])):
        if i == 0:
          pyperclip.copy(kwargs['content']['column_list'][i])
          time.sleep(0.5)
          pyautogui.hotkey("ctrl","v")
          self.input_space(self.fmt(kwargs['content']['column_list'][i], kwargs['width']))
        elif i == len(kwargs['content']['column_list'])-1:
          self.input_space(self.fmt(kwargs['content']['column_list'][-1], kwargs['width']))
          pyperclip.copy(kwargs['content']['column_list'][-1])
          time.sleep(0.5)
          pyautogui.hotkey("ctrl","v")
          self.input_enter()
        else:
          self.input_space(self.fmt(kwargs['content']['column_list'][i], kwargs['width']))
          pyperclip.copy(kwargs['content']['column_list'][i])
          time.sleep(0.5)
          pyautogui.hotkey("ctrl","v")
      for i in range(len(kwargs['content']['var_list'])):
        for j in range(len(kwargs['content']['column_list'])):
          if j % len(kwargs['content']['column_list']) == 0:
            pyperclip.copy(kwargs['content']['var_list'][i][0])
            time.sleep(0.5)
            pyautogui.hotkey("ctrl","v")
            self.input_space(self.fmt(kwargs['content']['var_list'][i][0], kwargs['width']))
          elif j % len(kwargs['content']['column_list']) == len(kwargs['content']['column_list'])-1:
            self.input_space(self.fmt(kwargs['content']['var_list'][i][-1], kwargs['width']))
            pyperclip.copy(kwargs['content']['var_list'][i][-1])
            time.sleep(0.5)
            pyautogui.hotkey("ctrl","v")
            self.input_enter()
          else:
            self.input_space(self.fmt(kwargs['content']['var_list'][i][j], kwargs['width']))
            pyperclip.copy(kwargs['content']['var_list'][i][j])
            time.sleep(0.5)
            pyautogui.hotkey("ctrl","v")
    else:
      for i in range(len(kwargs['content'])):
        if i % kwargs['column'] == 0:
          pyperclip.copy(kwargs['content'][i])
          time.sleep(0.5)
          pyautogui.hotkey("ctrl","v")
          self.input_space(self.fmt(kwargs['content'][i], kwargs['width']))
        elif i % kwargs['column'] == kwargs['column']-1:
          self.input_space(self.fmt(kwargs['content'][i], kwargs['width']))
          pyperclip.copy(kwargs['content'][i])
          time.sleep(0.5)
          pyautogui.hotkey("ctrl","v")
          self.input_enter()
        else:
          self.input_space(self.fmt(kwargs['content'][i], kwargs['width']))
          pyperclip.copy(kwargs['content'][i])
          time.sleep(0.5)
          pyautogui.hotkey("ctrl","v")
    self.input_enter()
          
  def input_enter(self):
    time.sleep(0.5)
    pyautogui.hotkey("enter")
    time.sleep(0.5)

  def input_space(self, num):
    time.sleep(0.5)
    for i in range(num):
      pyautogui.press('space')
    time.sleep(0.5)

  def input_hashtag(self, text):
    stock_hashtag = [text,text+"공모",text+"청약",text+"공모주",text+"상장",text+"주간사",text+"주관사",text+"공모가",text+"일정",text+"정보"]
    element = self.driver.find_element(By.CLASS_NAME , 'tag_input')
    for i in stock_hashtag:
      element.send_keys(i+" ")
      time.sleep(0.5)
    
  def register(self, text):
      self.driver.execute_script("window.scrollTo(0,0)")
      
      time.sleep(0.5)
      self.driver.find_element(By.CLASS_NAME ,'textarea_input').send_keys(text)
      time.sleep(0.5)
      self.click_elemen(self.driver.find_element(By.XPATH, '//span[contains(text(),"등록")]')) #등록 버튼 클릭

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
            if "카페 글쓰기" in i:
              isLoad = True
          time.sleep(1)
        win = pyautogui.getWindowsWithTitle("카페 글쓰기")[0]   #카페 글쓰기 창 포커스(활성화)
        if win.isActive == False:   #창이 활성화되어있지 않으면 최소화/복구로 활성화 .activate()오류
          pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
          win.activate()

          
        if stock_dict['stock_logo']:
          self.input_img(stock_dict['stock_logoAddress'])
        
        self.input_lineQuot("청약정보")

        text = f"{stock_dict['stock_name']}\n총 공모주식수 : {stock_dict['stock_numPublicOffer']}\n일반투자자 공모주식수 : {stock_dict['stock_numNormalOffer']}\n\n청약일 : {stock_dict['stock_subscriptionDay']}\n환불일 : {stock_dict['stock_refundDay']}\n상장일 : {stock_dict['stock_listingDay']}\n주간사 : {stock_dict['stock_manager']}"
        
        self.input_text(content = text)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.input_verticalLine(stock_dict['stock_managerInfo'], "주간사 별 주식수 및 일반 청약한도")
        
        self.input_lineQuot("공모정보")
        
        text = f"희망공모가격 : {stock_dict['stock_hopePrice']}\n희망공모금액 : {stock_dict['stock_hopeMount']}\n청약경쟁률 : {stock_dict['stock_competition']}"
        
        self.input_text(content = text)
        
        self.input_lineQuot("기업정보")
        
        text = f"종목코드 : {stock_dict['stock_code']}\n분류 : {stock_dict['stock_categori']}"
        
        self.input_text(content = text)
        
        self.input_enter()
        
        if stock_dict['stock_index']:
          self.input_text(content = "주가지표", size = 24, bold = True)
        
          self.input_text(content = stock_dict['stock_index'],column = 4,width = 30)
          
          self.input_enter()
        
        if stock_dict['stock_business']:
          self.input_text(content = "사업현황", size = 24, bold = True)
          
          for i in stock_dict['stock_business']:
            self.input_text(content = i)
          
          self.input_enter()

        self.input_text(content = "재무정보", size = 24, bold = True)
        
        self.input_text(content = stock_dict['stock_finance'], width = 30)

        self.input_lineQuot("공시정보")
        
        for i in stock_dict['stock_gongsi']:
          self.input_text(content = i)
        
        self.input_lineQuot("참고사항")
        
        self.input_text(content = stock_dict['stock_notes'])
        
        self.input_lineQuot("공모주 일정")
        
        self.input_text(content = stock_dict['stock_schedule'], width = 30)
        
        text = "\n\n* 이 페이지의 모든 정보는 사실과 다를 수 있으며 투자조언으로 활용하실 수 없습니다."
        
        self.input_text(content = text, bold = True)
        
        self.input_hashtag(stock_dict['stock_name'])
        
        title = f"{stock_dict['stock_name']} 공모주 청약정보 | 청약정보/공모정보/기업정보/공시정보/참고사항/공모주전체일정"
        
        self.register(title)
        
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

