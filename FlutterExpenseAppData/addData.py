import json
import pandas as pd
import uuid
from datetime import datetime
from clean_data import cleandata

# csv_file = "./FlutterExpenseAppData/output.csv"
userId = "dhruv4023"

csv_files = [
    "C:\\Users\\Dhruv Patel\\OneDrive\\OneNotes\\ExpenseReport\\ExpenseData\\expense_data_2021.csv",
    "C:\\Users\\Dhruv Patel\\OneDrive\\OneNotes\\ExpenseReport\\ExpenseData\\expense_data_2022.csv",
    "C:\\Users\\Dhruv Patel\\OneDrive\\OneNotes\\ExpenseReport\\ExpenseData\\expense_data_2023.csv",
    "C:\\Users\\Dhruv Patel\\OneDrive\\OneNotes\\ExpenseReport\\ExpenseData\\expense_data_2024.csv",
]

# Load and clean data
dataframes = [pd.read_csv(file) for file in csv_files]

# Concatenate all DataFrames
df = pd.concat(dataframes, ignore_index=True)

# df = pd.read_csv(csv_file)
df = cleandata(df)
# df = lableData(df)


# Helper function to generate unique IDs
def generate_id():
    return str(uuid.uuid4().int)[:14]


# Function to parse the date and time, providing default time if necessary
def parse_datetime(date, time):
    dt_str = f"{date} {time}".strip()
    dt_obj = datetime.strptime(dt_str, "%d-%m-%Y %I:%M:%S %p")
    return dt_obj


# Initialize a dictionary to hold wallet data for different years
wallets_data = {}
accounts_and_labels_data = {}

# Dictionary to hold account balances for each year
account_balances = {}

# Initialize dictionaries to track label and account IDs
label_ids = {}
account_ids = {}


def add_label(accounts_and_labels, label_name: str, year: int, default=False):
    doc = {
        "_id": generate_id(),
        "label_name": label_name.strip(),
        "default": default,
        "added_on": datetime.now(),
        "updated_on": datetime.now(),
    }
    accounts_and_labels["labels"].append(doc)
    label_ids[label_name] = doc["_id"]


def add_account(
    accounts_and_labels,
    account_name: str,
    default=False,
):
    doc = {
        "_id": generate_id(),
        "account_name": account_name.strip(),
        "default": default,
        "added_on": datetime.now(),
        "updated_on": datetime.now(),
    }
    accounts_and_labels["accounts"].append(doc)
    account_ids[account_name] = doc["_id"]


def get_or_create_wallet(year):
    wallet_id = f"{userId}_{year}"
    if wallet_id not in wallets_data:
        wallets_data[wallet_id] = {
            "_id": wallet_id,
            "year": str(year),
            "username": userId,
            "transactions": [],
            "opening_balances": [
                {"_id": k, "balance": round(v, 2)} for k, v in account_balances.items()
            ],
            "started_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "updated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        }
    if userId not in accounts_and_labels_data:
        accounts_and_labels_data[userId] = {
            "_id": userId,
            "labels": [],
            "accounts": [],
            "added_on": datetime.now(),
            "updated_on": datetime.now(),
        }
    return wallets_data[wallet_id], accounts_and_labels_data[userId]


# Process each row in the CSV file
for index, row in df.iterrows():
    account = str(row["Account"]).strip()
    label = str(row["Label"]).strip()
    amount = float(row["Amount"])
    message = str(row["Note"]).strip()
    date = str(row["Date"]).strip()
    time = str(row["Time"]).strip()

    # Parse date to get the year
    dt_obj = parse_datetime(date, time)
    year = dt_obj.year

    # Get or create the appropriate wallet and accounts_and_labels structure for the year
    wallet_data, accounts_and_labels = get_or_create_wallet(year)

    if account not in account_ids:
        add_account(accounts_and_labels, account)
        print(account + " account added ...")

    if label not in label_ids:
        add_label(accounts_and_labels, label, year)
        print(label + " label added ...")

    transaction = {
        "_id": generate_id(),
        "comment": message if message else " ",
        "account_id": account_ids.get(account),
        "label_id": label_ids.get(label),
        "amt": amount,
        "added_on": dt_obj.strftime("%Y-%m-%d %H:%M:%S.%f"),
        "updated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    }
    wallet_data["transactions"].append(transaction)
    if account_ids.get(account) not in account_balances:
        account_balances[account_ids.get(account)] = 0.0
    account_balances[account_ids.get(account)] += round(float(amount), 2)
print(account_balances)


# Update the updated_on field for all wallet_data and accounts_and_labels
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
for wallet_id in wallets_data:
    wallets_data[wallet_id]["updated_on"] = current_time
    accounts_and_labels_data[userId]["updated_on"] = current_time

# Save data to JSON files
WALLETS = []
ACCOUNT_AND_LABELS = []

for wallet_id, wallet_data in wallets_data.items():
    WALLETS.append(wallet_data)

for wallet_id, accounts_and_labels in accounts_and_labels_data.items():
    ACCOUNT_AND_LABELS.append(accounts_and_labels)

with open(f"_WALLET.json", "w") as jsonfile:
    json.dump(WALLETS, jsonfile, indent=4, default=str)

with open(f"_ACCOUNT_AND_LABELS_.json", "w") as jsonfile:
    json.dump(ACCOUNT_AND_LABELS, jsonfile, indent=4, default=str)
