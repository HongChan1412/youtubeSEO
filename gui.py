#-*- coding:utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import feedparser
from ui import Ui_MainWindow
from multiprocessing import freeze_support
from logger import __get_logger
logger = __get_logger()
import logic
import pandas as pd
import time
    
class Worker(QObject) :
  finished = pyqtSignal()
  progress = pyqtSignal(str) 
  quit_process = 0
  
  def auto_update(self):
    while True:
      self.seo = []
      if self.channel == "주식스터디":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCQs5EP_QjBXjOzOkV-ETpog")#주식스터디
        channelLink = "https://www.youtube.com/c/%EC%A3%BC%EC%8B%9D%EC%8A%A4%ED%84%B0%EB%94%94"
      elif self.channel == "주식전망":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UChnhVGiF3RcMwz0EUNc6ovw")#주식전망
        channelLink = "https://www.youtube.com/c/%EC%A3%BC%EC%8B%9D%EB%A7%88%EC%8A%A4%ED%84%B0"
      elif self.channel == "주식사는법":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC7Rt-QEDilvmZBuaRh5mV7Q")#주식사는법
        channelLink = "https://www.youtube.com/c/%EC%A3%BC%EC%8B%9D%EC%82%AC%EB%8A%94%EB%B2%95"
      elif self.channel == "치트키":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC7Rt-QEDilvmZBuaRh5mV7Q")#치트키
        channelLink = "https://www.youtube.com/c/%EC%B9%98%ED%8A%B8%ED%82%A4"
      elif self.channel == "주식LIVE":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCUtKih4a5UkiYlZciXrPwQA")#주식LIVE
        channelLink = "https://www.youtube.com/channel/UCUtKih4a5UkiYlZciXrPwQA"
      elif self.channel == "세력수급포착":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCCuY9hs95Wl2fTZxMJy5D1w")#세력수급포착 
        channelLink = "https://www.youtube.com/channel/UCCuY9hs95Wl2fTZxMJy5D1w"
      elif self.channel == "주식테라피":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCw17GTk0hHHS-3BJ10Bp8mQ")#주식테라피
        channelLink = "https://www.youtube.com/channel/UCw17GTk0hHHS-3BJ10Bp8mQ"
      elif self.channel == "주식 리포트TV":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC05pM0iYOUdyOlurcfGkF5g")#주식 리포트TV
        channelLink = "https://www.youtube.com/channel/UC05pM0iYOUdyOlurcfGkF5g"
      elif self.channel == "신분상승":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC7JZwVEnnccvmvalgv3Cshg")#신분상승
        channelLink = "https://www.youtube.com/channel/UC7JZwVEnnccvmvalgv3Cshg"
      elif self.channel == "코인스쿨 : 대한민국 NO.1 코인 채널":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCsXxjI960QybYHYuJeQtvDA")#코인스쿨
        channelLink = "https://www.youtube.com/channel/UCsXxjI960QybYHYuJeQtvDA"
      elif self.channel == "재테크에 반하다♡ : 대한민국 NO.1 재테크 채널":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC7Rt-QEDilvmZBuaRh5mV7Q")#재테크에반하다
        channelLink = "https://www.youtube.com/channel/UC7Rt-QEDilvmZBuaRh5mV7Q"
      else:
        self.progress.emit("※채널명 입력 확인※")
        return False
      youtube_seo = {'제목':[],'키워드':[],'채널링크':[],'채널이름':[],'영상링크':[]}
      youtube_seo = pd.DataFrame(youtube_seo)
      cnt = 0
      for k in parse_rss.entries:
        if self.search_opt == ["추천영상접속"] and cnt >= 1:
          break
        # if cnt >= 5:
        if cnt >= 1:
          break
        if "주식스터디 직통번호: 070-4820-2877" in k.summary:
          continue
        summary = k.summary
        start_index = summary.rfind("\n")
        keyword_list = []
        if start_index > 0:
          keyword = list(set(summary[start_index+1:].strip("#").replace(" ","").split("#")))
          for i in range(len(keyword)):
            for j in keyword[i].split(","):
              keyword_list.append(j.strip())
          if len(keyword_list) < 5:
            continue
          data_insert = {'제목':k.title,'키워드':",".join(keyword_list),'채널링크':channelLink,'채널이름':self.channel, '영상링크':k.link}
          youtube_seo = youtube_seo.append(data_insert, ignore_index=True)
          cnt += 1
      result = f"AUTO_SEO_{self.channel}.csv"
      youtube_seo.to_csv(result,encoding='utf-8-sig',index=False)

      data = pd.read_csv(result,encoding="utf-8-sig")  
      if len(data) > 0:
        break
    
    for i in range(len(data)):
      input_search = f'영상 제목 >> {data.iloc[i]["제목"]}\n키워드 >> {data.iloc[i]["키워드"]}\n채널 이름 >> {data.iloc[i]["채널이름"]}\n채널 링크 >> {data.iloc[i]["채널링크"]}\n영상 링크 >> {data.iloc[i]["영상링크"]}\n조회수 >> {self.view_cnt}\n검색방법 >> {self.search_opt}\n기기 선택 >> {self.device_opt}\n프록시 선택 >> {self.proxy_opt}'
      self.seo.append([data.iloc[i]['제목'],data.iloc[i]['키워드'],data.iloc[i]['채널이름'],data.iloc[i]['채널링크'],data.iloc[i]['영상링크'],self.search_opt,self.device_opt,self.proxy_opt,self.proxy])
      self.progress.emit("{0:-^100}".format(f'{i+1}번 봇'))
      self.progress.emit(input_search)
    self.progress.emit("\n"+"{0:=^96}".format("SEO 최신화 완료")+"\n")
    return True
  
  def run(self):
    try:
      bot = []
      success = 0
      fail = 0
      self.progress.emit("\n"+"{0:=^96}".format("프로세스 시작")+"\n")
      if self.auto_seo:
        if not self.auto_update():
          return self.finished.emit()
      for j in range(len(self.seo)):
        if "유튜브검색" in self.seo[j][5]:
          rankData = {'제목':[],'키워드':[],'처음조회수':[],'마지막조회수':[],'검색처음순위':[],'1번째 순위변동':[],'2번째 순위변동':[],'3번째 순위변동':[],'4번째 순위변동':[],'5번째 순위변동':[],'6번째 순위변동':[],'7번째 순위변동':[],'8번째 순위변동':[],'9번째 순위변동':[],'10번째 순위변동':[],'10+번째 순위변동':[]}
          data = pd.DataFrame(rankData)
          result = f"순위변동LOG_{self.seo[j][2]}채널_{self.seo[j][6]}.csv"
          data.to_csv(result,encoding='utf-8-sig',index=False)
      for i in range(self.view_cnt):
        if self.quit_process == 1:
          break
        if self.auto_seo and i%5 == 0 and i >=5:
          self.auto_update()
        self.progress.emit("{0:-^98}".format(f'{i+1}번째 시작'))
        print(i+1,"번째시작")
        msg = logic.multiprocessingq(logic.qweqwe, self.seo, len(self.seo))
        k = 1
        for j in msg:
          now = time.localtime()
          now = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
          if j['option'] == '링크접속':
            self.progress.emit(f'[{k}번봇][{j["device"]}][{j["proxy"]}][{j["option"]}][{j["link"]}][{now}]\n[{j["post"]}] >> {j["status"]}\n')
          elif j['option'] == '추천영상접속':
            self.progress.emit(f'[{k}번봇][{j["device"]}][{j["proxy"]}][{j["option"]}][{j["channelName"]}][{now}]\n[{j["urls"]}] >> {j["status"]}\n')
          elif j['option'] == '채널검색':
            self.progress.emit(f'[{k}번봇][{j["device"]}][{j["proxy"]}][{j["option"]}][{j["channelName"]}][{now}]\n[{j["post"]}] >> {j["status"]}\n')
          else:
            self.progress.emit(f'[{k}번봇][{j["device"]}][{j["proxy"]}][{j["option"]}][{j["keyword"]}][{now}]\n[{j["post"]}] >> {j["status"]}\n')
          if len(bot) < k:
            bot.append({'success':success,'fail':fail})
          if j['res']:
            bot[k-1]['success'] += 1
          else:
            bot[k-1]['fail'] += 1
          print(k,"번봇 종료")
          k+=1
        for x in range(len(bot)):
          self.progress.emit(f'{x+1}번봇 >> 성공: {bot[x]["success"]}, 실패: {bot[x]["fail"]}')
        print(i+1,"번째종료")
        self.progress.emit("{0:-^98}".format(f'{i+1}번째 종료'))
      self.finished.emit()
    except Exception as e:
      self.progress.emit(f'{e.args}')
      logger.error(e.args)
      self.finished.emit()
    
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow) :
  seo_data = []
  proxy = ""
  def __init__(self) :
    try :
      super().__init__()
      QtWidgets.QMainWindow(self)
      self.setupUi(self)
      self.run_flag = 0
      self.startPause.clicked.connect(self.runClicked)
      self.pushButton.clicked.connect(self.add_search)
      self.pushButton_2.clicked.connect(self.seo_reset)
      self.recommendsearch.stateChanged.connect(self.selectRecommendsearch)
      self.proxycombo.activated.connect(self.add_ip)
      self.pushButton_3.clicked.connect(self.kill_chrome)
      self.keywordinput.setPlaceholderText("입력후 키워드생성 클릭")
      self.keywordinput.returnPressed.connect(self.generate_keyword)
      self.pushButton_4.clicked.connect(self.generate_keyword)
      self.channelinput.setPlaceholderText("입력후 SEO항목 최신화 클릭")
      self.pushButton_5.clicked.connect(self.newSEO)
      self.channelinput.returnPressed.connect(self.newSEO)    
      self.auto_input.stateChanged.connect(self.autonewSEO)  
      self.log.setText("""※실행방법※
검색기능 선택 >> 조회수(숫자)입력 >> PC,M 선택 >> 프록시 선택 >> SEO항목 불러오기(파일 선택) >> ▶클릭
※기능설명※
SEO항목 최신화 : 입력한 채널의 최근영상5개로 SEO항목을 .csv 파일로 저장(키워드는 수동으로 입력 필요)
초기화 : 로그 정리와, SEO항목들 초기화
키워드 생성 : 채널명과 주식종목이름을 조합해서 키워드를 생성
크롬정리 : 크롬드라이브와 크롬프로그램 종료
SEO자동 최신화 : 입력한 채널의 SEO항목을 자동으로 업데이트
""")
    except Exception as e:
      print(e)
      
  def progress_emited(self, text):
    self.log.append(text)
    
  def runClicked(self):
    if self.run_flag == 0:
      self.startPause.setText('■')
      self.run_flag = 1
      self.thread = QThread()
      self.worker = Worker()
      self.worker.moveToThread(self.thread)
      self.thread.started.connect(self.worker.run)
      self.worker.finished.connect(self.thread.quit)
      self.worker.finished.connect(self.worker.deleteLater)
      self.thread.finished.connect(self.thread.deleteLater)
      self.worker.progress.connect(self.progress_emited)
      if self.auto_input.isChecked():
        self.worker.search_opt = []
        if self.youtubesearch.isChecked():
          self.worker.search_opt.append("유튜브검색")
        if self.channelsearch.isChecked():
          self.worker.search_opt.append("채널검색")
        if self.linksearch.isChecked():  
          self.worker.search_opt.append("링크접속")
        if self.recommendsearch.isChecked():
          self.worker.search_opt.append("추천영상접속")
        if self.worker.search_opt == [] :
          self.progress_emited("※검색방법을 체크해주세요※.")
          return
        if self.view.text() == "":
          self.progress_emited("※조회수를 입력해주세요.※")
          return 
        self.worker.view_cnt = int(self.view.text())
        self.worker.auto_seo = self.auto_input.isChecked()
        self.worker.channel = self.channelinput.text()
        self.worker.device_opt = self.devicecombo.currentText()
        self.worker.proxy_opt = self.proxycombo.currentText()
        self.worker.proxy = self.proxy
      else:
        self.worker.seo = self.seo_data
        self.worker.view_cnt = self.view_cnt
        self.worker.auto_seo = ""
      self.thread.start()
      self.thread.finished.connect(
        lambda :  self.progress_emited("\n"+"{0:=^95}".format("프로세스 종료 완료")+"\n")
      )
      self.thread.finished.connect(self.threadFinished)
    else:
      self.worker.quit_process = 1
      self.progress_emited("현재 수행 작업 후 종료 됩니다.")
      
  def threadFinished(self):
    self.run_flag = 0
    self.startPause.setText("▶")
  
  def autonewSEO(self):
    try:
      if self.auto_input.isChecked():
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        if self.recommendsearch.isChecked():
          self.recommendsearch.toggle()
        self.recommendsearch.setEnabled(False)
      else:
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.recommendsearch.setEnabled(True)
    except Exception as e:
      self.progress_emited(f'{e.args}')
      logger.error(e.args)
  
  def newSEO(self):
    try:
      channel = self.channelinput.text()
      if channel == "주식스터디":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCQs5EP_QjBXjOzOkV-ETpog")#주식스터디
        channelLink = "https://www.youtube.com/c/%EC%A3%BC%EC%8B%9D%EC%8A%A4%ED%84%B0%EB%94%94"
      elif channel == "주식전망":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UChnhVGiF3RcMwz0EUNc6ovw")#주식전망
        channelLink = "https://www.youtube.com/c/%EC%A3%BC%EC%8B%9D%EB%A7%88%EC%8A%A4%ED%84%B0"
      elif channel == "주식사는법":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC7Rt-QEDilvmZBuaRh5mV7Q")#주식사는법
        channelLink = "https://www.youtube.com/c/%EC%A3%BC%EC%8B%9D%EC%82%AC%EB%8A%94%EB%B2%95"
      elif self.channel == "치트키":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC7Rt-QEDilvmZBuaRh5mV7Q")#치트키
        channelLink = "https://www.youtube.com/c/%EC%B9%98%ED%8A%B8%ED%82%A4"
      elif channel == "주식상한가":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCnZ2SFE9J6EGXYf3PXd04FQ")#주식상한가
        channelLink = "https://www.youtube.com/channel/UCnZ2SFE9J6EGXYf3PXd04FQ"
      elif channel == "주식LIVE":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCUtKih4a5UkiYlZciXrPwQA")#주식LIVE
        channelLink = "https://www.youtube.com/channel/UCUtKih4a5UkiYlZciXrPwQA"
      elif channel == "세력수급포착":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCCuY9hs95Wl2fTZxMJy5D1w")#세력수급포착 
        channelLink = "https://www.youtube.com/channel/UCCuY9hs95Wl2fTZxMJy5D1w"
      elif channel == "주식테라피":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCw17GTk0hHHS-3BJ10Bp8mQ")#주식테라피
        channelLink = "https://www.youtube.com/channel/UCw17GTk0hHHS-3BJ10Bp8mQ"
      elif self.channel == "주식 리포트TV":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC05pM0iYOUdyOlurcfGkF5g")#주식 리포트TV
        channelLink = "https://www.youtube.com/channel/UC05pM0iYOUdyOlurcfGkF5g"
      elif self.channel == "신분상승":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC7JZwVEnnccvmvalgv3Cshg")#신분상승
        channelLink = "https://www.youtube.com/channel/UC7JZwVEnnccvmvalgv3Cshg"
      elif self.channel == "코인스쿨 : 대한민국 NO.1 코인 채널":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCsXxjI960QybYHYuJeQtvDA")#코인스쿨
        channelLink = "https://www.youtube.com/channel/UCsXxjI960QybYHYuJeQtvDA"
      elif self.channel == "재테크에 반하다♡ : 대한민국 NO.1 재테크 채널":
        parse_rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC7Rt-QEDilvmZBuaRh5mV7Q")#재테크에반하다
        channelLink = "https://www.youtube.com/channel/UC7Rt-QEDilvmZBuaRh5mV7Q"
      else:
        self.progress_emited("※채널명 입력 확인※")
        return
      
      youtube_seo = {'제목':[],'키워드':[],'채널링크':[],'채널이름':[],'영상링크':[]}
      youtube_seo = pd.DataFrame(youtube_seo)
      cnt = 0
      for k in parse_rss.entries:
        if cnt >= 5:
          break
        if "주식스터디 직통번호: 070-4820-2877" in k.summary:
          continue
        summary = k.summary
        start_index = summary.rfind("\n")
        keyword_list = []
        if start_index > 0:
          keyword = list(set(summary[start_index+1:].strip("#").replace(" ","").split("#")))
          for i in range(len(keyword)):
            for j in keyword[i].split(","):
              keyword_list.append(j.strip())
          if len(keyword_list) < 5:
            continue
          data_insert = {'제목':k.title,'키워드':",".join(keyword_list),'채널링크':channelLink,'채널이름':channel, '영상링크':k.link}
          youtube_seo = youtube_seo.append(data_insert, ignore_index=True)
          cnt += 1
          
      
      
      # youtube_seo = {'제목':[],'키워드':[],'채널링크':[],'채널이름':[],'영상링크':[]}
      # youtube_seo = pd.DataFrame(youtube_seo)
      # cnt = 1
      # for i in range(len(parse_rss.entries)):
      #   if "주식스터디 직통번호: 070-4820-2877" in parse_rss.entries[i].summary:
      #     continue
      #   data_insert = {'제목':parse_rss.entries[i].title,'채널링크':channelLink,'채널이름':channel, '영상링크':parse_rss.entries[i].link}
      #   youtube_seo = youtube_seo.append(data_insert, ignore_index=True)
      #   cnt += 1
      #   self.progress_emited(f'{parse_rss.entries[i].title}')
      #   if cnt > 5 :
      #     break
      result = f"SEO_INPUT_{channel}.csv"
      self.progress_emited(f"{result}생성 완료\n{result}의 키워드 항목을 채워주세요")
      youtube_seo.to_csv(result,encoding='utf-8-sig',index=False)
    except Exception as e:
      self.progress_emited(f'{e.args}')
      logger.error(e.args)
      
  def selectRecommendsearch(self):
    if self.recommendsearch.isChecked():
      if self.youtubesearch.isChecked():
        self.youtubesearch.toggle()
      if self.channelsearch.isChecked():
        self.channelsearch.toggle()          
      if self.linksearch.isChecked():
        self.linksearch.toggle()
      if self.auto_input.isChecked():
        self.auto_input.toggle()
      self.youtubesearch.setEnabled(False)
      self.channelsearch.setEnabled(False)
      self.linksearch.setEnabled(False)  
      self.auto_input.setEnabled(False)
    else:
      self.youtubesearch.setEnabled(True)
      self.channelsearch.setEnabled(True)
      self.linksearch.setEnabled(True)
      self.auto_input.setEnabled(True)
  
  def generate_keyword(self):
    try:
      text = self.keywordinput.text()
      channel = text.split("/")[0]
      keyword = text.split("/")[1]
      keywordList = ["주식","주가","주가 전망"]
      text = []
      for i in range(len(keywordList)):
        text.append(keyword+" "+keywordList[i])
      text.append(keyword+" "+channel)
      text.append(channel+" "+keyword)
      text.append(channel)
      text.append(keyword)
      res = ""
      for i in text:
        if i == text[-1]:
          res += i
        else:
          res += i + ","
      self.log.append(res)
    except Exception as e:
      self.progress_emited(f'{e.args}')
      logger.error(e.args)

  def kill_chrome(self):
    import psutil
    i = 0
    j = 0
    try:
      for proc in psutil.process_iter():
        if proc.name() == "chrome.exe":
          proc.kill()
          i+=1
        if proc.name() == "chromedriver.exe":
          proc.kill()
          j+=1
      self.progress_emited(f"크롬{i}개종료완료")
      self.progress_emited(f"크롬드라이버{j}개종료완료")
    except Exception as e:
      self.progress_emited(f'{e.args}')
      logger.error(e.args)
      
  def add_ip(self):
    try:
      proxy_opt = self.proxycombo.currentText()
      if proxy_opt == "IP 리스트 선택":
        fname = QtWidgets.QFileDialog.getOpenFileName(self)
        self.proxy = fname[0]
        if not self.proxy:
          self.proxycombo.setCurrentText("자체 IP 변경")
        else:
          self.progress_emited(f"IP 리스트 선택 완료 >> {fname[0]}")
    except Exception as e:
      self.progress_emited(f'{e.args}')
      logger.error(e.args)
  
  def add_search(self):
    try:
      youtube_search = self.youtubesearch.isChecked()
      channel_search = self.channelsearch.isChecked()
      link_search = self.linksearch.isChecked()
      recommend_search = self.recommendsearch.isChecked()
      device_opt = self.devicecombo.currentText()
      proxy_opt = self.proxycombo.currentText()
      search_opt = []
      if youtube_search:
        search_opt.append("유튜브검색")
      if channel_search:
        search_opt.append("채널검색")
      if link_search:
        search_opt.append("링크접속")
      if recommend_search:
        search_opt.append("추천영상접속")
      if search_opt == []:
        self.progress_emited("※검색방법을 체크해주세요※.")
        return
      if self.view.text() == "":
        self.progress_emited("※조회수를 입력해주세요.※")
        return
      
      fname = QtWidgets.QFileDialog.getOpenFileName(self)
      data = pd.read_csv(fname[0],encoding="utf-8-sig")  
      if len(data) == 0:
        self.progress_emited("※SEO_INPUT.csv 파일을 확인해주세요.※")
        return  
      self.progress_emited(f"SEO항목 가져오기 완료 >> {fname[0]}")
      self.view_cnt = int(self.view.text())
      for i in range(len(data)):
        input_search = f'영상 제목 >> {data.iloc[i]["제목"]}\n키워드 >> {data.iloc[i]["키워드"]}\n채널 이름 >> {data.iloc[i]["채널이름"]}\n채널 링크 >> {data.iloc[i]["채널링크"]}\n영상 링크 >> {data.iloc[i]["영상링크"]}\n조회수 >> {self.view_cnt}\n검색방법 >> {search_opt}\n기기 선택 >> {device_opt}\n프록시 선택 >> {proxy_opt}'
        self.seo_data.append([data.iloc[i]['제목'],data.iloc[i]['키워드'],data.iloc[i]['채널이름'],data.iloc[i]['채널링크'],data.iloc[i]['영상링크'],search_opt,device_opt,proxy_opt,self.proxy])
        self.log.append("{0:-^100}".format(f'{i+1}번 봇'))
        self.log.append(input_search)
        print(self.seo_data)
    except Exception as e:
      self.progress_emited(f'{e.args}')
      logger.error(e.args)
    
  def seo_reset(self):
    self.seo_data = []
    self.log.clear()

if __name__ =="__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  ui = MainWindow()
  ui.show()
  sys.exit(app.exec_())
  
    