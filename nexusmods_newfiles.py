# Import libraries
import time
import pandas as pd
import requests

# Set the file path where the .csv file is stored
final_sample_path = r"K:\Thesis Data\Sample B\Nexus Mods\nexus_games.csv"

# Set the file path where the .csv files will be stored
output_dir = r"K:\Thesis Data\Sample B\Nexus Mods\nexus_newfiles"

# Set the headers for the GET request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "apikey": "1AH06UrskJXAIckI+vt40EtIe63Xx5oqt2QGmbYm/krP7Vo4lg==--jq05+xlAfp8c6LEu--njhoknhqtxqYzjXRkop6QA=="
}

# Read the .csv file into a pandas dataframe
df = pd.read_csv(final_sample_path)

# Iterate through the rows of the dataframe and make a GET request for each nexus_id
for nexus_id in df["nexus_id"]:
    url = f"https://staticstats.nexusmods.com/site_stats/{nexus_id}.csv"
    output_path = f"{output_dir}/{nexus_id}.csv"

    response = requests.get(url, headers=headers)
    with open(output_path, "wb") as f:
        f.write(response.content)

    # Print the nexus_id of the file that was just saved
    print(f"File saved: {nexus_id}.csv")

    # Wait 1 minute between requests
    time.sleep(1)
