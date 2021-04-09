import requests
import json
import os

lastpass_token = os.environ.get('lastpass_token')


class NewHireLP:
  '''Creates a new LastPass user account'''
  def __init__(self, email, first_name, last_name):
    url = 'https://lastpass.com/enterpriseapi.php'

    payload = json.dumps(
      {
      "cid": 9131752,
      "provhash": lastpass_token,
      "cmd": "batchadd",
      "data": [
        {
          "username": email,
          "fullname": f'{first_name} {last_name}',
          "password": "DefaultPassword",
          "password_reset_required": True
        }
      ]
    }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=payload)
