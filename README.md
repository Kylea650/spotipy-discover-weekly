# spotipy-discover-weekly

A simple python script to archive the user's current Discover Weekly playlist as a new spotify playlist on their account.

This script is set up to run weekly (every Monday at 6am UTC) using GitHub Actions.

## To run locally:
This project uses Python 3.10 and Spotipy 2.20.0 as per the requirements.txt.

Clone the repo and run the following from your terminal to create a virtual environment for the project and install the required dependencies.

bash/zsh
```
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
powershell
```
python3.10 -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Update the fields within the config/example_credentials.py with your own information and update the import in discover_weekly.py accordingly.

CLIENT_ID and CLIENT_SECRET:
You will require a Spotify account, and your CLIENT_ID and CLIENT_SECRET can be generated by registering a new app with Spotify at the following [link](https://developer.spotify.com/dashboard/applications).

USER_ID
This is your Spotify username which can be found in your account settings.

PLAYLIST_ID
This is the playlist URI for your Discover Weekly playlist. Open your playlist on Spotify Web, click the three dots and then 'Share'. Holding CTL or ALT will give you the option of copying the URI link. 

REFRESH_TOKEN
Once you run the script once locally, you will be re-directed to your browser and required to authorise. Once complete, a .cache file will appear in your root folder containing the value of your refresh token. Copy this value (REFRESH_TOKEN value only) into your credentials.py file. This will allow your application to run without the need for you to authorise in the future.

## To run with GitHub Actions:
The GitHub Actions YAML file will take care of setting up and running the script automatically. You will first however need to add your secret IDs to your GitHub account. This can be done via Settings > Secrets > Actions. Ensure these values do not contain any additional spaces and do not contain quotation marks.
