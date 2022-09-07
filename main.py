
from stock_crawl import crawl
from naver_post import naverPost
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from get_stocks import calendar
from tistory_post import tistoryPost
import time

def get_today_days(time):
  days = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
  day = time.tm_wday
  return days[day]

def job(input_dict, input_day_of_week):
  try:
    print("프로세스 시작")
    stocks_name = calendar.get_calendar()
    print(stocks_name)
    time.sleep(1)
    for i in stocks_name:
      try:
        print(f"{i} 크롤링 시작")
        if crawl().get_stock(i):
          print(f"{i} 크롤링 완료")
          time.sleep(1)
          print(f"{i} 티스토리 포스팅 시작")
          for j in input_dict['Turl']:
            if tistoryPost(input_dict['Tid'], input_dict['Tpw'], j).do_post(i):
              print(f"{i} 티스토리 포스팅 완료")
            else:
              print(f"{i} 티스토리 포스팅 실패")
            time.sleep(1)
          if get_today_days(time.localtime()) == input_day_of_week:
            print(f"{i} 카페 포스팅 시작")
            if naverPost(input_dict['Nid'], input_dict['Npw'], input_dict['Nurl'], input_dict['proxy']).do_post(i):
              print(f"{i} 카페 포스팅 완료")
            else:
              print(f"{i} 카페 포스팅 실패")
        else:
          print(f"{i} 크롤링 실패")
      except KeyboardInterrupt:
        break
      except Exception as e:
        print(e)
      time.sleep(60 * int(input_dict['term']))
    print("프로세스 종료")
  except Exception as e:
    print(e)
    print("오류 발생")

def main():
  try:
    print("""
   ___              _  _     _____  _               _        
  |_  |            (_)| |   /  ___|| |             | |       
    | | _   _  ___  _ | | __\ `--. | |_  _   _   __| | _   _ 
    | || | | |/ __|| || |/ / `--. \| __|| | | | / _` || | | |
/\__/ /| |_| |\__ \| ||   < /\__/ /| |_ | |_| || (_| || |_| |
\____/  \__,_||___/|_||_|\_\\____/  \__| \__,_| \__,_| \__, |
                                                        __/ |
                                                       |___/        
""")
    sched = BackgroundScheduler(timezone='Asia/Seoul')
    sched.start()
    print("""
※네이버 공모주리포트 사용법※

카페 포스팅은 일주일에 한번씩 입력한 시간에 이루어집니다.
티스토리 포스팅은 하루에 한번씩 입력한 시간에 이루어집니다.
겹칠경우 티스토리 포스팅 이후 카페 포스팅이 이루어집니다.

""")
    input_day_of_week = input("요일을 입력해주세요 ex) 월요일 : ")
    input_time = input("시각을 입력해주세요 ex) 08:00 : ")
    input_term = input("포스팅 간격(분)을 입력해주세요 ex) 60 : ")
    input_hour = input_time.split(":")[0]
    input_minute = input_time.split(":")[1]
    input_Nid = input("네이버 ID를 입력해주세요 : ")
    input_Npw = input("네이버 PW를 입력해주세요 : ")
    input_Nurl = input("네이버 URL을 입력해주세요 : ")  
    input_Nproxy = input("네이버 prxoy리스트 텍스트의 파일명을 확장자 빼고 입력해주세요 (없으면 엔터 입력) : ")
    input_Tid = input("티스토리 ID를 입력해주세요 : ")
    input_Tpw = input("티스토리 PW를 입력해주세요 : ")
    input_Turl = input("티스토리 URL을 입력해주세요 : ")  
    Nid = "moneym0814"
    Npw = "ajsl12qw!@1"
    Nurl = "https://cafe.naver.com/ca-fe/cafes/29470508/menus/229/articles/write?boardType=L"
    Tid = "moneymachine.vip@gmail.com"
    Tpw = "money1366"
    Turl = ["stockstudy-ipo"]
    input_dict = {'Nid':Nid,'Npw':Npw,'Nurl':Nurl,'Tid':Tid,'Tpw':Tpw,'Turl':Turl,'proxy':input_Nproxy, 'term':input_term}
    print(f"카페 포스팅은 매주 {input_day_of_week} {input_hour}시{input_minute}분 에 {input_Nid} / {input_Npw} 로 {input_Nurl} 에  {input_Nproxy}.txt 사용해 포스팅 진행합니다.")
    print(f"티스토리 포스팅은 매일 {input_hour}시{input_minute}분 에 {input_Tid} / {input_Tpw} 로 {input_Turl} 에 포스팅 진행합니다.")
    try:
      sched.add_job(job, 'cron', hour=input_hour, minute = input_minute, id='ipoPost',args = [input_dict, input_day_of_week], misfire_grace_time = 600)
    except:
      try:
        print("기존 Job 제거 후 새로 추가")
        sched.remove_all_jobs()
        sched.add_job(job, 'cron', hour=input_hour, minute = input_minute, id='ipoPost',args = [input_dict, input_day_of_week], misfire_grace_time = 600)
      except JobLookupError as e:
        print("Scheduler 오류 발생", e)
        return
    while True:
      try:
        print("Running main process............","| [time] ", str(time.localtime().tm_hour)+":"+str(time.localtime().tm_min)+":"+str(time.localtime().tm_sec))
        time.sleep(600)  
      except KeyboardInterrupt:
        import sys
        print("Ctrl + C 중지, Job 제거 후 프로그램 종료")
        sched.remove_all_jobs()
        sys.exit()
  except KeyboardInterrupt:
    print("Ctrl + C 중지")

if __name__ == "__main__":
  main()


  
  