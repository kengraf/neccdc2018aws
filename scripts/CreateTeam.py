# Create a new blue team
import os
import getopt
import sys
import boto3
from botocore.exceptions import ClientError
import configparser
import time

def create_organization( client,teamname ):

  email = teamname + '@neccdc2018.org'
  session = boto3.Session(profile_name='neccdc', region_name='us-east-1')
  client = session.client('organizations')
  
  # Check to see if we already have an organization
  found = False
  response = client.list_accounts()
  for acc in response['Accounts']:
    if acc['Name'] == teamname:
      return 
  
  response = client.create_account(Email=email,
                                     AccountName=teamname,
                                     RoleName='OrganizationAccountAccessRole',
                                     IamUserAccessToBilling='DENY')
   
  while response['CreateAccountStatus']['State'] == 'IN_PROGRESS':
    time.sleep(10)
    reqId = response['CreateAccountStatus']['Id']
    response = client.describe_create_account_status(CreateAccountRequestId=reqId)

  # Stop the process if something went wrong
  if response['CreateAccountStatus']['Status'] == 'FAILED':
    print(response)
    exit()

  # Update the configuration
  response = client.describe_account(AccountId=response['CreateAccountStatus']['Id'])
  config[teamname] = { 'account_arn': response['Account']['Arn'],
                       'account_id': response['Account']['Id'],
                       'email': response['Account']['Email'],
                       'role': 'OrganizationAccountAccessRole' }
  return;

def create_user( config, name, team ):
    
  try:
    session = boto3.Session(profile_name=team)
    iam = session.client('iam')
    response = clinet.assume_role(RoleArn='', RoleSessionName='DefineUsers')
    
    user = iam.create_user(UserName=name)
  except ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
      print("User: %s already exists" % name)
    else:
      print("Unexpected error: %s" % e)
      return false

  response = iam.create_access_key(UserName=name)
  # Write access key to credentials file
  config[team]['aws_access_key_id'] = response.AccessKey,AccessKeyId
  config[team]['aws_secret_access_key'] = response.AccessKey,SecretAccessKey

def main():
  
  # Read the configuration file, a section for each team
  config = configparser.ConfigParser()
  
  # Read command line args
  opts, args = getopt.getopt(sys.argv[1:],"n:c:",["name=","cidr="])

  for o, a in opts:
    if o in ( '-n','--name'):
        team_name = a
    elif o in ( '-c','--cidr'):
        team_cidr = a
    else:
        print("Usage: %s -n name -c cidr" % sys.argv[0])
        
#  create_organization(config, team_name)
#  config[team_name]['cidr'] = team_cidr
  
  # Create an all powerful admin and access keys  
  create_user(config, team=team_name, name="TeamAdmin")
  
  # Output a new configuration file
  config.write(sys.stdout)
  exit()

main()
    
