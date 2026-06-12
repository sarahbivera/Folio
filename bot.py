#Pulse - Daily Summary Bot Daily 8AM IST via Github actions
#Fetch: weather wttr.in + quote zenquotes.io

import os
import smtplib
import requests
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Weather
def get_weather(city="Kochi"):
    url=f"https://wttr.in/{city}?format=3"
    try:
        response=requests.get(url,timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Weather Unvailable ({e})"

#quote
def get_quote():
    url="https://zenquotes.io/api/random"
    try:
        response=requests.get(url,timeout=10)
        response.raise_for_status()
        data=response.json()
        quote=data[0]["q"]
        author=data[0]["a"]
        return f'"{quote}" - {author}"'
    except Exception as e:
        return "Quote unavailable ({e})"
    
#Build Summary
def build_summary():
    today=date.today().strftime("%A, %d %B &Y")
    weather=get_weather()
    quote=get_quote()
    summary=f"""
===========================
PULSE - Daily Summary
{today}
===========================
WEATHER
{weather}

Today's Quote
{quote}

===========================
"""
    return summary

# Send Email
def send_email(summary):
    sender = os.environ["SENDER_EMAIL"]
    password = os.environ["APP_PASSWORD"]
    receiver = os.environ["RECEIVER_EMAIL"]

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = " Pulse - Daily Summary"

    message.attach(MIMEText(summary, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(message)

#run
def run():
    summary=build_summary()
    print(summary)
    with open("daily_summary.txt","w",encoding="utf-8") as f:
        f.write(summary)
    send_email(summary)

    print("Pulse ran successfully")


if __name__=="__main__":
    run()
    
