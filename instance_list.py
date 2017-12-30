#! /usr/bin/env python3
"""
This will list all instances available and provide an option to ssh into them.
"""

import boto3, sys, os
instance_name_list = []
def get_region():
    datafile = open('infra.py')
    for line in datafile:
        if 'region' in line:
            region = line[-13:-4]
            return region
def main():
    region = get_region()
    #region = input('Enter region or hit enter for default (us-west-2): ') or 'us-west-2'
    ec2 = boto3.resource('ec2', region_name=region) # call ec2 recourse to perform further actions
    instances = ec2.instances.all()  # get all instances from above region
    for instance in instances:
        if instance.state['Name'] == "running":
            for tags in instance.tags:
                if tags["Key"] == 'Name':
                    instancename = tags["Value"]
            print ("Instance ID: {} Instance Public IP: {} Instance Private IP: {} - {}".format(instance.id,instance.public_ip_address,instance.private_ip_address,instancename))
    print ("End Instance List")

def instance_tags():
    region = get_region()
    #region = input('Enter region or hit enter for default (us-west-2): ') or 'us-west-2'
    ec2 = boto3.resource('ec2', region_name=region) # call ec2 recourse to perform further actions
    instances = ec2.instances.all()  # get all instances from above region
    for instance in instances:
            for tags in instance.tags:
                if tags["Key"] == 'Name':
                    instancename = tags["Value"]
                    if instancename not in instance_name_list:
                        instance_name_list.append(instancename)
    return instance_name_list

if __name__== "__main__":
  main()
