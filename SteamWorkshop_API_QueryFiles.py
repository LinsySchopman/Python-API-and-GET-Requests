import requests
import json
import os
import time

# Set the API GET request URL
url = "https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/"

# Set the default parameters for the API request
default_params = {
    "key": "152370BE7CC2D6F08E28670C5EBE2B01",
    "query_type": 1,
    "cursor": "*",
    "numperpage": 100,
    "filetype": 0,
    "return_short_description": True,
    "return_details": True
    }

# Set the file path where the CSV files are stored
csv_file_path = r"H:\Thesis Data\Sample B\Steam Workshop\csv files for appid"

# Set the file path where the JSON files will be stored
json_file_path = r"H:\Thesis Data\Sample B\Steam Workshop\Json"

# Check if the JSON file path exists and create it if it does not
if not os.path.exists(json_file_path):
    os.makedirs(json_file_path)

# Loop through each CSV file in the folder
for csv_file in os.listdir(csv_file_path):
    # Get the appid from the CSV file name
    appid = os.path.splitext(csv_file)[0]

    # Set the appid parameter for the API request
    params = default_params.copy()
    params["appid"] = int(appid)

    try:
        # Make the API request
        response = requests.get(url, params=params)

        # Raise an exception if the response status code is not 200 OK
        response.raise_for_status()

        # Parse the JSON response
        json_data = json.loads(response.text)

        # Set the file path and name for the JSON file
        json_file_name = os.path.join(json_file_path, appid + ".json")

        # Check if the JSON file already exists and delete it if it does
        if os.path.exists(json_file_name):
            os.remove(json_file_name)

        # Loop through the JSON data and write it to the file
        while True:
            with open(json_file_name, "a") as f:
                json.dump(json_data, f)
                f.write("\n")

            # Check if there are more results and set the next cursor value for deep pagination
            if "response" in json_data and "next_cursor" in json_data["response"]:
                next_cursor = json_data["response"]["next_cursor"]

                # Break the loop if the same next_cursor value comes back twice
                if next_cursor == params["cursor"]:
                    break

                params["cursor"] = next_cursor
                response = requests.get(url, params=params)

                # Raise an exception if the response status code is not 200 OK
                response.raise_for_status()

                json_data = json.loads(response.text)

                # Sleep for 0.5 seconds before making the next API request
                time.sleep(0.2)
            else:
                break

    except Exception as e:
        # Print an error message if there was an issue with the API request
        print(f"Error processing appid {appid}: {str(e)}")
