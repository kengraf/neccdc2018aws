## NECCDC 2018 Blue Team Quick Start

The CloudFormation templates have been derived from AWS' Goldbase templates.

There are three (3) template tiers: 1) infrastructure 2) scoring 3) service

The infrastructure templates have the following design goals:
* Same deployment for team practice, qualifying, and regional event.
* Allow teams to deploy independantly into a Blue team managed account.
* Deploy all access, network, and resources required to deploy the application an scoring tiers.

Scoring templates
* This public repo will only know how to score the sample web service.
* The template will be parameterized to faciliate the services used in qualifying and regional.
* Allow testing of Black team infrastructure.

Service templates design goals
* This public repo will contain only a sample web service.
* The template will be parameterized to faciliate the services used in qualifying and regional.
* Allow testing of Black team infrastructure.

During qualifying and regional AWS organizations will used to control access.
* Only the Black with have the access rights needed to successfully deploy the infrastructure and scoring template tiers.
* Each team will be issued an account controlled by the Black team.
* AWS root credentials will be held by the Black team.
* One or more users/roles will be created to allow Blue teams to manage their services.

Prereqs:

* [AWS Account](https://aws.amazon.com/)
* [Git installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [AWS CLI installed and configured](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)
* [Ansible installed and configured](http://docs.ansible.com/ansible/latest/intro_installation.html)

The UNH team offered this guidance to setup an Ansible control box based on AWS EC2:

Set up an Ansible control box using AWS

launch ec2 instance use an AWS linux, the security group needs to allow SSH

    sudo yum -y install git
    sudo pip install ansible pan-python pandevice xmltodict boto3 botocore
    ansible-galaxy install PaloAltoNetworks.paloaltonetworks
    git clone https://github.com/kengraf/neccdc2018automation

# Configure identity
Copy your private to the Ansible control box.  Needed for SSH to Palo Alto system.

# Example (you will need your own values):
    scp -i neccdc.pem neccdc.pem ec2-user@54.208.19.212:neccdc.pem

# Configure the AWS CLI on the Ansible control box.
    $ aws configure
    AWS Access Key ID [None]: AKIAJK............
    AWS Secret Access Key [None]: xUuIs..................................
    region name [None]: us-east-1
    Default output format [None]: json

# fix bug in PaloAlto role
    Edit /home/ec2-user/.ansible/roles/PaloAltoNetworks.paloaltonetworks/library/panos_nat_rule.py

locate the line: 'from ansible.module_utils.basic import get_exception'

add a new line: 'from ansible.module_utils.basic import AnsibleModule'

# Configure your playbook
    cd ~/neccdc2018automation

# Edit the 'VARS' section of the playbook 
    vi ./playbooks/create-team-stack.yml
# The UNH team's var section looked like this:

    # Standalone deploys can use the default, event will teamX
    team_name: "{{ team | default('team1') }}"
    # Standalone deploys can use the default, event will use campus name XXX.edu
    school_name: "{{ campus | default('unh') }}"
    # AMI selected are based in us-east-1
    region: "us-east-1"
    
    # Parameters specific to a team are maintained in the .aws/credentials file
    white_cidr: "{{ lookup('ini', 'cidr section=neccdc file=~/.aws/credentials') }}"
    campus_cidr: "{{ lookup('ini', 'cidr section={{ school_name }} file=~/.aws/credentials') }}"
    aws_access_key: "{{ lookup('ini', 'aws_access_key_id section={{ school_name }} file=~/.aws/credentials') }}"
    aws_secret_key: "{{ lookup('ini', 'aws_secret_access_key section={{ school_name }} file=~/.aws/credentials') }}"
    key_name: "{{ lookup('ini', 'ssh_keyname section={{ school_name }} file=~/.aws/credentials') }}"
    key_filename: "{{ lookup('ini', 'ssh_keyfile section={{ school_name }} file=~/.aws/credentials') }}"
    
    # Palo Alto admin user
    admin_username: "admin"
    # Password defined for Palo Alto web interface
    admin_password: "Neccdc-2018"

# We use the AWS credential file to keep private outside of this repo.
# There is additional information placed in that file.  "credentials" is provided as an example.
    
# Run the Ansible playbook to setup the stack
    ansible-playbook ./playbooks/create-team-stack.yml

The Palo Alto management HTTPS IP is reported by TASK [FirewallManagementEIP]
The SSH/HTTP access to the protected service is reported by TASK [FirewallPublicDataInterface]

The stack takes less than 5 minutes to deploy.  The Palo Alto configure steps take less than 10 minutes.  Is normal to see logins timeouts at the Palo Alot server does take some time to fully spin up.

It'll take less than 5 minutes to create the network infrastructure and IAM 

This playbook will also install a Palo Alto VM100 server.
The server is unlicensed; it will process traffic but most features are not available until a licnese is applied (separate team action).
A simple web server with SSH enabled is also deployed.

This just a practice environment, expect the qualifier and regional events to be different.
