from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secrets_desk.json',
    scopes=['https://www.googleapis.com/auth/content']
)

credentials=flow.run_local_server(host='localhost',
                      port=8080,
                      authorization_prompt_message='Please visit this URL: {url}', 
                      success_message='The auth flow is complete; you may close this window.',
                      open_browser=True)

print(credentials)