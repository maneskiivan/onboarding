from hellosign_sdk import HSClient
import os

hello_sign_apikey = os.environ.get('hello_sign_apikey')

class NewHireHS:
  '''Creats a new user account in HelloSign'''
  def __init__(self, email):
    client = HSClient(api_key=hello_sign_apikey)
    new_account = client.add_team_member(email_address=email)