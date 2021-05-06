




from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import logging
import pickle
import re 
import json
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
sheetsConfig = {"sheetID": "", "hourlyRange":"","dailyRange":"","slackRange":""}

def getLatestRow(sheetID,slackRange):
    creds = getToken()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    targetRange = 'Dashboard!B3:I5'
    result = sheet.values().get(spreadsheetId=sheetID,
                                range=slackRange).execute()
    values = result.get('values', [])
    
    return values 

def loadSheetsConfig():
    try:
        fin = json.load(open("sheetsConfig.json","r"))
        sheetsConfig["sheetID"] = fin["sheetID"]
        sheetsConfig["hourlyRange"] = fin["hourlyRange"] if isValidRange(fin["hourlyRange"]) else "" 
        sheetsConfig["dailyRange"] = fin["dailyRange"] if isValidRange(fin["dailyRange"]) else "" 
        sheetsConfig["slackRange"] = fin["slackRange"] if isValidRange(fin["slackRange"]) else "" 
    except Exception as e:
        logging.error("Failed to load sheets config - %s" % (e))
        return 

def RegularUpdate(scoreBoard, sheetID = None, updateRange = None):
    if sheetID is None:
        sheetID = sheetsConfig["sheetID"]
    if updateRange is None:
        updateRange = sheetsConfig["hourlyRange"]


    now = scoreBoard["timestamp"]
    rows = scoreBoard["rows"]
    newObj = []
    for row in rows:
        
        newRow = []
        newRow.append(now)
        
        newRow.append(row["team"])
        newRow.append(row["steps"])
        newObj.append(newRow)
    creds = getToken()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    # Call the Sheets API
    


    result = sheet.values().get(spreadsheetId=sheetID,
                                range=updateRange).execute()
    values = result.get('values', [])

    
    if not values:
        startRow = 1
    else:
        startRow = len(values)+1
    
    newRanges = splitRange(updateRange)
    newRanges = newRanges[0]
    newRange = "'%s'!%s%s:%s%s" % (newRanges[0],newRanges[1],startRow,newRanges[2],startRow+len(rows))
    #newRange = "Raw!A%s:C%s" % (startRow,startRow+len(rows))
    
    body = {"values":newObj}
    
    result = sheet.values().update(spreadsheetId=sheetID,
                                    range=newRange,
                                    valueInputOption="USER_ENTERED", body=body).execute()

def getToken(tokenName = "sheets"):
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  filename = "%s.pickle" % (tokenName)
  print(os.getcwd()+filename)
  if os.path.exists(filename):
      with open(filename, 'rb') as token:
          creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          print ("Needing authorisation for the %s inbox!" % (tokenName))
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open(filename, 'wb') as token:
          pickle.dump(creds, token)
  return creds

def isValidRange(tarRange):
    return re.match(r"[\S\s]*[A-Za-z]+[0-9]*:[A-Za-z]+[0-9]*",tarRange)
    
def splitRange(tarRange):
    return re.findall(r"'*([\S\s]+)'*!([A-Za-z])[0-9]*:([A-Z]+)[0-9]*",tarRange)
    

if __name__ == "__main__":
    import main
    main.hourly()