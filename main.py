from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# print(client_id, client_secret)

# authorization and authentication methods differ depending on the API used
# give access to the authorization/access token for Spotify API
def get_token():
    # modify authorization token
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,

        # how can I know what's the content type:
        # check the docs, it says to set to below
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    if result.status_code != 200:
        print("Error: Failed to get a valid response from the server")
        print("Status Code:", result.status_code)
        print("Response Content:", result.content)
    else:
        # convert result.content from json to a python dictionary
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists ...")
        return None
    return json_result[0]


token = get_token()
result = search_for_artist(token, "ACDC")
print(result["name"])
# the token is what's used in headers when we send requests to API