# from https://www.youtube.com/watch?v=79KGri12tgk
import schedule
import time

def job():
    print("Hello!")

schedule.every(10).seconds.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("12:40").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("12:40").do(job)
schedule.every().minute.at(":40").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
