import requests
from monteprediction import VERIFICATION_URL


def get_verification_status(email):
    """Sends a request to the Flask endpoint to check an email's verification status."""
    params = {'email': email}
    
    try:
        response = requests.get(VERIFICATION_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('status', 'unknown')
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle exceptions that occur during the request
        print(f"Request failed: {e}")
        return None



if __name__ == "__main__":
    test_email = 'example@example.com'
    status = get_verification_status(test_email)
    if status == 'pending':
         print('Check back in an hour')
    if status == 'verified':
         print('Your submission has been verified')
    if status == 'failed':
         print('Your submission failed, please resubmit')
      
