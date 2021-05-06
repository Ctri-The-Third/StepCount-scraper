




from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1kJaivNZ3NrtIfLcRV8-KjzGSBRsT9v9ThcnY_7H12DY'
SAMPLE_RANGE_NAME = 'Raw!A:A'


def getLatestRow():
    creds = getToken()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    targetRange = 'Dashboard!B3:I5'
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=targetRange).execute()
    values = result.get('values', [])
    
    return values 


def main(scoreBoard):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    now = scoreBoard["timestamp"]
    rows = scoreBoard["rows"]
    newObj = []
    for row in rows:
        
        newRow = []
        newRow.append(now)
        
        newRow.append(row["teamName"])
        newRow.append(row["steps"])
        newObj.append(newRow)
    creds = getToken()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    # Call the Sheets API
    


    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    
    if not values:
        startRow = 1
    else:
        startRow = len(values)+1
    

    newRange = "Raw!A%s:C%s" % (startRow,startRow+len(rows))
    
    body = {"values":newObj}
    
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
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




if __name__ == "__main__":
    getLatestRow()