import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests



# API_KEY = "AIzaSyC_oPEQ4fx-GI_PVzWSwBA9wCHd21CiMAo"
# SHEET_ID = "1nOe7h-6-sSe7akaP8BJwbqL1dNwVrP8tvSaaes2_DU8"
# RANGE = "Sheet1!A:Z" 

# url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{RANGE}?key={API_KEY}"

def __init__(self, config):
    """"Config must include API_KEY, SHEET_ID. RANGE have or not."""
    self.API_KEY = config["API_KEY"]
    self.SHEET_ID = config["SHEET_ID"]
    
def get_sheet_data(self, RANGE=None):
    """Return data from gg sheet type array 2D"""
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.SHEET_ID}/values/{RANGE}?key={self.API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("values", [])  # Get values or empty list
    else:
        print("Error:", response.status_code, response.text)
        return None

