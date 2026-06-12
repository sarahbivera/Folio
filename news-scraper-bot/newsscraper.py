import os
import requests
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

API_KEY = os.environ["NEWS_API_KEY"]

EMAIL = os.environ["SENDER_EMAIL"]
PASSWORD = os.environ["APP_PASSWORD"]
TO_EMAIL = os.environ["RECEIVER_EMAIL"]

url = (
    "https://newsapi.org/v2/top-headlines?"
    "language=en&pageSize=9&apiKey=" + API_KEY
)

response = requests.get(url)
data = response.json()

articles = data.get("articles", [])

html = """
<html>
<body style="font-family:Arial;">
<h2>📰 Daily News Headlines</h2>
<hr>
"""

for article in articles:

    title = article.get("title", "No Title")
    source = article.get("source", {}).get("name", "Unknown")
    published = article.get("publishedAt", "")
    link = article.get("url", "#")

    html += f"""
    <div style="margin-bottom:20px;">
        <h3>{title}</h3>
        <p>
            <b>Source:</b> {source}<br>
            <b>Published:</b> {published}
        </p>
        <a href="{link}">
            Read Article
        </a>
    </div>
    <hr>
    """

html += """
</body>
</html>
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = "Daily News Headlines"
msg["From"] = EMAIL
msg["To"] = TO_EMAIL

msg.attach(MIMEText(html, "html"))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL, PASSWORD)

server.sendmail(
    EMAIL,
    TO_EMAIL,
    msg.as_string()
)

server.quit()

print("Email sent successfully.")