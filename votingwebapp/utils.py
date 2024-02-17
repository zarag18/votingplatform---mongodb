# utils.py
import requests

def validate_email(email):
    api_key = '91bb81c484634e21a55c63cd96829a49'
    url = f'https://emailvalidation.abstractapi.com/v1/?api_key=91bb81c484634e21a55c63cd96829a49&email={email}'

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            return data.get('format_valid') and data.get('smtp_check')
        else:
            # Handle API errors
            return False
    except Exception as e:
        # Handle connection errors
        print(f"Error: {e}")
        return False
