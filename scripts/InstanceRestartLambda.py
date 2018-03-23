import logging
import boto3
import urllib2

logger = logging.getLogger()
logger.setLevel(logging.INFO)
systems=[{'type':"PaloAlto",'ssm':"https://s3.amazonaws.com/wildeagle/paloalto.ssm"},
    {'type':"proxy",'ssm':"https://s3.amazonaws.com/wildeagle/proxy.ssm"},
    {'type':"jumpbox",'ssm':"https://s3.amazonaws.com/wildeagle/jumpbox.ssm"},
    {'type':"mail",'ssm':"https://s3.amazonaws.com/wildeagle/mail.ssm"},
    {'type':"helpdesk",'ssm':"https://s3.amazonaws.com/wildeagle/helpdesk.ssm"},
    {'type':"training",'ssm':"https://s3.amazonaws.com/wildeagle/training.ssm"}]

def bootCommands(id,type):
    ssm = boto3.client('ssm')
    for x in systems:
        if x['type'] == type:
            response = urllib2.urlopen(x['ssm'])
            parms = {"commands":[ response.read() ]}
            ssm.send_command(InstanceIds=[id],DocumentName='AWS-RunShellScript',
                             Parameters=parms )
    return

def lambda_handler(event, context):
    id = event['detail']['instance-id']
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(id)
    logger.info('instance-id='+id)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Type':
            bootCommands(id,tags["Value"])
    return ''
lambda_handler({'detail':{'instance-id':'i-02050b3841682e8df'}},'q')