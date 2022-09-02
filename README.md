# Spotify2Youtube-python

## Setup

#### First, create an app on the Spotify Developer dashboard found [here](https://developer.spotify.com/dashboard/applications "here").
Retrieve the Client ID and Client Secret and paste those in the .env file for Spotify OAuth

#### Secondly, enable the Youtube Data API V3 by going to this [link](https://console.cloud.google.com/apis/library/youtube.googleapis.com?project=phrasal-waters-275622 "link")

#### Lastly, go to [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials "Google Cloud Credentials")  and create both a API Key and a OAuth 2.0 Client ID. 
Make sure the OAuth 2.0 Client ID is of type *Desktop* .
Go back to the link mentioned above and click *Download OAuth client* on the right-side of the OAuth Client ID. 
Make sure to download the .json and name it *client_secrets.json* while saving it in the main directory of your cloned local repository (same directory as the main.py, youtubeHandler.py, etc.).
Also paste any more remaining keys, ids, secrets in the .env file (should just be YouTube related). Your YouTube OAuth should now be setup.

#### To execute your code, run main.py
If you have python installed, you can simply execute the command _python main.py_ in console

#### Note: YouTube quota costs restrict the number of API requests with each cost varying by each endpoint. Therefore, you won't be able to convert something like 1000+ songs in one day if you do not have enough quota.

------------

