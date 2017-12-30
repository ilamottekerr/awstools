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

def parse_domain(domain, mytag):
    client = boto3.client('ssm', region_name=region)
    #substrline = '{ print substr($0, index($0,$4)) }'
    mycommand = "cut -d $' ' -f4- /home/{}/logs/{}-php-error.log | sort | uniq -c | sort -r".format(domain, domain)
    response = client.send_command(
        Targets=[
            {
                'Key': 'tag:Name',
                'Values': [
                    mytag,
                ]
            },
        ],
        DocumentName='AWS-RunShellScript',
        TimeoutSeconds=30,
        Comment='This is a script to check domain error logs',
        Parameters={
            'commands': [
                mycommand,
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
                    if mytag == instancename:
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
        print ("*" * 40)

def main():
    import instance_list
    import domainlist
    instance_name_list = instance_list.instance_tags()
    print ("Available Instance Category Names")
    for instance_name in instance_name_list:
        print ("{}".format(instance_name))
    print ("*" * 40)
    mytag = input ("Which Instance Tag Would You Like to View Logs For?(q to quit) ")
    domainlist.main()
    print ("*" * 40)
    domain = input ("Which Domain Would You Like to View Logs For?(q to quit) ")
    if domain != 'q':
        parse_domain(domain,mytag)
    else:
        print ("Thanks for checking the logs! Bye!")
        quit

if __name__== "__main__":
  main()
