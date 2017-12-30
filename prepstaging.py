#! /usr/bin/env python3

"""
As part of rolling out a staging/dev environment we must disable termination protection followed by force dismounting the EBS volume.This script will assist agents with doing so.
"""

import boto3, sys, os
from time import sleep

instance_case = []

def upper_case(str_, start, end):
    substr = str_[start:end].upper()
    return str_[:start] + substr + str_[end:]
def raise_combinations(str_, length):
    for x in range(len(str_) - length + 1):
        instance_case.append(upper_case(str_, x, x + length) + "*")

def get_region():
    datafile = open('infra.py')
    for line in datafile:
        if 'region' in line:
            region = line[-13:-4]
            return region

def main():
    region = get_region()
    #region = input('Enter region or hit enter for default (us-west-2): ') or 'us-west-2'
    instance_tag = input('What stack would you like to search for (staging, web, dev): ')
    str_ = instance_tag
    for x in range(1, len(str_) + 1):
        raise_combinations(str_, x)
    client = boto3.client('ec2', region_name=region)

    marker = None
    instances = []
    attachedvolumes = []
    volume_id_list = []

    while True:
        paginator = client.get_paginator('describe_instances')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'PageSize': 10,
                'StartingToken': marker})
        for page in response_iterator:
            r = page['Reservations']
            for reservation in r:
                for instance in reservation['Instances']:
                    instances.append(instance['InstanceId'])
                    #print(instance['InstanceId'])
        try:
            marker = page['Marker']
        except KeyError:
            break

    for instance in instances:
        ec2 = boto3.resource('ec2', region_name=region)
        ec2instance = ec2.Instance(instance)
        instancename = ''
        for tags in ec2instance.tags:
            if tags["Key"] == 'Name':
                instancename = tags["Value"]
                if instance_tag.lower() in instancename.lower():
                    for item in ec2instance.volumes.filter(
                        Filters=[{'Name':'tag:Name', 'Values':instance_case}]
                    ):
                      volume_id_list.append(item.id)
                    print("Instance {} is labled as {}. The Volume ID is: {} ".format(instance, instance_tag, volume_id_list))
                    disableterm = input('Would you like to disable termination protection for this instance and dismount the volume? (y/n): ')
                    if disableterm in 'yes':
                        ec2instance.modify_attribute(DisableApiTermination={'Value': False})
                        ec2instance.detach_volume(
                            VolumeId=volume_id_list[0],
                            Force=True
                        )

                        client = boto3.client('ec2', region_name=region)
                        status = ""
                        i = 1
                        while status != 'available':
                            response = client.describe_volumes(
                                VolumeIds=volume_id_list
                            )
                            status = response['Volumes'][0]['State']
                            print('*' * i, end='\r', flush=True)
                            sleep(3)
                            i += 1
                        print ("\nVolume has been detached and Termination Protection Disabled.")
    deploy = input("Would you like to deploy {} now?".format(instance_tag))
    if deploy == 'y' or deploy == 'yes':
        os.system("nimbi deploy {}-ec2".format(instance_tag))
        os.system("nimbi deploy {}-alarms".format(instance_tag))
if __name__== "__main__":
  main()
