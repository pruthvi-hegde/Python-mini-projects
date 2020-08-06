import requests
from bs4 import BeautifulSoup
import smtplib

URL = 'https://www.google.com/search?sxsrf=ALeKk02tlMZmrxWsfdA6CZds_1Kr7JCSNw%3A1586600076660&ei=jJiRXtL7J4iRlwSeyKrICQ&q=amazon+stock+price&oq=amazon+stock+price&gs_lcp=CgZwc3ktYWIQAzIMCCMQJxCdAhBGEPoBMgQIABBDMgIIADICCAAyAggAMgIIADIECAAQQzICCAAyAggAMgIIADoECAAQRzoPCCMQsQIQJxCdAhBGEPoBOgQIABAKOggIABAHEAoQHjoGCAAQBxAeOgQIABAeSgoIFxIGMTEtMTQ0SggIGBIEMTEtOFCtGViVPWC4RWgBcAN4AIAB4QSIAcMHkgEFNC41LTGYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwjS8eDvkeDoAhWIyIUKHR6kCpkQ4dUDCAw&uact=5'

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

def check_stock_price():
    page = requests.get(URL,headers=headers)

    soup = BeautifulSoup(page.content,'html.parser')

    amazon_stock_price = soup.find(jsname="vWLAgc").get_text()
    converted_price = float(amazon_stock_price[0:5])
    print(amazon_stock_price.strip())

    if (converted_price > 1.700):
        send_mail()

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('pruhegde@gmail.com','guthsujvuieywmxc')

    subject = 'Price has gone up!'
    body = 'It is a right time to invest in Amazon stock'
    msg = f"Subject:{subject}\n\n{body}"
    server.sendmail(
        'pruhegde@gmail.com',
        'pruhegde@gmail.com',
        msg
    )
    print("Email has been sent!")
    server.quit()


check_stock_price()