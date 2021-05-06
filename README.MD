# Overview 
This is a scraper designed to automatically get your workplace rankings from https://www.stepcount.org.uk/.

# Installation

1. With Python 3.9+ installed, install the requirements.txt modules via pip.

2. Create an `auth.json` file in the main directory  with the following structure
```json 
{
	"username":"email@domain.com",
	"password":"supersafepassword123"
}
```

3. download a client json file from https://console.cloud.google.com/apis/credentials. Your goal is readwrite access to your own spreadsheets. rename the file to `credentials.json` in the main directory.  
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

In order to provide updates to a channel, the slackAnnounce.py script only needs a [valid webhook](https://api.slack.com/messaging/webhooks) for the channel in question. At present the scripts only supprt a single webhook.

![alt text](https://github.com/Ctri-The-Third/StepCount-scraper/blob/main/Slack-sheetsPreview.PNG?raw=true)
![alt text](https://github.com/Ctri-The-Third/StepCount-scraper/blob/main/Slack-messagePreview.PNG?raw=true)


1. Create a JSON file named `slackConfig.json` with the following content
```json
{
	"secretWebhook":"https://hooks.slack.com/services/[ALPHANUMERIC]/[ALPHANUMERIC]/[LONG ALPHANUMERIC]"
}
```

2. configure a scheduler to run the `slackAnnounce.py` script.