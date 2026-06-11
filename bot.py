#Pulse - Daily Summary Bot Daily 8AM IST via Github actions
#Fetch: weather wttr.in + quote zenquotes.io

import requests
from datetime import date

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

#run
def run():
    summary=build_summary()
    print(summary)
    with open("daily_summary.txt","w",encoding="utf-8") as f:
        f.write(summary)

    print("Pulse ran successfully")


if __name__=="__main__":
    run()
    
