import boto3

# Use the filter() method of the instances collection to retrieve
# all running EC2 instances.
session = boto3.Session(profile_name='saml', region_name='us-east-1')
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.
ec2 = session.client('ec2')

ami = {'name':'Amazon Linux AMI 2016.09.1', 'id':'ami-0b33d91d'}
ami = {'name':'ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-20170405', 'id':'ami-772aa961'}
subnet = {'id':'subnet-changeme', 'name':'changeme'}
secgroup = {'id':'sg-changeme', 'name':'changeme'}

response = ec2.run_instances(ImageId=ami['id'], MinCount=1, MaxCount=1,
                             KeyName='changeme',
                             SubnetId=subnet['id'],
                             InstanceType='m4.xlarge',
                             IamInstanceProfile={'Name':'changeme'},
                             SecurityGroupIds=[secgroup['id']])

instanceId = response['Instances'][0]['InstanceId']

tag = ec2.create_tags(Resources=[instanceId],
                      Tags=[{'Key':'Name','Value':'changeme'}])

print('success')