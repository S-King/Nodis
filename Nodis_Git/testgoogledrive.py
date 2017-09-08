import os
import gflags
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools 


SCOPES = 'https://www.googleapis.com/auth/drive.file'      # Permissions requested, space delimited string
CLIENT_SECRET = 'client_secrets.json'

API_KEY = 'AIzaSyDuAA_zAb4HPwIz3QLqbLEaKXOzV3AFVGw'  # DONT PUT INTO PROD!!
#SERVICE = build(API, VERSION, developerKey=API_KEY)

try:
    import argparse
    flags = tools.argparser.parse_args([])
    print(flags)

except ImportError:
    flags = None
    print("HERE!")
    print(ImportError)

store = file.Storage('storage.json')
credz = store.get()
print("1")
if not credz or credz.invalid:
    #flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    # Try 2
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope=SCOPES,
        # redirect_uri='http://www.example.com/oauth2callback'
        redirect_uri='http:/localhost:8080/oauth2callback'
        )
    flow.params['access_type'] = 'online'         # offline access
    flow.params['include_granted_scopes'] = 'true'   # incremental auth    

    print("ddd")
    auth_uri = flow.step1_get_authorize_url()
   
    print(auth_uri)
    credz = tools.run_flow(flow, store, flags) # if flags else tools.run(flow, store)
    credentials = flow.step2_exchange(credz)
    print(credz)

print("2")
DRIVE = build('drive', 'v3', Http=credz.authorize(Http()))

FILES = (
    ('hello.txt', None)
    )

print("3")
for filename, mimeType in FILES:
    metadata = {'name': filename}
    if mimeType:
        metadata['mimeType'] = mimeType
    res = DRIVE.files().create(body=metadata, media_body=filename).execute()
    if res:
        print('Uploaded "{}" -- {}'.format(filename, res['mimeType']))



if res:
    MIMETYPE = 'application/pdf'
    data = DRIVE.files().export(fileId=res['id'], mimeType=MIMETYPE).execute()
    if data:
        fn = '%s.pdf' % os.path.splitext(filename)[0]
        with open(fn, 'wb') as fh:
            fh.write(data)
        print('Downloaded {} -- {} '.format(fn, MIMETYPE))



# SERVICE = build(API, VERSION, Http=credz.authorize(Http()) # Basic stuff needed to make google api requests
