#! /usr/bin/env python3

"""
This will list all instances available and provide an option to ssh into them.
"""
import yaml
import boto3, sys, os, subprocess
from pathlib import Path

def main():
    folders = os.listdir (".")
    for folder in folders:
        parsedomains(folder)
    outputdomains()

hostname = []
def parsedomains(customer):
    file = './{}/system-domains.yaml'.format(customer)
    #print (file)
    my_file = Path(file)
    if my_file.is_file():
        for key, value in yaml.load(open(file))['domain_names'].items():
            if 'cloudfront_ssl_id' in value:
                hostname.append(value['hostname'].lower())
        #for host in hostname:
            #print (host)

def outputdomains():
    thefile = open('domains', 'w')
    for host in hostname:
        thefile.write("{} 443\n".format(host))
    #subprocess.call("~/Downloads/ssl-cert-check -f ~/Downloads/domains", shell=True)
    print ("Done")
if __name__== "__main__":
  main()
