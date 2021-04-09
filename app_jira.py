import requests
from requests.auth import HTTPBasicAuth
import random
import string
import json
import os

jira_api_email = os.environ.get('jira_api_email')
jira_api_token = os.environ.get('jira_api_token')



class NewHireJira:
  '''Retreives the data from the new hire ticket, comments and transition the ticket'''
  def __init__(self, issue_key):
    '''Gets the required fields from the new hire issue. Assigns them to the appropriate variables.'''
    self.__issue_key = issue_key
    url = f"https://gumgum.jira.com/rest/api/2/issue/{self.__issue_key}"

    self.__auth = HTTPBasicAuth(jira_api_email, jira_api_token)

    headers = {
      "Accept": "application/json"
    }

    query = {
      'fields': ['customfield_13546', 'customfield_13547', 'customfield_13943', 'customfield_13560',
                 'customfield_13550', 'customfield_13549', 'customfield_13552', 'customfield_13954',
                 'customfield_13953', 'customfield_13557', 'customfield_13561', 'issuetype']

    }

    response = requests.request(
      "GET",
      url,
      headers=headers,
      params=query,
      auth=self.__auth,
      )


    response_dict = response.json()
    # Adding the values from the custom fields to the appropriate variables
    new_hire_name_value = response_dict['fields']['customfield_13546']
    new_hire_name_value_list = new_hire_name_value.split()
    self.last_name = new_hire_name_value_list[1]
    self.first_name = new_hire_name_value_list[0]
    self.title = response_dict['fields']['customfield_13547']
    self.email = response_dict['fields']['customfield_13943']
    self.employemnt_type = None
    employemnt_type = response_dict['fields']['customfield_13560']
    for key, value in employemnt_type.items():
      if key == 'value':
        self.employemnt_type = value
    manager = response_dict['fields']['customfield_13550']
    self.manager = None
    for key, value in manager.items():
        if key == 'emailAddress':
            self.manager = value
    location = response_dict['fields']['customfield_13549']
    self.location = None
    for value in location.values():
        if value == 'Santa Monica':
            self.location = 'SM'
        elif value == 'New York':
            self.location = 'NY'
        elif value == 'Chicago':
            self.location = 'CHI'
        elif value == 'London':
            self.location = 'UK'
        elif value == 'Tokyo':
            self.location = 'JP'
        elif value == 'Remote':
            self.location = 'Remote'
        elif value == 'San Francisco':
            self.location = 'Remote'
    self.department = None
    if  response_dict['fields']['customfield_13954'] == None:
        department = response_dict['fields']['customfield_13953']
        for key, value in department.items():
            if key == 'value':
                self.department = value
    else:
        department = response_dict['fields']['customfield_13954']
        for key, value in department.items():
            if key == 'value':
                self.department = value
    google_groups_string = response_dict['fields']['customfield_13552']
    self.google_groups = google_groups_string.splitlines()
    applications_access = response_dict['fields']['customfield_13557']
    self.applications_access = []
    for selection in applications_access:
      self.applications_access.append(selection['value'])
    self.lastpass = False
    if response_dict['fields']['customfield_13561']:
      self.lastpass = True
    # create a random password
    random_source = string.ascii_letters + string.digits + string.punctuation
    generated_password = random.choice(string.ascii_lowercase)
    generated_password += random.choice(string.ascii_uppercase)
    generated_password += random.choice(string.digits)
    generated_password += random.choice(string.punctuation)

    for i in range(4):
      generated_password += random.choice(random_source)

    password_list = list(generated_password)
    random.SystemRandom().shuffle(password_list)
    self.password = ''.join(password_list)

  def update_ticket(self):
    '''Comments in the Jira ticket'''
    url = f'https://gumgum.jira.com/rest/api/2/issue/{self.__issue_key}/comment'

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }

    username = self.email[:self.email.index("@")]

    body = f"The following accounts have been created:" \
           f"\nG Suite" \
           f"\nEmail: {self.email}" \
           f"\nPassword: {self.password}" \
           f"\nMac" \
           f"\nUsername: {username}" \
           f"\nPassword: {self.password}" \
           f"\nJumpCloud" \
           f"\nJira" \
           f"\nZoom" \
           f"\nSlack"

    for application in self.applications_access:
      if application == 'DropBox (available only for Design, Accounting and PeopleOps)':
        body = body + f'\nDropBox'
      elif application == 'HelloSign':
        body = body + f'\nHelloSign'
      elif application == 'SumoLogic':
        body = body + f'\nSumoLogic'
      elif application == 'Verity Databricks Prod':
        body = body + f'\nVerity Databricks Prod'

    if self.lastpass:
      body = body + f'\nLastPass'

    payload = json.dumps({
      "body": body
    })

    response = requests.request(
      "POST",
      url,
      data=payload,
      headers=headers,
      auth=self.__auth
    )