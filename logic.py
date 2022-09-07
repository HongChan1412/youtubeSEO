#-*- coding:utf-8 -*-
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
import math
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import os
os.environ['WDM_LOG_LEVEL'] = '0'
from logger import __get_logger
logger = __get_logger()

pc_headers = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36', #chrome 88
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36', #chrome 88
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36', #chrome mac
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36', #chrome mac
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36', #chrome 87
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', #chrome 87
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', #chrome 86
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15', #safari 13
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15', #safari 14
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15', #safari 12
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15', #safari 14
]

mobile_headers = [
    'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
    'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G955U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36'
]

def getProxy(proxy_list):
  try:
    with open(proxy_list, 'r') as proxyLists:
      d = proxyLists.readlines()
      fileLists = list(map(lambda e: e.strip("\n"), d))
      random.shuffle(fileLists)
      return fileLists[0]
  except Exception as e:
    print("파일 읽기 실패")
    return False
      
class pcLogic():
  def __init__(self, keyword, title, channelName, channelLink, link, seo_opt, agent, proxy_opt, device, proxy_list) -> None:
    try:
      self.status_message = ''
      self.urls = []
      self.channelName = channelName
      self.device = device
      self.result = ""
      chrome_options = webdriver.ChromeOptions()
      if proxy_opt == 'IP 리스트 선택':
        self.ip = getProxy(proxy_list)
        chrome_options.add_argument('--proxy-server=%s' %self.ip)
      chrome_options.add_argument('blink-settings=imagesEnabled=false') #이미지 로딩 X
      chrome_options.add_argument('headless') #창 띄우지않음
      chrome_options.add_argument("disable-gpu")
      chrome_options.add_argument("lang=ko_KR")
      #chrome_options.add_argument('--incognito')
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument(f"user-agent={agent}")
      chrome_options.add_argument('--disable-blink-features=AutomationControlled')
      chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
      chrome_options.add_argument('--ignore-certificate-errors')
      chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
      chrome_options.add_experimental_option('useAutomationExtension', False)
      chrome_options.add_argument("--disable-setuid-sandbodx")
      chrome_options.add_argument("--disable-dev-shm-usage")
      chrome_options.add_argument("--disable-infobars")
      chrome_options.add_argument("--disable-browser-side-navigation")
      prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
      chrome_options.add_experimental_option('prefs', prefs)
      print(f"키워드: {keyword}\n제목: {title}\n채널링크: {channelLink}\n채널이름: {channelName}\n영상링크: {link}\n접속방식: {seo_opt}\n기기: {device}")
      try :
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.driver.implicitly_wait(30)
        self.driver.delete_all_cookies()
      except Exception as e:
        self.status_message = "chromedriver error"
        logger.error([e.args])
        self.result = False
        return
      self.wait = WebDriverWait(self.driver, 30)
      print(keyword, title, channelName, channelLink, link, seo_opt,agent)
      if device == 'PC':
        if seo_opt == "유튜브검색":
          self.result = self.youtubesearchTrafficPC(keyword, title)
        elif seo_opt == "채널검색":
          self.result = self.channelsearchTrafficPC(channelName, channelLink, title)
        elif seo_opt == "링크접속":
          self.reuslt = self.linkTrafficPC(link)
        elif seo_opt == "추천영상접속":
          self.result = self.recommendsearchTrafficPC(link, channelName)
      else:
        if seo_opt == "유튜브검색":
          self.result = self.youtubesearchTrafficM(keyword, title)
        elif seo_opt =="채널검색":
          self.result = self.channelsearchTrafficM(channelName, channelLink, title)
        elif seo_opt == "링크접속":
          self.result = self.linkTrafficM(link)
        elif seo_opt == "추천영상접속":
          self.result = self.recommendsearchTrafficM(link, channelName)
      print("종료 결과: ",self.result)
    except Exception as e:
      self.status_message = "※오류발생※"
      self.driver.quit()
      logger.error([e.args])
      self.result = False
      return
  
  def click_elemen(self, element):
    try:
      WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(element)).click()
    except:
      self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
      self.driver.execute_script("arguments[0].click();", element)
      
  def save_csv(self,seo_rank,keyword,title,view):
    try: 
      data = pd.read_csv(f"순위변동LOG_{self.channelName}채널_{self.device}.csv",encoding="utf-8-sig")
      data_insert = {'키워드':keyword,'제목':title,'처음조회수':view,'검색처음순위':seo_rank}
      if (data['키워드'] == keyword).any() :
        first_rank = int(data['검색처음순위'].values[data['키워드']==keyword])
        if first_rank > seo_rank:
          var_rank = first_rank - seo_rank
          res = f'상위 {seo_rank}번째({var_rank} 상승)'
          for i in range(1,12):
            if i == 11:
              data.loc[data['키워드']==keyword,'10+번째 순위변동'] = res 
              break
            if not data.loc[data['키워드']==keyword,f'{i}번째 순위변동'].any():
              if i == 1:
                data.loc[data['키워드']==keyword,f'{i}번째 순위변동'] = res 
                break
              else:
                if res != data[f'{i-1}번째 순위변동'].values[data['키워드']==keyword]:
                  data.loc[data['키워드']==keyword,f'{i}번째 순위변동'] = res
                break   
        elif first_rank < seo_rank:
          var_rank = seo_rank - first_rank
          res = f'상위 {seo_rank}번째({var_rank} 하락)'
          for i in range(1,12):
            if i == 11:
              data.loc[data['키워드']==keyword,'10+번째 순위변동'] = res 
              break
            if not data.loc[data['키워드']==keyword,f'{i}번째 순위변동'].any():
              if i == 1:
                data.loc[data['키워드']==keyword,f'{i}번째 순위변동'] = res 
                break
              else:
                if res != data[f'{i-1}번째 순위변동'].values[data['키워드']==keyword]:
                  data.loc[data['키워드']==keyword,f'{i}번째 순위변동'] = res
                break    
      else:
        data = data.append(data_insert, ignore_index=True)
      data.loc[data['키워드']==keyword,'마지막조회수'] = view  
      data = data.sort_values(by=['제목'], ascending=False)
      data = data.set_index('제목', inplace=False).reset_index()
      data.to_csv(f"순위변동LOG_{self.channelName}채널_{self.device}.csv",encoding='utf-8-sig',index=False)
      print(data)
      return True
    except Exception as e:
      self.status_message = "※파일 저장 중 오류발생※"
      self.driver.quit()
      logger.error([e.args])
      return False
      
  def adSkip_StayPC(self):
    time.sleep(4)
    try: 
      play = self.driver.find_elements(By.CSS_SELECTOR, "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > button")
      if play[0].get_attribute('title') == "재생(k)":
        if WebDriverWait(self.driver, 12).until(EC.element_to_be_clickable(play[0])):
          play[0].click()
          print("재생안돼있음")
      else:
        print("재생돼있음")
      ad = self.driver.find_elements(By.CLASS_NAME, "ytp-ad-skip-button-container")
      if ad:
        if WebDriverWait(self.driver, 12).until(EC.element_to_be_clickable(ad[0])):
          ad[0].click()                               
          print("광고1제거")
      else:
        print("광고없음")
      print("체류시작")
      video_len = int(self.driver.execute_script("return document.getElementById('movie_player').getDuration()"))
      durate = random.randint(math.ceil(0.7*video_len),video_len)
      print(durate)
      time.sleep(durate)
      print("체류완료")
      self.status_message = "성공"
      return True
    except TimeoutException:
      self.status_message = "※Timeout 오류발생※"
      self.driver.quit()
      return False
    except ElementNotInteractableException:
      self.status_message = "※클릭할 수 없는 element 오류발생※"
      self.driver.quit()
      return False
    except NoSuchElementException:
      self.status_message = "※element를 찾지 못함 오류발생※"
      self.driver.quit()
      return False
    except Exception as e:
      self.status_message = "※광고 스킵 중 오류발생※"
      self.driver.quit()
      logger.error([e.args])
      return False
    
  def adSkip_StayM(self):
    time.sleep(4)
    try:
      element = self.driver.find_elements(By.CSS_SELECTOR, "#movie_player > div.ytp-cued-thumbnail-overlay > button")
      if element[0].is_displayed():
        element[0].click()
      
      mute = self.driver.find_element(By.CLASS_NAME, "ytp-unmute-inner")
      if mute.is_displayed():
        mute.click()
        print("음소거 해제 완료",end=" ")
      else:
        print("음소거 안돼있음",end=" ")
      
      ad = self.driver.find_elements(By.CLASS_NAME, "ytp-ad-skip-button-container")
      if ad:
        if WebDriverWait(self.driver,12).until(EC.element_to_be_clickable(ad[0])):
          ad[0].click()
          print("광고1제거",end=" ")
      else:
        print("광고없음",end=" ")
      
      print("체류시작")
      video_len = int(self.driver.execute_script("return document.getElementById('movie_player').getDuration()"))
      durate = random.randint(math.ceil(0.7*video_len),video_len)
      print(durate)
      time.sleep(durate)
      print("체류완료")
      self.status_message = "성공"
      return True
    except TimeoutException:
      self.status_message = "※Timeout 오류발생※"
      self.driver.quit()
      return False
    except ElementNotInteractableException:
      self.status_message = "※클릭할 수 없는 element 오류발생※"
      self.driver.quit()
      return False
    except NoSuchElementException:
      self.status_message = "※element를 찾지 못함 오류발생※"
      self.driver.quit()
      return False
    except Exception as e:
      self.status_message = "※광고 스킵 중 오류발생※"
      self.driver.quit()
      logger.error([e.args])
      return False

  def linkTrafficPC(self, link):
    print("linkTrafficPC")
    try:
      self.driver.get(link)
      if self.adSkip_StayPC():
        self.driver.quit()
        return True
      else:
        return False
    except TimeoutException:
      self.status_message = "※Timeout 오류발생※"
      self.driver.quit()
      return False
    except Exception as e:
      self.driver.quit()
      self.status_message = "※오류발생※"
      logger.error([e.args])
      return False

  def linkTrafficM(self, link):
    print("linkTrafficM")
    try:
      self.driver.get(link)
      if self.adSkip_StayM():
        self.driver.quit()
        return True
      else:
        return False
    except TimeoutException:
      self.status_message = "※Timeout 오류발생※"
      self.driver.quit()
      return False
    except Exception as e:
      self.driver.quit()
      self.status_message = "※오류발생※"
      logger.error([e.args])
      return False
    
  def youtubesearchTrafficPC(self, keyword, title):
    print("youtubesearchTrafficPC")
    start_url = "https://www.youtube.com"
    isFind = False
    len_elements = 0
    try:
      self.driver.get(start_url)
      time.sleep(5)
      element = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-input"]')))
      self.click_elemen(element)
      element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-form"]/div/div/div/div[2]/input')))
      element.send_keys(keyword)
      element.send_keys(Keys.RETURN)
      time.sleep(5)
      
      while True:
        rank = 0
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        elements = soup.find_all("a",{"id":"video-title"})
        
        for i in elements:
          rank += 1
          if i['title'] == title:
            try:
              self.click_elemen(self.driver.find_element(By.XPATH, f"""//*[contains(text(), "{title}")]"""))
            except:
              self.click_elemen(self.driver.find_element(By.XPATH, f"""//*[contains(text(), '{title}')]"""))
            view = i['aria-label'][i['aria-label'].rfind(" ")+1:]
            isFind = True
            break
        
        if isFind:
          break
        
        if len(elements) >= 1000:
          self.driver.quit()
          self.status_message = "※더이상 동영상을 찾을 수 없음※"
          return False
          
        self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)
        
        if len(elements) == len_elements:
          self.driver.quit()
          self.status_message = "※더이상 동영상을 찾을 수 없음※"
          return False
        
        len_elements = len(elements)
      
      if self.save_csv(rank, keyword, title, view):
        if self.adSkip_StayPC():
          self.driver.quit()
          return True
      
      return False
    except TimeoutException:
      self.status_message = "※Timeout 오류발생※"
      self.driver.quit()
      return False
    except ElementNotInteractableException:
      self.status_message = "※클릭할 수 없는 element 오류발생※"
      self.driver.quit()
      return False
    except NoSuchElementException:
      self.status_message = "※element를 찾지 못함 오류발생※"
      self.driver.quit()
      return False
    except Exception as e:
      self.driver.quit()
      self.status_message = "※오류발생※"
      logger.error([e.args])
      return False

  def youtubesearchTrafficM(self, keyword, title):
    print("youtubesearchTraffic")
    start_url = "https://www.youtube.com"
    len_elements = 0
    isFind = False
    try:
      self.driver.get(start_url)
      time.sleep(5)
      element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytm-app/ytm-mobile-topbar-renderer/header/div/button")))
      element.click()
      element = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ytm-app/ytm-mobile-topbar-renderer/header/ytm-searchbox/form/div/input")))
      element.send_keys(keyword)
      element.send_keys(Keys.RETURN)
      time.sleep(5)
      
      while True:
        rank = 0
      
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        elements = soup.find_all("a",{"class":"compact-media-item-metadata-content"})
      
        for i in elements:
          rank += 1
          if i.find("h4").text == title:
            try:
              self.click_elemen(self.driver.find_element(By.XPATH, f"""//*[contains(text(), "{title}")]"""))
            except:
              self.click_elemen(self.driver.find_element(By.XPATH, f"""//*[contains(text(), '{title}')]"""))
            view = i.find("div",{"class":"compact-media-item-stats small-text"}).text[i.find("div",{"class":"compact-media-item-stats small-text"}).text.rfind(" ")+1:]
            isFind = True
            break     
          
        if isFind:
          break 
          
        if len(elements) >= 1000:
          self.driver.quit()
          self.status_message = "※더이상 동영상을 찾을 수 없음※"
          return False
      
        self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)
        
        if len(elements) == len_elements:
          self.driver.quit()
          self.status_message = "※더이상 동영상을 찾을 수 없음※"
          return False
        
        len_elements = len(elements)
        
      if self.save_csv(rank, keyword, title, view):
        if self.adSkip_StayPC():
          self.driver.quit()
          return True
        
      return False

    except TimeoutException:
      self.status_message = "※Timeout 오류발생※"
      self.driver.quit()
      return False
    except ElementNotInteractableException:
      self.status_message = "※클릭할 수 없는 element 오류발생※"
      self.driver.quit()
      return False
    except NoSuchElementException:
      self.status_message = "※element를 찾지 못함 오류발생※"
      self.driver.quit()
      return False
    except Exception as e:
      self.driver.quit()
      self.status_message = "※오류발생※"
      logger.error([e.args])
      return False
      
  def channelsearchTrafficPC(self, channelName, channelLink, title):
    print("channelsearchTrafficPC")
    j = 1
    start_url = "https://www.youtube.com"
    try:
      self.driver.get(start_url)
      time.sleep(5)
      element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-input"]')))
      element.click()
      element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-form"]/div/div/div/div[2]/input')))
      element.send_keys(channelName)
      element.send_keys(Keys.RETURN)
      time.sleep(5)
      element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/ytd-toggle-button-renderer/a')))
      element.click()
      time.sleep(0.5)
      searchFilter = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse-content"]/ytd-search-filter-group-renderer[2]')))
      searchFilter.click()
      time.sleep(0.5)
      click_list_2 = searchFilter.find_elements(By.ID, 'endpoint')
      click_list_2[1].click()
      time.sleep(0.5)
      for i in range(1,10):
        nowLink = self.wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer[{i}]/div/div[1]/a'))).get_attribute('href')
        if nowLink == channelLink:
          element = self.wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer[{i}]/div/div[1]/a/div/yt-img-shadow/img')))
          self.driver.execute_script("arguments[0].click();", element)
          time.sleep(5)
          break
      element = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-browse[2]/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/tp-yt-app-toolbar/div/div/tp-yt-paper-tabs/div/div/tp-yt-paper-tab[2]/div')))
      self.driver.execute_script("arguments[0].click();", element)
      time.sleep(5)
      while True:
        nowTitle = self.wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/ytd-app/div/ytd-page-manager/ytd-browse[2]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[{j}]/div[1]/div[1]/div[1]/h3/a')))
        if nowTitle.get_attribute("title").replace(" ","") == title.replace(" ",""):
          self.driver.execute_script("arguments[0].scrollIntoView(true);", nowTitle)
          self.driver.execute_script("arguments[0].click();", nowTitle)
          if self.adSkip_StayPC():
            self.driver.quit()
            print("시청완료")
            return True
          else:
            return False
        j += 1
    except TimeoutException:
      self.status_message = "※Timeout 오류발생※"
      self.driver.quit()
      return False
    except ElementNotInteractableException:
      self.status_message = "※클릭할 수 없는 element 오류발생※"
      self.driver.quit()
      return False
    except NoSuchElementException:
      self.status_message = "※element를 찾지 못함 오류발생※"
      self.driver.quit()
      return False
    except Exception as e:
      self.driver.quit()
      self.status_message = "※오류발생※"
      logger.error([e.args])
      return False

  def channelsearchTrafficM(self, channelName, channelLink, title):
    print("channelsearchTrafficM")
    j = 1
    k = 1
    start_url = "https://www.youtube.com"
    try:
      self.driver.get(start_url)
      time.sleep(5)
      element = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ytm-app/ytm-mobile-topbar-renderer/header/div/button")))
      element.click()
      element = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ytm-app/ytm-mobile-topbar-renderer/header/ytm-searchbox/form/div/input")))
      element.send_keys(channelName)
      element.send_keys(Keys.RETURN)
      time.sleep(5)
      element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#header-bar > header > div > div > button.icon-button.search-filter-icon.topbar-menu-button-avatar-button')))
      self.driver.execute_script("arguments[0].click();", element)
      time.sleep(0.5)
      element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select")))
      element.click()
      time.sleep(0.5)
      element.send_keys(Keys.ARROW_DOWN)
      element.send_keys(Keys.RETURN)
      time.sleep(0.5)
      while True:
        for i in range(1,10):
          element = self.driver.find_elements(By.XPATH, f"/html/body/ytm-app/div[1]/ytm-search/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer[{j}]/lazy-list/ytm-compact-channel-renderer[{i}]/div/div/a")
          if element:
            print(element[0].get_attribute("href"))
            if element[0].get_attribute("href") == channelLink:
              self.driver.execute_script("arguments[0].click();", element[0])
              time.sleep(5)
              element = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ytm-app/div[1]/ytm-browse/ytm-single-column-browse-results-renderer/div[1]/a[2]")))
              self.driver.execute_script("arguments[0].click();", element)
              time.sleep(5)
              while True:
                nowTitle = self.wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/ytm-app/div[1]/ytm-browse/ytm-single-column-browse-results-renderer/div[2]/div[2]/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[{k}]/div/div/a/h4")))
                print(nowTitle.text)
                if nowTitle.text.replace(" ","") == title.replace(" ",""):   
                  self.driver.execute_script("arguments[0].scrollIntoView(true);", nowTitle)
                  self.driver.execute_script("arguments[0].click();", nowTitle)
                  if self.adSkip_StayM():
                    self.driver.quit()
                    print("시청완료")
                    return True     
                  else:
                    return False
                k += 1     
          else:
            break
        j += 1  
    except TimeoutException:
      self.status_message = "※Timeout 오류발생※"
      self.driver.quit()
      return False
    except ElementNotInteractableException:
      self.status_message = "※클릭할 수 없는 element 오류발생※"
      self.driver.quit()
      return False
    except NoSuchElementException:
      self.status_message = "※element를 찾지 못함 오류발생※"
      self.driver.quit()
      return False
    except Exception as e:
      self.driver.quit()
      self.status_message = "※오류발생※"
      logger.error([e.args])
      return False
     
  def recommendsearchTrafficPC(self, link, channelName):
    print("reommendsearchTrafficPC")
    start_url = link
    action = ActionChains(self.driver)
    try:
      self.driver.get(start_url)
      time.sleep(5)
      self.adSkip_StayPC()
      while True:
        i = 1
        while True:
          element = self.driver.find_elements(By.XPATH, f"/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[11]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[{i}]/div[1]/div/div[1]/a/div/ytd-video-meta-block/div[1]/div[1]/ytd-channel-name/div/div/yt-formatted-string")
          if element:
            action.move_to_element(element[0]).perform()
            if element[0].text == channelName:
              self.driver.execute_script("arguments[0].scrollIntoView(true);", element[0])
              self.driver.execute_script("arguments[0].click();", element[0])
              if self.adSkip_StayPC():
                self.urls.append(self.driver.current_url)
                print(self.urls)
                if len(self.urls) == 5:
                  self.status_message = f'5개 동영상 이동완료 성공'
                  return True
                break
              return False
          else:
            element = self.driver.find_elements(By.XPATH, "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[11]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-continuation-item-renderer/div[2]/ytd-button-renderer/a/tp-yt-paper-button/yt-formatted-string")
            if element:
              self.driver.execute_script("arguments[0].scrollIntoView(true);", element[0])
              self.driver.execute_script("arguments[0].click();", element[0])
              time.sleep(1)
            else:
              self.driver.quit()
              self.status_message = f'※더이상 동영상을 찾을 수 없음 {len(self.urls)}개 동영상 이동완료 성공※'
              return True          
          i += 1
    except TimeoutException:
      self.status_message = "※Timeout 오류발생※"
      self.driver.quit()
      return False
    except ElementNotInteractableException:
      self.status_message = "※클릭할 수 없는 element 오류발생※"
      self.driver.quit()
      return False
    except NoSuchElementException:
      self.status_message = "※element를 찾지 못함 오류발생※"
      self.driver.quit()
      return False
    except Exception as e:
      self.driver.quit()
      logger.error([e.args])
      self.status_message = f'※오류발생※'
      return False

  def recommendsearchTrafficM(self, link, channelName):
    print("reommendsearchTrafficM")
    start_url = link
    try:
      self.driver.get(start_url)
      time.sleep(5)
      self.adSkip_StayM()
      while len(self.urls) < 5:
        j = 0
        isFind = False
        while True:
          element = self.driver.find_elements(By.CLASS_NAME, "media-item-metadata")
          print(len(element))
          for i in range(j,len(element)):
            print(i, element[i].text.split("\n")[1].split("•")[0])
            if element[i].text.split("\n")[1].split("•")[0] == channelName:
              element1 = self.driver.find_elements(By.XPATH, f"/html/body/ytm-app/div[1]/ytm-watch/ytm-single-column-watch-next-results-renderer/ytm-item-section-renderer[3]/lazy-list/ytm-video-with-context-renderer[{i+1}]/ytm-media-item/a/div/img")
              if element1:
                self.driver.execute_script("arguments[0].click();", element1[0])
              else:
                element2 = self.driver.find_elements(By.XPATH, f"/html/body/ytm-app/div[1]/ytm-watch/ytm-single-column-watch-next-results-renderer/ytm-item-section-renderer[2]/lazy-list/ytm-video-with-context-renderer[{i+1}]/ytm-media-item/a/div/img")
                self.driver.execute_script("arguments[0].click();", element2[0])
              if self.adSkip_StayM():
                self.urls.append(self.driver.current_url) 
                print(self.urls)
                isFind = True
                break
              else:
                return False
            j+=1
          if isFind:
            break
          height = self.driver.execute_script("return document.body.scrollHeight")
          self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          time.sleep(1)
          new_height = self.driver.execute_script("return document.body.scrollHeight")
          if new_height == height:
            self.status_message = f'※더이상 동영상을 찾을 수 없음 {len(self.urls)}개 동영상 이동완료 성공※'
            self.driver.quit()
            return True 
      else:
        self.status_message = f'5개 동영상 이동완료 성공'
        return True    
          
    except TimeoutException:
      self.status_message = "※Timeout 오류발생※"
      self.driver.quit()
      return False
    except ElementNotInteractableException:
      self.status_message = "※클릭할 수 없는 element 오류발생※"
      self.driver.quit()
      return False
    except NoSuchElementException:
      self.status_message = "※element를 찾지 못함 오류발생※"
      self.driver.quit()
      return False
    except Exception as e:
      self.driver.quit()
      logger.error([e.args])
      self.status_message = f'※오류발생※'
      return False
  
def qweqwe(x):
  keywords = x[1].split(',')
  keyword = random.choice(keywords).strip()
  opts = x[5]
  if len(opts) == 3:
    opt = random.choices(opts, weights= [3,3,1])[0]
  else:
    opt = random.choice(opts)
  if x[6] == 'PC':
    header = random.choice(pc_headers)
  else:
    header = random.choice(mobile_headers)
    x[3] = x[3].replace("www","m")
  z = pcLogic(keyword, x[0], x[2], x[3], x[4], opt, header, x[7], x[6], x[8])
  if x[7] == '자체 IP 변경':
      try:
        req = requests.get("http://ipconfig.kr")
        ip = (re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',req.text)[1])
      except:
        ip = "ipconfig.kr 오류"
  else:
    ip = z.ip
  msg = {'status': z.status_message, 'post': x[0], 'option': opt, 'keyword': keyword, 'link': x[4], 'urls': z.urls, 'channelName':x[2], 'device':x[6],'proxy':ip,'res':z.result}
  print(msg)
  del z
  return msg
  
def multiprocessingq(func, args, workers):
  with ThreadPoolExecutor(workers) as ex:
     z = ex.map(func, args)
     return z
      


  

      
    
    
      