# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import time
import datetime
import smtplib
import csv
import pandas as pd

# Define the URL
URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'

# Set headers to avoid being blocked by the website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

# Function to extract title and price
def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract title and price
    title = soup.find(id='productTitle').get_text().strip()
    price = soup.find(id='priceblock_ourprice').get_text().strip()[1:]

    # Print extracted data (for debugging purposes)
    print("Title:", title)
    print("Price:", price)

    # Get today's date
    today = datetime.date.today()

    # Append data to CSV file
    header = ['Title', 'Price', 'Date']
    data = [title, price, today]

    # Write to CSV
    with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# Function to send email alert
def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('AlexTheAnalyst95@gmail.com', 'xxxxxxxxxxxxxx')  # Replace with secure login method

    subject = "The Shirt you want is below $15! Now is your chance to buy!"
    body = "Alex, This is the moment we have been waiting for. Now is your chance to pick up the shirt of your dreams. Don't mess it up! Link here: https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3"
    
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('AlexTheAnalyst95@gmail.com', 'recipient@example.com', msg)  # Replace with recipient email
    server.quit()

# Create or read the CSV file for initial data handling
def initialize_csv():
    try:
        df = pd.read_csv('AmazonWebScraperDataset.csv')
        print(df)
    except FileNotFoundError:
        # If file doesn't exist, create one with the header
        with open('AmazonWebScraperDataset.csv', 'w', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Price', 'Date'])

# Function to run the scraper
def run_scraper():
    check_price()
    time.sleep(86400)  # Wait for 24 hours

# Example usage to initialize CSV and start scraping
initialize_csv()  # Ensure CSV file is ready

# If you want to run the scraper indefinitely (caution with Jupyter)
# This would work in a script but might not work as intended in Jupyter due to infinite loop:
# while True:
#     run_scraper()
