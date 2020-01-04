# Allows us to access a URL and pull out the data from that URL
import requests
# Allows us to parse URL and pull out individual items from URL
from bs4 import BeautifulSoup
# Import Simple Mail Tranfer Protocol Library
import smtplib
# Time module for sleep function
import time

# Set to URL of interest (Note that some sites will block web scraping)
URL = 'https://www.amazon.ca/Sony-Full-Frame-Interchangeable-Digital-28-70mm/dp/B00FRDV06I'

# Gives information about browser
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
           }


def check_price():
    # Returns all data from website
    page = requests.get(URL, headers=headers)
    # Amazon makes HTML code with JS so need to first get the page content then prettify it
    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    # Set title and price from web page
    title = soup2.find(id="productTitle").get_text()
    price = soup2.find(id="priceblock_ourprice").get_text()

    # Convert price to a float for comparison
    converted_price = float(price[5:6]+price[7:-3])

    # Test if converted price and title are returned correctly
    print(converted_price)
    print(title.strip())

    # Condition to send mail
    if(converted_price < 500):
        send_mail()


def send_mail():
    # Establish connection between our connection and gmail so need to set servers
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Extended HELO; A command sent by an email server to identify itself when connecting to another email server to start the process of sending an email
    server.ehlo()
    # Encrypts connection
    server.starttls()
    # Identify again after encryption
    server.ehlo()

    # Log in using your email and password
    server.login('email@gmail.com', 'password')

    # Set subject, body, and message and send the mail
    subject = 'Price is under $500 CAD!'
    body = 'Check the Amazon link: https://www.amazon.ca/Sony-Full-Frame-Interchangeable-Digital-28-70mm/dp/B00FRDV06I'
    msg = f"Subject: {subject}\n\n{body}"     # Format message as string
    server.sendmail(
        'email@gmail.com',
        'email@gmail.com',
        msg
    )

    # Test print if email has been successfully sent
    print('Email has been successfully sent')
    # Close off connection
    server.quit()


# Check price everyday
while(True):
    check_price()
    time.sleep(86400)
