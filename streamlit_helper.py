import requests
import json

def perform_api_call(endpoint):
    """
    Makes the API call to a defined endpoint
    """
    url = f'http://localhost:8000/{endpoint}'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer 1337'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        print("Error:", response.status_code)

def check_menu():
    return perform_api_call("menu")

def check_inventory():
    return perform_api_call("inventory")

def purchase_ice_cream(input_flavor, input_quantity):
    return perform_api_call(f"orders?flavor={input_flavor}&quantity={input_quantity}")

def restock_ice_cream(restock_flavor, restock_quantity):
    return perform_api_call(f"restock?flavor={restock_flavor}&quantity={restock_quantity}")

def give_user_feedback(user_feedback, user_rating):
    return perform_api_call(f"give_feedback?feedback={user_feedback}&rating={user_rating}")

def get_all_feedback():
    return perform_api_call("get_feedback")

def feedback_report():
    return perform_api_call("report")