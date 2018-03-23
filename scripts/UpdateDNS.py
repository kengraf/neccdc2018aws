#!/usr/bin/env python

# Cycle through all accounts, updating all DNS entries
# DNS value determined by EC2 instance tag "DNS"

import boto3

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_SESSION_TOKEN = ''

dns_records = []

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

def route53update():
    zones= [{'domain':'neccdc2018.org','zone':'Z2OFBDQ1DF8ZZB'},
            {'domain':'cyber-unh.org','zone':'ZRWFREAU725TM'},
            {'domain':'wildeagle.net','zone':'Z39MUFJOVZF1T0'},
            ]
    boto3.setup_default_session(region_name='us-east-1')
    r53 = boto3.client( 'route53' )
    for x in dns_records:
        if x['dns'].find(zones[0]['domain']):
            zone = zones[0]['zone']
        if x['dns'].find(zones[1]['domain']):
            zone = zones[1]['zone']
        if x['dns'].find(zones[2]['domain']):
            zone = zones[2]['zone']
            
        r53.change_resource_record_sets(
            HostedZoneId=zone,
            ChangeBatch={ "Changes": [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': x['dns'],
                        'Type': 'A',
                        'ResourceRecords': [ { 'Value': x['ip'] } ],
                        'TTL': 300
                    }
                }
            ]})
    return

def resetZone(ip, instances):
    global dns_records
    print( 'zone reset' )
    for x in instances:
        if x.has_key('Tags'):
            for tags in x['Tags']:
                if tags["Key"] == 'PROXY':
                    print( "{0}={1}".format(tags["Value"],ip))
                    dns_records.append({'dns':tags["Value"], 'ip':ip})
    return

def paloAltoIP(ec2, instances):
    for x in instances:
        if x.has_key('Tags'):
            for tags in x['Tags']:
                if tags["Key"] == 'Type':
                    if tags["Value"] == 'paloalto':
                        for nic in x['NetworkInterfaces']:
                            if nic['Description'] == 'AWS FW1 E1/1':
                                if nic.has_key('Association'):
                                    return nic['Association']['PublicIp']

    return ''
    
def retrieveInstances():
    global dns_records
    ec2 = boto3.client( 'ec2' )    
    reservations = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    
    instances = []
    for x in reservations['Reservations']:
        instances.append( x['Instances'][0] )
    
    ip = paloAltoIP(ec2, instances)
    if ip != '':
        resetZone(ip, instances)
    for x in instances:
        if x.has_key('Tags'):
            for tags in x['Tags']:
                if tags["Key"] == 'DNS' or tags["Key"] == 'DNSMX':
                    print( "{0}={1}".format(tags["Value"],x['PublicIpAddress']))
                    dns_records.append({'dns':tags["Value"], 'ip':x['PublicIpAddress']})
    return
    
def main():
    
    # Loop over all account to find running instances
    for x in teams:
        print ( x['team'] )
        get_aws_security_token(x['account_id'])
        retrieveInstances()
        
    # Update Route53 for any instance with a DNS tag
    route53update()

if __name__ == '__main__':
    main()
