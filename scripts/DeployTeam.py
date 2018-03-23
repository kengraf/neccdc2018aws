# Create a new blue team
import os
import getopt
import sys
import boto3
from botocore.exceptions import ClientError
import configparser

# Predetermined values specific to 2018
PARENT_ID = 'ou-ej2m-9e1lj6fx'

def create_organization( config,TeamName ):
  global PARENT_ID
  
  session = boto3.Session(profile_name='neccdc', region_name='us-east-1')
  client = session.client('organizations')
  
  response = client.create_organizational_unit(ParentId=PARENT_ID, Name=TeamName)
  print (response)

  response = client.create_account(Email=TEAM_EMAIL,
                                   AccountName=TeamName,
                                   RoleName='OrganizationAccountAccessRole',
                                   IamUserAccessToBilling='DENY')
  print (response)   
  
  config.add_section(team_name)
  config.set(team_name, 'account_arn', arn)
  config.set(team_name, 'account_id', id)
  config.set(team_name, 'role', 'OrganizationAccountAccessRole')
  
  # Create SSH keypair
  response = client.create_key_pair( TeamName )
  config.set(team_name, 'ssh_key', response.KeyMaterial )
  config.set(team_name, '', team_name )
  
  return;

def create_user( name ):
    
  try:
    iam = boto3.client('iam')
    user = iam.create_user(UserName=name)
    print("Created user: %s" % user)
  except ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
      print("User: %s already exists" % name)
    else:
      print("Unexpected error: %s" % e)
      return false

  response = iam.create_access_key(UserName=name)
  # Write access key to credentials file
  config_file[team_name]['access_key_id'] = response.

def main():
  global TEAM_EMAIL
  
  # Read the configuration file, a section for each team
  config_file = configparser.ConfigParser()
  config_file.read(os.environ.get('NECCDC_CONFIG'))
  
  # Read command line args
  opts, args = getopt.getopt(sys.argv[1:],"n:c:e:",["name=","cidr=","email="])

  for o, a in opts:
    if o in ( '-n','--name'):
        team_name = a
    elif o in ( '-e','--email'):
        TEAM_EMAIL = a
    elif o in ( '-c','--cidr'):
        TEAM_CIDR = a
    else:
        print("Usage: %s -n name -e email -c cidr" % sys.argv[0])
        
  # Create an organization if needed
  if team_name in config_file:
    print('Updating: '+team_name)
  else:
    create_organization(config_file, team_name)
    return 0
  
  # Create an all powerful admin and access keys  
  create_user(config_file, "TeamAdmin")
  
  # Output a new configuration file
  config_file.write(sys.stdout)
  
  return 0

main()
    
