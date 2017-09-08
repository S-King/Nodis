# Create a Credentials object from the service account's credentials and the scopes your application needs access to. For example:
from oauth2client.service_account import ServiceAccountCredentials
print("JERE")
scopes = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('NodisApp-Secrets.json', scopes=scopes)
print("JERasdE")

# Use the authorized Http object to call Google APIs by completing the following steps:
# Build a service object for the API that you want to call. 
from httplib2 import Http

http_auth = credentials.authorize(Http())
print("JER231321E")
# You build a a service object by calling the build function with the name 
# and version of the API and the authorized Http object. 
# For example, to call version 1beta3 of the Cloud SQL Administration API:
from apiclient.discovery import build

drive = build('drive', 'v3', http=http_auth)
print("J999999E")
# Make requests to the API service using the interface provided by the service object. 
# For example, to list the instances of Cloud SQL databases in the exciting-example-123 project:

FILES = (('TextFile1.txt', None),)
print("JERa31sd2a13sd21E")
for filename, mimeType in FILES:
    metadata = {'name' : filename}
    if mimeType:
        metadata['mimeType'] = mimeType


print("here")
x = drive.files().create(body=metadata,
                                    media_body=filename,
                                    fields='id').execute()
print("x>> {}".format(x))


metadata = {'emailAddress' : 'nodisapi@gmail.com', 'type' : 'user', 'role' : 'reader'}
y = drive.permissions().create(body=metadata, fileId="0B-8FV19O5EIlZkNwRE9UX2JYdzA").execute()
print("y>> {}".format(y))


results = drive.files().list(
    pageSize=10,fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['id']))