import requests
import json
import os
import time

# Set the API GET request URL
url = "https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/"

# Set the parameters for the API request
params = {
    "key": "152370BE7CC2D6F08E28670C5EBE2B01",
    "query_type": 1,
    "cursor": "*",
    "numperpage": 100,
    "appid": 387990,
    "filetype": 0,
    "return_short_description": True,
    "return_details": True
    }

# Make the API request
response = requests.get(url, params=params)

# Parse the JSON response
json_data = json.loads(response.text)

# Set the file path where the JSON files will be stored
file_path = r"K:\Thesis Data\Sample B\Steam Workshop\Missing json 10-04"

# Check if the file path exists and create it if it does not
if not os.path.exists(file_path):
    os.makedirs(file_path)

# Keep track of the previous next_cursor value
prev_cursor = ""

# Loop through the JSON data and write it to a file with the appid as the name
while True:
    appid = str(params["appid"])
    file_name = os.path.join(file_path, appid + ".json")
    with open(file_name, "a") as f:
        json.dump(json_data, f)
        f.write("\n")

    # Check if there are more results and set the next cursor value for deep pagination
    if "response" in json_data and "next_cursor" in json_data["response"]:
        next_cursor = json_data["response"]["next_cursor"]

        # Break the loop if the same next_cursor value comes back twice
        if next_cursor == prev_cursor:
            break
        else:
            prev_cursor = next_cursor

        params["cursor"] = next_cursor
        response = requests.get(url, params=params)
        json_data = json.loads(response.text)

        # Sleep for 0.1 seconds before making the next API request
        time.sleep(0.1)
    else:
        break
