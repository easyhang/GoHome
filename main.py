import time
from datetime import datetime
import playsound
import smtplib, ssl
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

error_msgs = [
    'Oops, something went wrong',
    'Aw snap, no results',
    'Sorry, the itinerary you selected is no longer available'
]

no_price_msgs = ['Prices are not available for: ',
                 'Flights with unavailable prices are at the end of the list.'
]

has_price_msg = 'Total price includes taxes + fees for 1 adult.'

flights = [
    'https://www.google.com/flights?lite=0&hl=en#flt=SEA.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=DTW.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=LAX.PEK.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=LAX.CAN.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=LAX.XMN.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=CDG.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=CDG.PEK.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=CDG.CAN.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=AMS.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=AMS.CAN.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=AMS.XMN.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=FRA.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=ZRH.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=FRA.NKG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=DXB.CAN.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=NRT.DLC.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=NRT.SHE.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=NRT.FOC.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=NRT.SZX.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=NRT.HRB.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=BRU.PEK.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=YVR.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=ICN.NKG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=ICN.TAO.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=ICN.PEK.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=ICN.CGQ.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=ICN.SHE.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=ICN.PVG.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=ICN.SZX.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=ICN.CAN.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=ICN.XMN.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o',
    'https://www.google.com/flights?lite=0&hl=en#flt=DOH.CAN.2020-08-{};c:USD;e:1;s:0;sd:1;t:f;tt:o'
]


mail_body = 'Check ticket!\n\n' \
            '{}\n\n' \
            'This message is sent from python.\n' \

def alarm():
    alarm_file = 'alarm.mp3'
    playsound.playsound(alarm_file)

def google_crawler(url, date, driver):
    true_url = url.format(date)
    driver.get(true_url)
    time.sleep(0.5) # Let the user actually see something!
    page_html = driver.page_source
    soup = BeautifulSoup(page_html,  features="html.parser")
    tags = soup.findAll('p')

    no_ticket = False
    for tag in tags:
        if no_ticket:
            break
        text = tag.getText()
        for error_msg in error_msgs:
            if text == error_msg:
                print(datetime.fromtimestamp(time.time()), " 08-" + date +": No ticket!")
                no_ticket = True

    if not no_ticket:
        if validate(soup):
            alarm() # alarm might be noisy, comment out if you don't want it.
            print(datetime.fromtimestamp(time.time()), 'Ticket found:' + true_url)
            filename = 'ticket.text'
            f = open(filename, "a")
            text = str(datetime.fromtimestamp(time.time())) + ' ' + true_url + '\n'
            f.write(text)
            f.close()
            send_email(mail_body.format(true_url))
        else:
            print('No price, possibly false ticket: ' + true_url)

    time.sleep(0.5) # Let the user actually see something!

def validate(soup):
    res = soup.find("div", {"class": "flt-subhead1 gws-flights-results__price gws-flights-results__cheapest-price"})
    if res is None:
        return False
    else:
        price_string = res.text
        price = ''
        digits = re.findall(r'\d+', price_string)
        for digit in digits:
            price += digit
        print('price: $', price)

        if int(price) > 4500:
            print('Price too high. Ignore')
            return False
        return True

def send_email(text):
    port = 465  # For SSL
    '''
    use your own email below.
    '''
    password = 'xxxx'
    sender_email = 'xxx'
    receiver_email = 'xxx'

    message = MIMEMultipart("alternative")
    message["Subject"] = "Ticket available!"
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(text, "plain"))

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        print('Sending email to ', receiver_email)
        server.sendmail(sender_email, receiver_email, message.as_string())


def all_crawler():
    driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    for i in range (1, 32):
        date = str(i)
        if (i < 10):
            date = '0' + date
        for flight in flights:
            google_crawler(flight, date, driver)

    driver.quit()

def main():
    while(True):
        all_crawler()
        time.sleep(600)

if __name__ == "__main__":
    main()