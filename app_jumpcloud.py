import jcapiv1
from jcapiv1.rest import ApiException
import jcapiv2
from jcapiv2.rest import ApiException
import os

jumpcloud_org_id = os.environ.get('jumpcloud_org_id')
jumpcloud_apikey = os.environ.get('jumpcloud_apikey')


class NewHireJumpCloud:
  '''Creates a new user in JumpCloud and adds the user to JumpCloud user groups'''
  def __init__(
    self,
    email,
    first_name,
    last_name,
    employemnt_type,
    title,
    department,
    location,
    applications_access
  ):
    self.__jc_user_id = None
    self.__jc_groups = None
    self.__department = department
    self.__location = location
    self.__applications_access = applications_access
    self.__email = email
    self.__first_name = first_name
    self.__last_name = last_name
    self.__employement_type = employemnt_type
    self.__title = title

    self.__username = email[:email.index("@")]
    self.__displayname = f'{first_name} {last_name}'
    
    # Configure API key authorization: x-api-key
    configuration = jcapiv1.Configuration()
    configuration.api_key['x-api-key'] = jumpcloud_apikey
    # create an instance of the API class
    api_instance = jcapiv1.SystemusersApi(jcapiv1.ApiClient(configuration))
    content_type = 'application/json'  # str |  (default to application/json)
    accept = 'application/json'  # str |  (default to application/json)
    x_org_id = jumpcloud_org_id  # str |  (optional) (default to )
    body = jcapiv1.Systemuserputpost(
      email=self.__email,
      username=self.__username,
      firstname=self.__first_name,
      lastname=self.__last_name,
      displayname=self.__displayname,
      employee_type=self.__employement_type,
      department=self.__department,
      job_title=self.__title
    )

    try:
      # Create a system user and save the id
      api_response = api_instance.systemusers_post(content_type, accept, body=body, x_org_id=x_org_id)
      self.__jc_user_id = api_response.id
    except ApiException as e:
      pass

  def get_jc_groups(self):
    '''Gets the groups from JumpCloud'''
    # Configure API key authorization: x-api-key
    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = jumpcloud_apikey
    # create an instance of the API class
    api_instance = jcapiv2.GroupsApi(jcapiv2.ApiClient(configuration))
    content_type = 'application/json'  # str |  (default to application/json)
    accept = 'application/json'  # str |  (default to application/json)
    fields = [
      '[]']  # list[str] | The comma separated fields included in the returned records. If omitted, the default list of fields will be returned.  (optional) (default to [])
    filter = [
      '[]']  # list[str] | Supported operators are: eq, ne, gt, ge, lt, le, between, search, in (optional) (default to [])
    limit = 100  # int | The number of records to return at once. Limited to 100. (optional) (default to 10)
    skip = 0  # int | The offset into the records to return. (optional) (default to 0)
    sort = [
      '[]']  # list[str] | The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending.  (optional) (default to [])
    x_org_id = jumpcloud_org_id  # str |  (optional) (default to )

    try:
      # List All Groups
      self.__jc_groups = api_instance.groups_list(content_type, accept, fields=fields, filter=filter, limit=limit,
                                                  skip=skip, sort=sort, x_org_id=x_org_id)
    except ApiException as e:
      pass

  def add_jc_user_to_group(self, jc_group_id):
    '''Adds a user to a user group in jumpcloud'''
    # Configure API key authorization: x-api-key
    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = jumpcloud_apikey
    # create an instance of the API class
    api_instance = jcapiv2.UserGroupMembersMembershipApi(jcapiv2.ApiClient(configuration))
    group_id = jc_group_id  # str | ObjectID of the User Group.
    content_type = 'application/json'  # str |  (default to application/json)
    accept = 'application/json'  # str |  (default to application/json)
    x_org_id = jumpcloud_org_id  # str |  (optional) (default to )
    body = jcapiv2.UserGroupMembersReq(id=self.__jc_user_id, op='add',
                                       type='user')  # UserGroupMembersReq |  (optional)

    try:
      # Manage the members of a User Group
      api_instance.graph_user_group_members_post(group_id, content_type, accept, body=body, x_org_id=x_org_id)
    except ApiException as e:
      pass

  def gp_based_on_location(self):
    '''Adds the JC user to user groups based on the location value'''
    if self.__location == 'SM':
      for group in self.__jc_groups:
        if group.name == 'SM-Users':
          self.add_jc_user_to_group(group.id)
    elif self.__location == 'NY':
      for group in self.__jc_groups:
        if group.name == 'NY-Users':
          self.add_jc_user_to_group(group.id)
    elif self.__location == 'CHI':
      for group in self.__jc_groups:
        if group.name == 'CHI-Users':
          self.add_jc_user_to_group(group.id)
    elif self.__location == 'CHI':
      for group in self.__jc_groups:
        if group.name == 'CHI-Users':
          self.add_jc_user_to_group(group.id)
    elif self.__location == 'JP':
      for group in self.__jc_groups:
        if group.name == 'JP-Users':
          self.add_jc_user_to_group(group.id)
    elif self.__location == 'JP':
      for group in self.__jc_groups:
        if group.name == 'JP-Users':
          self.add_jc_user_to_group(group.id)
    elif self.__location == 'UK':
      for group in self.__jc_groups:
        if group.name == 'UK-Users':
          self.add_jc_user_to_group(group.id)
    elif self.__location == 'Remote':
      for group in self.__jc_groups:
        if group.name == 'Remote-Users':
          self.add_jc_user_to_group(group.id)

  def gp_based_on_department(self):
    '''Adds the JC user to user groups based on the department value'''
    for group in self.__jc_groups:
      if group.name == self.__department:
        self.add_jc_user_to_group(group.id)

    # Adding jc user to Lattice
    for group in self.__jc_groups:
      if group.name == 'Lattice-Users':
        self.add_jc_user_to_group(group.id)

  def gp_based_on_app_access(self):
    '''Adds the JC user to user groups based on the application access value'''
    db_groups_list = ['Design', 'Finance & Accounting', 'Network IT', 'People Operations']
    hs_groups_list = ['Account Management', 'Ad Operations', 'Domestic Sales', 'Executive & Admin', 'Network IT', 'Product Management', 'Programmatic']
    sf_groups_list = ['Account Management',
                      'Business Intelligence',
                      'Domestic Sales',
                      'Executive & Admin',
                      'Growth Strategy',
                      'Japan Sales',
                      'Marketing & Sales Strategy',
                      'Network IT',
                      'Programmatic',
                      'Publisher Development',
                      'Sports Marketing',
                      'Sports Sales',
                      'UK-Users']
    hubspot_group_list = ['Network IT', 'Sports Marketing']

    for application in self.__applications_access:
      if application == 'DropBox (available only for Design, Accounting and PeopleOps)' and self.__department not in db_groups_list:
        for group in self.__jc_groups:
          if group.name == 'DropBox-Users':
            self.add_jc_user_to_group(group.id)
      elif application == 'HelloSign' and self.__department not in hs_groups_list:
        for group in self.__jc_groups:
          if group.name == 'HelloSign-Users':
            self.add_jc_user_to_group(group.id)
      elif application == 'SalesForce':
        for group in self.__jc_groups:
          if group.name == 'SalesForce-Users' and self.__department not in sf_groups_list:
            self.add_jc_user_to_group(group.id)
      elif application == 'HubSpot':
        for group in self.__jc_groups:
          if group.name == 'HubSpot-Users' and self.__department not in hubspot_group_list:
            self.add_jc_user_to_group(group.id)
      elif application == 'SumoLogic':
        for group in self.__jc_groups:
          if group.name == 'SumoLogic-Analyst':
            self.add_jc_user_to_group(group.id)
      elif application == 'Verity Databricks Prod':
        for group in self.__jc_groups:
          if group.name == 'Verity Databricks Prod' and self.__department != 'Verity':
            self.add_jc_user_to_group(group.id)