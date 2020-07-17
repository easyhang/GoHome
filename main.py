import time
import playsound
from bs4 import BeautifulSoup
from selenium import webdriver

error_msgs = ['Oops, something went wrong',
                'Aw snap, no results',
                'Sorry, the itinerary you selected is no longer available']
shenzhen_error_message = "Sorry, the route you inquired dose not have the applicable price."
cdg_pvg = 'https://www.google.com/flights?lite=0&hl=en#flt=CDG.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o'
ams_pvg = 'https://www.google.com/flights?lite=0&hl=en#flt=AMS.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o'
fra_pvg = 'https://www.google.com/flights?lite=0&hl=en#flt=FRA.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o'
zrh_pvg = 'https://www.google.com/flights?lite=0&hl=en#flt=ZRH.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o'
fra_nkg = 'https://www.google.com/flights?lite=0&hl=en#flt=FRA.NKG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o'
dxb_can = 'https://www.google.com/flights?lite=0&hl=en#flt=DXB.CAN.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o'

shenzhen_airline_nrt_szx = 'https://global.shenzhenair.com/zhair/ibe/air/searchResults.do?_catRootMessageId=zh-dev-PRD-0adc2d7e-443034-6081&_catParentMessageId=zh-dev-PRD-0adc2d7e-443034-6081&_catChildMessageId=zh-dev-PRD-0adc2d7e-443034-6092'
def alarm():
    alarm_file = 'alarm.mp3'
    playsound.playsound(alarm_file)

def google_crawler(url, date):
    time.sleep(1)
    driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    true_url = url.format(date)
    driver.get(true_url)
    time.sleep(1) # Let the user actually see something!
    page_html = driver.page_source
    soup = BeautifulSoup(page_html,  features="html.parser")
    tags = soup.findAll('p')

    Noticket = False
    for tag in tags:
        if Noticket:
            break
        text = tag.getText()
        for error_msg in error_msgs:
            if text.find(error_msg):
                print("No ticket!")
                Noticket = True

    if not Noticket:
        print('Ticket found:' + url)
        filename = 'ticket.text'
        f = open(filename, "a")
        f.write(true_url + '\n')
        f.close()
        alarm()

    time.sleep(2) # Let the user actually see something!
    driver.quit()



def all_crawler():
    for i in range (1, 31):
        date = str(i)
        if (i < 10):
            date = '0' + date
        google_crawler(cdg_pvg, date)
        google_crawler(ams_pvg, date)
        google_crawler(fra_pvg, date)
        google_crawler(zrh_pvg, date)
        google_crawler(fra_nkg, date)
        # google_crawler(dxb_can, date)

def main():
    while(True):
        all_crawler()
        time.sleep(600)

if __name__ == "__main__":
    main()