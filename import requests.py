import requests
from bs4 import BeautifulSoup
import time
import datetime
import smtplib
import csv
import pandas as pd

URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find(id='productTitle').get_text().strip()
    price = soup.find(id='priceblock_ourprice').get_text().strip()[1:]
    print("Title:", title)
    print("Price:", price)
    today = datetime.date.today()
    header = ['Title', 'Price', 'Date']
    data = [title, price, today]
    with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('AlexTheAnalyst95@gmail.com', 'xxxxxxxxxxxxxx')
    subject = "The Shirt you want is below $15! Now is your chance to buy!"
    body = "Alex, This is the moment we have been waiting for. Now is your chance to pick up the shirt of your dreams. Don't mess it up! Link here: https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3"
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail('AlexTheAnalyst95@gmail.com', 'recipient@example.com', msg)
    server.quit()

def initialize_csv():
    try:
        df = pd.read_csv('AmazonWebScraperDataset.csv')
        print(df)
    except FileNotFoundError:
        with open('AmazonWebScraperDataset.csv', 'w', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Price', 'Date'])

def run_scraper():
    check_price()
    time.sleep(86400)

initialize_csv()
