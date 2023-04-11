# Import libraries
import pandas as pd
import requests
import time

# Read the CSV file into a pandas dataframe
df = pd.read_csv(r'K:\Thesis Data\Steam Workshop\Sample B\steamgames_beforetreatment.csv')

# Create an empty list to store the API responses
api_responses = []

# Iterate through the rows of the dataframe
for index, row in df.iterrows():
    # Extract the App ID value from the 'App ID' column
    app_id = row['appid']

    # Construct the GET request URL with the extracted App ID value
    url = f"https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key=152370BE7CC2D6F08E28670C5EBE2B01&query_type=1&cursor=*&numperpage=10&appid={app_id}&filetype=0&return_short_description=true&return_metadata=&return_details=true"

    # Make the GET request and append the response to the list
    response = requests.get(url).json()
    response['appid'] = app_id
    api_responses.append(response)

    # Wait for 1 second before moving on to the next App ID
    time.sleep(1)

# Create a new dataframe from the list of API responses
query_files_df = pd.DataFrame(api_responses)

# Reorder the columns to have the 'App ID' column first
query_files_df = query_files_df[['appid'] + [col for col in query_files_df.columns if col != 'appid']]

# Write the dataframe to a new CSV file
query_files_df.to_csv('workshop_check.csv', index=False)
