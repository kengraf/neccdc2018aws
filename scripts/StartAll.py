#!/usr/bin/env python

# Cycle through all accounts, starting any stopped instances

import boto3
import sys, getopt

teams = [
    {"team": "team01","account_id":"585631158666"},
    {"team": "team02","account_id":"675745366777"},
    {"team": "team03","account_id":"223014916519"},
    {"team": "team04","account_id":"198460829881"},
    {"team": "team05","account_id":"898938655540"},
    {"team": "team06","account_id":"794057850276"},
    {"team": "team07","account_id":"743590977885"},
    {"team": "team08","account_id":"422498658548"},
    {"team": "team09","account_id":"966498817107"},
    {"team": "team10","account_id":"156756618389"},
    {"team": "team11","account_id":"048794274401"}
]    

def get_aws_security_token(account_id):
    # Use the assertion to get an AWS STS token for cross account work
    session = boto3.session.Session(region_name='us-east-1')
    sts = session.client('sts')
    assumedRole = sts.assume_role(
        RoleArn='arn:aws:iam::{0}:role/OrganizationAccountAccessRole'.format(account_id),
        RoleSessionName='UpdateDNSSession')

    boto3.setup_default_session(aws_access_key_id=assumedRole['Credentials']['AccessKeyId'], 
                                aws_secret_access_key=assumedRole['Credentials']['SecretAccessKey'], 
                                aws_session_token=assumedRole['Credentials']['SessionToken'], 
                                region_name='us-east-1')
    return

def pickInstances(ec2, machine, state='running'):

    reservations = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': [state]}])

    ids = []
    for x in reservations['Reservations']:
        ami = x['Instances'][0]
        if ami.has_key('Tags'):
            for tags in ami['Tags']:
                if machine == 'all':
                    ids.append(ami['InstanceId'])
                elif tags["Key"] == 'Type' and machine == tags["Value"]:
                    ids.append(ami['InstanceId'])
    return ids
    
def main():

    try:
        myopts, args = getopt.getopt(sys.argv[1:],"s:c:t:m:")
    except getopt.GetoptError as e:
        print (str(e))
        print("Usage: %s -s {start|stop} -c cmdFile -t team -m machine" % sys.argv[0])
        sys.exit(2)
    
    state = ''
    cmdFile = ''
    team = 'all'
    machine = 'all'
    for o, a in myopts:
        if o == '-s':
            state=a
        elif o == '-c':
            cmdFile=a
        elif o == '-t':
            team=a
        elif o == '-m':
            machine=a
    
    # Loop over all account to find running instances
    for x in teams:
        if team == 'all' or team == x['team']:
            print ( x['team'] )
            get_aws_security_token(x['account_id'])
            ec2 = boto3.client( 'ec2' )
            if state == 'start':
                ids = pickInstances(ec2, machine,'stopped')
            else:
                ids = pickInstances(ec2, machine,'running')
            
  
            if len(ids) != 0:
                if state == 'start':
                    print( 'starting={}'.format(ids) )
                    response = ec2.start_instances(InstanceIds=ids)
                elif state == 'stop':
                    print( 'stopping={}'.format(ids) )
                    response = ec2.stop_instances(InstanceIds=ids)
                elif cmdFile != '':
                    print( 'execute on={}'.format(ids) )
                    with open(cmdFile) as f:
                        content = f.readlines()  
                    ssm_client = boto3.client('ssm', region_name="us-east-1") 
                    response = ssm_client.send_command(InstanceIds=ids,
                                                DocumentName="AWS-RunShellScript",
                                                Parameters={
                                                    'commands': content
                                                    },
                                                )
    
if __name__ == '__main__':
    main()
