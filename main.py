#!/usr/bin/python3
import requests
import json

session = requests.Session()

def main():
    headers = {}
    headers['Accept'] = 'application/json'
    headers['Accept-Language'] = 'en-US,en;q=0.9'
    headers['Authorization'] = getBearer()
    headers['Connection'] = 'keep-alive'
    headers['Content-Type'] = 'application/json'
    headers['DNT'] = '1'
    headers['Referer'] = 'https://antiochian.org/home'
    headers['sec-ch-ua-mobile'] = '?0'
    headers['sec-ch-ua'] = '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"'
    headers['sec-ch-ua-platform'] = '"Linux"'
    headers['Sec-Fetch-Dest'] = 'empty'
    headers['Sec-Fetch-Mode'] = 'cors'
    headers['Sec-Fetch-Site'] = 'same-origin'
    headers['User-Agent'] = 'OrthoBot'
    #headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' 
    session.headers.update(headers)

    WriteMsg(
        Today(session)
    )

def getBearer():
    # having issues with python requests here...
    # solution: copy form curl :(
    from subprocess import Popen, PIPE 
    command = """curl 'https://antiochian.org/connect/token' \
      -H 'Accept: application/json, text/plain, */*' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      -H 'Connection: keep-alive' \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -H 'DNT: 1' \
      -H 'Origin: https://antiochian.org' \
      -H 'Referer: https://antiochian.org/home' \
      -H 'Sec-Fetch-Dest: empty' \
      -H 'Sec-Fetch-Mode: cors' \
      -H 'Sec-Fetch-Site: same-origin' \
      -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' \
      -H 'sec-ch-ua: "Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'sec-ch-ua-platform: "Linux"' \
      --data-raw 'client_id=antiochian_api&client_secret=TAxhx@9tH(l%5EMgQ9FWE8%7DT@NWUT9U)&grant_type=client_credentials&scope=antiochianapp_api' \
      --compressed"""
    output = json.loads(Popen(command, shell=True, stdout = PIPE, stderr = PIPE).communicate()[0])
    token_type = output['token_type']
    token = output['access_token']
    return token_type+" "+token

def Today(session):
    url =  'https://antiochian.org/api/antiochian/LiturgicalDays/1'
    response = json.loads(session.get(url).content)[0]
    readingsjson = json.loads(session.get('https://antiochian.org/api/antiochian/LiturgicalDay/'+str(response['itemId'])).content)

    calendarDateLong = readingsjson['liturgicalDay']['calendarDateLong'].strip()
    formatCalendarDate = "+++"+"+"*len(calendarDateLong)+"+++\n++ "+calendarDateLong+" ++\n+++"+"+"*len(calendarDateLong)+"+++"

    fastDesignation = readingsjson['liturgicalDay']['fastDesignation'].strip()
    feastDayDescription = readingsjson['liturgicalDay']['feastDayDescription'].strip()
    reading1Title = readingsjson['liturgicalDay']['reading1Title'].strip()
    reading1FullText = CleanText(readingsjson['liturgicalDay']['reading1FullText'])
    reading2Title = readingsjson['liturgicalDay']['reading2Title'].strip()
    reading2FullText = CleanText(readingsjson['liturgicalDay']['reading2FullText'])
    reading3Title = readingsjson['liturgicalDay']['reading3Title'].strip()
    reading3FullText = CleanText(readingsjson['liturgicalDay']['reading3FullText'])
    thought = DailyThought(session)

    msg = f"""{formatCalendarDate}
        \n☦ TODAY'S FAST: {fastDesignation} ☦
        \n☦ TODAY'S FEASTS ☦ \n{feastDayDescription}
        \n☦ TODAY'S THOUGHT ☦ \n{thought}
        \n\n☦ READING 1: {reading1Title} ☦
        \n{reading1FullText}
        \n\n☦ READING 2: {reading2Title} ☦
        \n{reading2FullText}\n"""

    if reading3Title != "":
        msg = msg+f"""
            \n☦ READING 3: {reading3Title} ☦
            \n{reading3FullText}\n\n"""

    return msg

def DailyThought(session):
    url =  'https://antiochian.org/api/antiochian/ThoughtForTheDay'
    return CleanText(json.loads(session.get(url).content)['description'])

def CleanText(text):
    return text.strip().replace("&quot;","\"").replace("&#39;","\'").replace("&#58;",":")

def WriteMsg(msg):
    print(msg)

main()
