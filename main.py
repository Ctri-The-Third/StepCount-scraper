import requests
import json
import re
import sheetspart
import datetime
from bs4 import BeautifulSoup



 
def getLogin(username,password):
    
    url = "https://www.stepcount.org.uk/login"
    data = {
        "lemail":username,
        "lpw":password,
        "submit":"Log in",
        "gogoin":"yeh"
    }
    r = session.post(url=url, data=data)
    
    print(session.cookies.get_dict())


def getLeaderBoard():
    url = "https://www.stepcount.org.uk/my-leaderboard?mywork"

    r = session.get(url)
    print(r)
    print(len(r.content))
    content = r.content.decode('UTF-8')
    leaderBoard = []
    soup = BeautifulSoup(content,'html.parser')

    lbl = soup.find_all(name='div',class_=re.compile("lead_bd(?![0-9])"))
    for tag in lbl:
        entry = BeautifulSoup(str(tag),'html.parser')
        

        rawName = entry.find(name="span", class_="lb_name").text
        if rawName[-16:] == "Unity | Game Ops":
            rawName = rawName[0:-16]
            rawName = re.sub(r" \([0-9]*.{2}\)","",rawName)

        rawSteps = entry.find(name="div", class_="lead_bd3").text
        if rawSteps[-6:] == " Steps":
            
            rawSteps = re.sub(r"[^0-9]","",rawSteps)
            int(rawSteps)
        

        leaderBoardEntry = {"team":rawName,"steps":rawSteps}
        print(leaderBoardEntry)
        leaderBoard.append(leaderBoardEntry)
        #lb_name
        #lead_bd3
    leaderBoard = {"timestamp" : datetime.datetime.now().strftime(r"%y-%m-%d %H:%M"), "rows":leaderBoard}
    return leaderBoard    


try:
    j = json.load(open("auth.json","r"))
    if "username" not in j or "password" not in j:
        raise Exception("could not load username and password")
except Exception as e:
    j = {"username":"", "password":""}


session = requests.Session()
def hourly():
    getLogin(j["username"],j["password"])
    leaderBoard = getLeaderBoard()
    sheetspart.loadSheetsConfig()
    sheetspart.RegularUpdate(leaderBoard)

def daily():
    getLogin(j["username"],j["password"])
    leaderBoard = getLeaderBoard()
    sheetspart.loadSheetsConfig()
    sheetspart.RegularUpdate(leaderBoard,updateRange=sheetspart.sheetsConfig["dailyRange"])
    
    
