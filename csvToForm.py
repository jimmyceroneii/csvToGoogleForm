from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import argparse
from parseCsv import parse_csv
from formatForGoogleFormApi import formatForGoogleFormApi

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
    
title = input("Enter the title: ")

store = file.Storage("token.json")
creds = None
if not creds or creds.invalid:
  flow = client.flow_from_clientsecrets("client_secrets.json", SCOPES)
  creds = tools.run_flow(flow, store)

form_service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

# Request body for creating a form
NEW_FORM = {
    "info": {
        "title": title,
    }
}

# Creates the initial form
result = form_service.forms().create(body=NEW_FORM).execute()

# Request body to add a multiple-choice question
csv = parse_csv('test.csv')

questions = formatForGoogleFormApi(csv)

body = { "requests": questions }

# Adds the question to the form
question_setting = (
    form_service.forms()
    .batchUpdate(formId=result["formId"], body=body)
    .execute()
)

# Prints the result to show the question has been added
get_result = form_service.forms().get(formId=result["formId"]).execute()
print(get_result)