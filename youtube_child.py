# Child process to uplaod a file to youtube
# Input: token via stdin, and file information via command line args
# Output: URL to get token via stdout

import sys
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

import errors

# Youtube initialization vars
scopes = ["https://www.googleapis.com/auth/youtube.upload"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "./api_keys/client_secret_760766942734-7b92qqmu8p6dpeb7hhfqb15batdp1sba.apps.googleusercontent.com.json"

def upload(filepath, subreddit, title):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    print(f"{title} (r/{subreddit})")

    # Call youtube api to upload video
    request = youtube.videos().insert(
        # Use snippet part to add title and description
        part="snippet",
        body={
          "snippet": {
            "title": f"{title} (r/{subreddit}) #shorts",
            "description": f"Hope you enjoyed the best of r/{subreddit}!"
          }
        },

        # File to upload
        media_body=MediaFileUpload(filepath)
    )

    # Submit request    
    response = request.execute()

if not len(sys.argv) == 4: print("TO FEW ARGS")
else:
    upload(sys.argv[1], sys.argv[2], sys.argv[3])