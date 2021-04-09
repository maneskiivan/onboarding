import json
from app_jira import NewHireJira
from app_gsuite import NewHireGsuite
from app_jumpcloud import NewHireJumpCloud
from app_dropbox import NewHireDB
from app_hellosign import NewHireHS
from app_lastpass import NewHireLP


def lambda_handler(event, context):
  data = event['body']
  data_dict = json.loads(data)
  issue_key = data_dict['id']
  # Getting the values from Jira
  new_hire = NewHireJira(issue_key)
  # Create a G Suite account
  new_hire_gsuite = NewHireGsuite(
    new_hire.last_name,
    new_hire.first_name,
    new_hire.title,
    new_hire.department,
    new_hire.employemnt_type,
    new_hire.location,
    new_hire.manager,
    new_hire.email,
    new_hire.password,
    new_hire.google_groups
  )
  # Add the G Suite user to Google Groups
  new_hire_gsuite.gsuite_user_to_group()
  # Create a JumpCloud account
  new_hire_jc = NewHireJumpCloud(
    new_hire.email,
    new_hire.first_name,
    new_hire.last_name,
    new_hire.employemnt_type,
    new_hire.title,
    new_hire.department,
    new_hire.location,
    new_hire.applications_access
  )
  # Get the available groups in JumpCloud
  new_hire_jc.get_jc_groups()
  # Add the JC user to  JC groups based on location, department and applications access
  new_hire_jc.gp_based_on_location()
  new_hire_jc.gp_based_on_department()
  new_hire_jc.gp_based_on_app_access()
  # Create a DropBox and/or HelloSign account based on applications access
  for app in new_hire.applications_access:
    if app == 'DropBox (available only for Design, Accounting and PeopleOps)':
      new_hire_db = NewHireDB(new_hire.email, new_hire.first_name, new_hire.last_name)
    elif app == 'HelloSign':
      new_hire_hs = NewHireHS(new_hire.email)
  # Create a LastPass account based on LastPass (If needed)
  if new_hire.lastpass:
    new_hire_lp = NewHireLP(new_hire.email, new_hire.first_name, new_hire.last_name)
  # Comment in the Jira ticket
  new_hire.update_ticket()

  return {
    'statusCode': 200,
  }