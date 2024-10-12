import pandas as pd


# Define the categorize function with the additional categories
def categorize(message):
    message = str(message).lower()
    if "self transfer" in message:
        return "SELF TRANSFER"
    if "gpay lite" in message:
        return "GPAY LITE"
    if "higher study" in message:
        return "HIGHER STUDY"
    if "hotel review" in message:
        return "HOTEL REVIEW"
    if "cashback" in message:
        return "CASHBACK"
    if "mummy" in message:
        return "Mummy"
    if "kirtan" in message:
        return "KIRTAN"
    if "study" in message or "education" in message:
        return "Education"
    if "amazon" in message:
        return "Amazon"
    if "recharge" in message:
        return "Recharge"
    if "deal" in message:
        return "Top Deals"
    if (
        "biil" in message
        or "bill" in message
        or "electricity" in message
        or "light" in message
        or "gas" in message
        or "policy" in message
    ):
        return "Bills"
    if "food" in message:
        return "Food"
    if "fees" in message or "fee" in message:
        return "Fees"
    if "int" in message or "interest" in message:
        return "Interest"
    if "train" in message or "ticket" in message:
        return "Travel"
    if "deposit" in message:
        return "Deposit"

    if "me" in message:
        return "ME"
    if "transport" in message or "train" in message or "bus" in message:
        return "Transport"
    if "fk" in message:
        return "FK"
    return "Other"


def lableData(df: pd.DataFrame):
    # Apply the categorize function to create a new 'Category' column
    df["Label"] = df["Message"].apply(categorize)
    return df
