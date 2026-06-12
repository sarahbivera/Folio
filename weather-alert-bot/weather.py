import os
import requests
import smtplib
from email.mime.text import MIMEText

# ==========================
# CONFIGURATION
# ==========================

API_KEY = os.getenv("API_KEY")
print(API_KEY)

CITY = "Kochi"
COUNTRY = "IN"

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

TEMP_THRESHOLD = 35      # Celsius
RAIN_THRESHOLD = 50      # Percent chance

# ==========================
# FETCH WEATHER DATA
# ==========================

url = (
    f"https://api.openweathermap.org/data/2.5/forecast"
    f"?q={CITY},{COUNTRY}"
    f"&appid={API_KEY}"
    f"&units=metric"
)

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print(f"Failed to fetch weather data: {e}")
    exit()

if data.get("cod") != "200":
    print("API returned an error:")
    print(data)
    exit()

# First forecast = next 3-hour period
forecast = data["list"][0]

temperature = forecast["main"]["temp"]
rain_probability = forecast.get("pop", 0) * 100

# ==========================
# CHECK CONDITIONS
# ==========================

alerts = []

if temperature > TEMP_THRESHOLD:
    alerts.append(
        f" High Temperature Alert\n"
        f"Temperature: {temperature:.1f}°C"
    )

if rain_probability >= RAIN_THRESHOLD:
    alerts.append(
        f"🌧 Rain Alert\n"
        f"Chance of rain in the next 3 hours: {rain_probability:.0f}%"
    )

if not alerts:
    print("No alert conditions met.")
    print(f"Temperature: {temperature:.1f}°C")
    print(f"Rain chance: {rain_probability:.0f}%")
    exit()

# ==========================
# SEND EMAIL
# ==========================

body = "\n\n".join(alerts)

message = MIMEText(body)
message["Subject"] = "Weather Alert"
message["From"] = SENDER_EMAIL
message["To"] = RECEIVER_EMAIL

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(message)

    server.quit()

    print("Weather alert email sent successfully!")

except Exception as e:
    print("Failed to send email:")
    print(e)
