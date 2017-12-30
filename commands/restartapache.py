#! /usr/bin/env python3

"""
This will list all instances available and provide an option to ssh into them.
"""

import boto3
from time import sleep

instancelist = []
def get_region():
    datafile = open('infra.py')
    for line in datafile:
        if 'region' in line:
            region = line[-13:-4]
            return region
region = get_region()
client = boto3.client('ssm', region_name=region)



response = client.send_command(
    Targets=[
        {
            'Key': 'tag:Name',
            'Values': [
                'WebTier',
            ]
        },
    ],
    DocumentName='AWS-RunShellScript',
    TimeoutSeconds=30,
    Comment='This is a script to restart httpd',
    Parameters={
        'commands': [
            'service httpd restart',
        ]
    }
)
#print (response)
#print ("*" * 20)
ec2 = boto3.resource('ec2', region_name=region) # call ec2 recourse to perform further actions
instances = ec2.instances.all()  # get all instances from above region
for instance in instances:
    if instance.state['Name'] == "running":
        for tags in instance.tags:
            if tags["Key"] == 'Name':
                instancename = tags["Value"]
                if instancename == 'WebTier':
                    instancelist.append(instance.id)
        #print ("Instance ID: {} Instance Public IP: {} Instance Private IP: {} - {}".format(instance.id,instance.public_ip_address,instance.private_ip_address,instancename))
#print (instancelist)
sleep(2)
for instance in instancelist:
    request = response['Command']['CommandId']
    try:
        requestresponse = client.get_command_invocation(
            CommandId=request,
            InstanceId=instance
        )
        stdout = requestresponse['StandardOutputContent']
        print ("{} has ran the command, the output is\n{}".format(instance, stdout))
    except:
        print ("There was an error while running on {}. Please Review".format(instance))
