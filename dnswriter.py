#! /usr/bin/env python3
asub = {}
arecords = []
mxsub = {}
mxrecords = []
txtsub = {}
txtrecords = []
cnamesub = {}
cnamerecords = []
ips = {}


i = 0
def main():
    domain = input('Enter domain name:') or ''
    while True:
        subdomain = input('Enter subdomain prefix:') or ''
        recordtype = input('Enter Record Type (CNAME, MX, A, TXT):')
        record = input('Enter record:')
        ttl = input('Enter ttl:')
        if recordtype.upper() == 'A':
            arecords.append([recordtype, record, ttl, subdomain])
            asub[subdomain] = []
        if recordtype.upper() == 'MX':
            mxrecords.append([recordtype, record, ttl, subdomain])
            mxsub[subdomain] = []
        if recordtype.upper() == 'TXT':
            txtrecords.append([recordtype, record, ttl, subdomain])
            txtsub[subdomain] = []
        if recordtype.upper() == 'CNAME':
            cnamerecords.append([recordtype, record, ttl, subdomain])
            cnamesub[subdomain] = []
        keepgoing = input('Do you have more records to enter? (y/n):')
        if keepgoing == 'n' or keepgoing == 'no':
            break;

    for entry in arecords:
        dstart = domain[0:3].upper()
        lastoctet = entry[1].split('.')
        ipname = dstart + lastoctet[3]
        ips[domain[0:3] + lastoctet[3]] = (entry[1])
    print ("The following variables need to be set for the A records to work:")
    print (" ")
    for k, v in ips.items():
        print("Input{}Address = {}".format(k.upper(), v))

    print ("A records to add in infra.py:")
    print (" ")
    for subdomain in asub:
        for rec in arecords:
            subdomainlocal = rec[3]
            if subdomainlocal == subdomain:
                dstart = domain[0:3].upper()
                lastoctet = entry[1].split('.')
                ipname = dstart + lastoctet[3]
                asub[subdomain].append("route53.ExternalA('{}', 'Prod')".format(ipname))
        if len(asub[subdomain]) > 1:
            print("r53.add_a(\n\t'{}',{}\n\t,{})".format(subdomain,asub[subdomain],rec[2]))
            print (" ")
        else:
            print("r53.add_a(\n\t'{}',route53.ExternalA('{}', 'Prod')\n\t,{})".format(subdomain,ipname,rec[2]))
            print (" ")
 
    print ("MX Records to add in infra.py:")
    print (" ")
    for subdomain in mxsub:
        for rec in mxrecords:
            subdomainlocal = rec[3]
            if subdomainlocal == subdomain:
                mxsub[subdomain].append(rec[1])
    for subdomain in mxsub:
        print("r53.set_mx(\n\t'{}',{}\n\t,{})".format(subdomain,mxsub[subdomain],rec[2]))
        print (" ")    
    
    print ("TXT Records to add in infra.py:")
    print (" ")
    for subdomain in txtsub:
        for rec in txtrecords:
            subdomainlocal = rec[3]
            if subdomainlocal == subdomain:
                txtsub[subdomain].append(rec[1])
        print("r53.set_txt('{}',\n\t{}\n\t,{})".format(subdomain,txtsub[subdomain],rec[2]))
        print (" ")
    
    print ("CNAME Records to add in infra.py")
    print (" ")
    for subdomain in cnamesub:
        for rec in cnamerecords:
            subdomainlocal = rec[3]
            if subdomainlocal == subdomain:
                cnamesub[subdomain].append(rec[1])
        print("r53.add_cname('{}','{}',{})".format(subdomainlocal,rec[1],rec[2]))
        print (" ")

if __name__== "__main__":
  main()
