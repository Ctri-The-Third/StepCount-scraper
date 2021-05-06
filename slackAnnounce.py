import requests 
import json
import sheetspart

def postToSlack (text):


    url = getWebhook()
    headers = {"Content-type":"application/json"}
    body = {"text":text}
    r = requests.post(url = url, headers = headers,data=json.dumps(body))
    print(r)
    print(r.content)

def getWebhook():
    try:
        conf = json.load(open("slackConfig.json"))
        return conf["secretWebhook"]
    except Exception as e:
        return "" 



def prepareMessage ():
    values = sheetspart.getLatestRow()
    names = values[0]
    growth = values[1]
    totals = values[2]
    teams = []
    for i in range(len(names)):
        team = {"name":names[i],
                "growth":int(growth[i]),
                "total":int(totals[i])
                }
        teams.append(team)
    
    teams = sortTeams(teams)
    print (teams)

    message = """ *Yesterday's contributions* (as of 23:30 UTC+1)

"""
    for team in teams:
        message = "%s+%s (%s)\t`%s`\n" % (message,format(team["growth"],","),format(team["total"],","),team["name"])
    return message
    
def sortTeams(teams):
    changed = True
    while changed:
        changed = False
        for i in range (len(teams)):
            try: 
                oldTeam = teams[i]
                newTeam = teams[i+1]
                if oldTeam["total"] < newTeam["total"]:
                    #if the total score is lower, swap.
                    oldTeam = teams[i]
                    newTeam = teams[i+1]
                    teams[i] = newTeam
                    teams[i+1] = oldTeam
                    changed = True
            except Exception as e:
                pass
    return teams

if __name__ == "__main__":
    message = prepareMessage()
    postToSlack(message)
