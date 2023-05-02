# Overview 
This is a scraper designed to automatically get your workplace rankings from https://www.stepcount.org.uk/.

# Installation

1. With Python 3.9+ installed, install the requirements.txt modules via pip.

2. Create an `auth.json` file in the main directory  with the following structure
```json 
{
	"username":"email@domain.com",
	"password":"supersafepassword123",
}
```

3. download a client json file from https://console.cloud.google.com/apis/credentials. Your goal is readwrite access to your own spreadsheets. rename the file to `credentials.json` in the main directory.  You'll need to have enabled the Google Sheets API for the project you're using.
It should look like this:
```json
{
  "installed": {
    "client_id": "big-longUniqueString.apps.googleusercontent.com",
    "project_id": "name-numericsuffix",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "~20 mixed characters and numbers"
  }
}
```


4. Configure a scheduler to run the `runmeHourly.py` and `runmeDaily.py` files
# Slack

In order to provide updates to a channel, the slackAnnounce.py script requires a token with `chat:write`, and for the created app to be added to a given channel.

![preview of the sheets layout](https://raw.githubusercontent.com/Ctri-The-Third/StepCount-scraper/main/ReadmeAssets/Slack-sheetsPreview.PNG)

![preview of the slack message](https://raw.githubusercontent.com/Ctri-The-Third/StepCount-scraper/main/ReadmeAssets/Slack-messagePreview.PNG)

Ensure the slack token and slack channel identifier are added to the auth.json. The final thing will look like the following:

```json
{
  "username":"email@domain.com",
  "password":"supersafepassword123",
  "slacktoken":"xoxb-1234567890-1234567890-aLpHaNuMeRiC",
  "slackchannel": "C0ALPHANUMERIC"
}
```

2. configure a scheduler to run the `runmeDaily.py` script, which includes attempting to announce to slack.

