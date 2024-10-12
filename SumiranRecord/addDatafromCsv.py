import pandas as pd
from datetime import datetime
import json

def csv_to_json(csv_file_path, user_id, name, username, json_file_path):
    # Load the CSV data
    df = pd.read_csv(csv_file_path)
    
    # Initialize the JSON structure
    data = {
        "_id": user_id,
        "name": name,
        "username": username,
        "records": [],
        "started_on": "",
        "updated_on": ""
    }
    
    # Track the earliest and latest dates for started_on and updated_on
    earliest_date = None
    latest_date = None
    
    # Process each row in the DataFrame
    for index, row in df.iterrows():
        record_id = f"record{index + 1}"
        date_str = row['Date']
        time_str = row['Time']
        
        # Convert date and time to the required format
        date = datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
        time = datetime.strptime(time_str, '%H:%M').strftime('%H:%M:%S')
        
        # Calculate time in seconds
        h, m, s = map(int, time.split(':'))
        time_in_seconds = h * 3600 + m * 60 + s
        
        # Set the added_on and updated_on timestamps (for simplicity, set to noon UTC)
        added_on = f"{date}T12:00:00Z"
        updated_on = added_on
        
        # Add record to the JSON structure
        data["records"].append({
            "_id": record_id,
            "date": date,
            "time": time,
            "timeInSeconds": time_in_seconds,
            "added_on": added_on,
            "updated_on": updated_on
        })
        
        # Update earliest and latest dates
        if earliest_date is None or date < earliest_date:
            earliest_date = date
        if latest_date is None or date > latest_date:
            latest_date = date
    
    # Set the started_on and updated_on fields
    data["started_on"] = f"{earliest_date}T12:00:00Z"
    data["updated_on"] = f"{latest_date}T12:00:00Z"
    
    # Write JSON output to a file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
csv_file_path = './SumiranRecord/data.csv'
json_file_path = './SumiranRecord/data.json'
user_id = '654321'
name = 'Jane Smith'
username = 'janesmith'
csv_to_json(csv_file_path, user_id, name, username, json_file_path)
