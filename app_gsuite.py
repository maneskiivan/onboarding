import requests
import pickle
from googleapiclient.discovery import build
import os


class NewHireGsuite:
  '''"""Creates a user in G Suite and adds the user to Google groups'''
  def __init__(
    self,
    lastname,
    firstname,
    title,
    department,
    employemnt_type,
    location,
    manager,
    email,
    password,
    google_groups
  ):
    self.__email = email
    self.__google_groups = google_groups
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    # Create a new token.pickle file if needed on a local machine and upload it to AWS
    with open('/mnt/efs/token.pickle', 'rb') as token:
      creds = pickle.load(token)
      
    self.__service = build('admin', 'directory_v1', credentials=creds, cache_discovery=False)

    # Creates the user in G Suite
    user = {
      "name": {"familyName": lastname, "givenName": firstname, },
      'organizations': [
        {'title': title, 'department': department, 'description': employemnt_type}],
      'locations': [{'type': 'desk', 'area': 'desk', 'buildingId': location}],
      'relations': [{'value': manager, 'type': 'manager'}],
      "password": password,
      "primaryEmail": email,
      "changePasswordAtNextLogin": True,
    }

    # Call the Admin SDK Directory API to create the user
    try:
      results = self.__service.users().insert(body=user).execute()
      create = requests.post('https://www.googleapis.com/admin/directory/v1/users', data=user)
    except:
      pass

  def gsuite_user_to_group(self):
    '''Adds a user to google groups'''
    member = {
      "email": self.__email,
      "role": "MEMBER"
    }

    # Call the Admin SDK Directory API to add the user to the groups
    for group in self.__google_groups:
      try:
        results = self.__service.members().insert(groupKey=group, body=member).execute()
      except:
        pass