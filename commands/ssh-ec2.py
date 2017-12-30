#! /usr/bin/env python3

import boto3
import botocore
import paramiko

key = paramiko.RSAKey.from_private_key_file(open("/Users/ilamottekerr/.ssh/config", "r"))
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect/ssh to an instance
try:
    # Here 'ec2-user' is user name and 'instance_ip' is public IP of EC2
    client.connect(hostname="54.202.89.132", username="ec2-user", pkey=key)

    # Execute a command(cmd) after connecting/ssh to an instance
    stdin, stdout, stderr = client.exec_command(cmd)
    print stdout.read()

    # close the client connection once the job is done
    client.close()
    break

except Exception, e:
    print e
