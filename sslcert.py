#! /usr/bin/env python3
"""
This will assist in the loading of SSL Certificates
"""

import boto3, sys, os, datetime, time, random

def get_region():
    datafile = open('infra.py')
    for line in datafile:
        if 'region' in line:
            region = line[-13:-4]
            return region
def check_acm():
    datafile = open('infra.py')
    acm = False
    for line in datafile:
        if 'cloudfront_acm_ssl_arn' in line:
            acm = True

            return acm
def main():
    region = get_region()
    domain = input("What Domain are we adding the SSL for?")
    path = "./ssl/{}".format(domain.lower())
    try:
        haskey = os.path.isfile(path + ".key")
        hascrt = os.path.isfile(path + ".crt")
        keymodified = os.path.getmtime(path + ".key")
        crtmodified = os.path.getmtime(path + ".crt")
    except:
        pass
    # print (datetime.datetime.fromtimestamp(
    #     int(keymodified)
    # ).strftime('%Y-%m-%d %H:%M:%S'))
    modified_after = time.time() - 24 * 60 * 60
    # print (datetime.datetime.fromtimestamp(
    #     int(modified_after)
    # ).strftime('%Y-%m-%d %H:%M:%S'))
    if haskey and hascrt:
        if keymodified >= modified_after and crtmodified >= modified_after:
            #pass #OK To Continue
            randomnum = random.randrange(1000,9999)
            now = datetime.datetime.now()
            sslname = str(now.year) + str(randomnum)
            command = "AWS_DEFAULT_REGION=us-east-1 aws iam upload-server-certificate \
            --path \"/cloudfront//\" \
            --server-certificate-name {}-{} \
            --certificate-body file://ssl/{}.crt \
            --private-key file://ssl/{}.key | grep ServerCertificateId | awk -F: '{{print $2}}'".format(domain,sslname,domain,domain)

            response = os.system(command)
            print ("SSL Has been uploaded for {}. Please use the above ID where needed in the system-domains.yaml file".format(domain))
        else:
            print ("CRT/KEY File has not been changed recently")
    else:
        acm = check_acm()
        if acm:
            orderacm = input("No CRT/KEY Found, would you like to order an ACM Cert? ")
            if orderacm == 'y' or orderacm == 'yes':
                print ("This is where I order it")
                while True:
                    validation = input ("Are we going to validate via Email or DNS? (dns/email) ")
                    if validation.lower() not in ['email','dns']:
                        print ("Invalid Selection, Please only type email or dns")
                    else:
                        break
                wildcard = "*." + domain
                idemtoken = random.randrange(1000,9999)
                client = boto3.client('acm', region_name='us-east-1')
                response = client.request_certificate(
                    DomainName=domain,
                    ValidationMethod=validation.upper(),
                    SubjectAlternativeNames=[
                        wildcard,
                    ],
                    IdempotencyToken=str(idemtoken),
                )
                certarn = response['CertificateArn']
                print ("Certificate Requested, Please validate before adding to infra. Certificate ARN: {}".format(certarn))
        else:
            orderacm = False
            print ("No Certificate Files were found and the customer is not configured for ACM certs, please refer to a lead to see if this can be done.")

if __name__== "__main__":
  main()
