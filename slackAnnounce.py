import requests 
import json
import sheetspart
from serviceHelpers.slack import slack
import openai



def prepareMessage (sheetID,slackRange):
    values = sheetspart.getLatestRow(sheetID,slackRange)
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

def add_motivation(message:str, open_ai_token:str) -> str:
    "feeds the current slack table into open and gets a short motivation & celebration for the winning / losing teams"

    openai.api_key = open_ai_token
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role":"user",
             "content":f"{message} \n\n The above is being posted to a company step challenge. Without repeating the rankings or step counts, give a short consolidated celebration paragraph for the top 3, and an encouraging note for the team that increased by the least"
            }],
        temperature=0.7,
        max_tokens=150,
        frequency_penalty=0.5,
        presence_penalty=0,
        top_p=1.0
    )
    response_content = response["choices"][0]["message"]["content"]
    return f"{message}\n\n{response_content}"