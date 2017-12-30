#! /usr/bin/env python3

"""
This will list all instances available and provide an option to ssh into them.
"""
import yaml
import boto3, sys, os
hostname = []
def main():
    for key, value in yaml.load(open('system-domains.yaml'))['domain_names'].items():
        hostname.append(value['hostname'].lower())
    for host in hostname:
        print (host)

if __name__== "__main__":
  main()
