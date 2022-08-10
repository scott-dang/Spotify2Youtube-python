# Spotify2Youtube-python

## Setup

#### First, create an app on the Spotify Developer dashboard found [here](https://developer.spotify.com/dashboard/applications "here").
Retrieve the Client ID and Client Secret and paste those in the .env file for Spotify OAuth

#### Secondly, go to [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials "Google Cloud Credentials")  and create both a API Key and a OAuth 2.0 Client ID. 
Make sure the OAuth 2.0 Client ID is of type *Desktop* .
Go back to the link mentioned above and click *Download OAuth client* on the right-side of the OAuth Client ID. 
Make sure to download the .json and name it *client_secrets.json* while saving it in the main directory of your cloned local repository (same directory as the main.py, youtubeHandler.py, etc.).
Also paste any more remaining keys, ids, secrets in the .env file (should just be YouTube related). Your YouTube OAuth should now be setup.

#### To execute your code, run main.py
------------

