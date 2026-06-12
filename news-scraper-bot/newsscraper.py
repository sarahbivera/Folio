import os
import feedparser
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


EMAIL = os.environ["SENDER_EMAIL"]
PASSWORD = os.environ["APP_PASSWORD"]
TO_EMAIL = os.environ["RECEIVER_EMAIL"]


feeds = {
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
    "The Hindu": "https://www.thehindu.com/news/feeder/default.rss",
    "CNN": "http://rss.cnn.com/rss/edition.rss"
}

html = """
<html>
<head>
<style>
body{
    font-family:Arial;
    background:#f4f4f4;
    padding:20px;
}
.container{
    background:white;
    padding:20px;
    border-radius:10px;
}
h1{
    color:#222;
}
h2{
    color:#0b5ed7;
}
.article{
    margin-bottom:15px;
}
.time{
    color:gray;
    font-size:13px;
}
</style>
</head>

<body>
<div class="container">
<h1>📰 Daily News Headlines</h1>
"""

for source, url in feeds.items():

    feed = feedparser.parse(url)

    html += f"<h2>{source}</h2>"

    for article in feed.entries[:3]:

        title = article.get("title", "No Title")
        link = article.get("link", "#")
        published = article.get("published", "Publication time unavailable")

        html += f"""
        <div class="article">
            <b>{title}</b><br>
            <span class="time">{published}</span><br>
            <a href="{link}">{link}</a>
        </div>
        """

html += """
</div>
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

print("Email sent successfully!")