import dropbox
import os

drop_box_token = os.environ.get('drop_box_token')

class NewHireDB:

  def __init__(self, email, first_name, last_name):
    '''Creates a new user in DropBox and sends an invitation email'''
    dbx_team = dropbox.DropboxTeam(drop_box_token)
    member = dropbox.team.MemberAddArg(
      member_email=email,
      member_given_name=first_name,
      member_surname=last_name,
      send_welcome_email=True)
    try:
      dbx_team.team_members_add([member])
    except:
      pass