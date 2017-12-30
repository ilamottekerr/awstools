#! /usr/bin/env python3
from collections import defaultdict
import sys

#fn = sys.argv[1]


columns = defaultdict(list) # each value in each column is appended to a list
arecords = []
mxrecords = []
txtrecords = []
cnamerecords = []
ips = {}
asub = {}
mxsub = {}
txtsub = {}
mxs = []
txts = []
ipnamelist = []
def main():
    fn = input("Where is the file located? ")
    with open(fn) as f:
        reader = f.readlines()
        for row in reader:
            myrow = row.split()
            if len(myrow) == 1:
                domain = myrow[0]
                domainlength = len(domain)
            if len(myrow) >= 2:
                subdomain = myrow[0][:-(domainlength+1)]
                #print ("Subdomain: {}".format(subdomain))
                if myrow[3] == 'A':
                    arecords.append(myrow)
                    asub[subdomain] = []
                if myrow[3] == 'MX':
                    mxrecords.append(myrow)
                    mxsub[subdomain] = []
                if myrow[3] == 'TXT':
                    txtrecords.append(myrow)
                    txtsub[subdomain] = []
                if myrow[3] == 'CNAME':
                    cnamerecords.append(myrow)
        f.close()

    for entry in arecords:
        dstart = domain[1:4].upper()
        lastoctet = entry[4].split('.')
        ipname = dstart + lastoctet[3]
        ips[domain[1:4] + lastoctet[3]] = (entry[4])
        #print("r53.add_a(\n\t'" + entry[0][:-(domainlength+1)] + "',\n\troute53.ExternalA('" + ipname + "', 'Prod')\n\t)")
    print ("The following variables need to be set for the A records to work")
    for k, v in ips.items():
        print("Input{}Address = {}".format(k.upper(), v))
    print ("These are the required A Records")
    for subdomain in asub:
        for rec in arecords:
            subdomainlocal = rec[0][:-(domainlength+1)]
            if subdomainlocal == subdomain:
                dstart = domain[1:4].upper()
                lastoctet = rec[4].split('.')
                ipname = dstart + lastoctet[3]
                asub[subdomain].append("route53.ExternalA('{}', 'Prod')".format(ipname))
        if len(asub[subdomain]) > 1:
            print("r53.add_a(\n\t'{}',{}\n\t,{})".format(subdomain,asub[subdomain],rec[1]))
        else:
            print("r53.add_a(\n\t'{}',route53.ExternalA('{}', 'Prod')\n\t,{})".format(subdomain,ipname,rec[1]))

    print ("These are the required MX Records")
    for subdomain in mxsub:
        for rec in mxrecords:
            lengthofrec = len(rec)
            needed_spots = lengthofrec - 4
            dummyname = ""
            for i in range(needed_spots):
                dummyname += rec[i+4] + " "
            subdomainlocal = rec[0][:-(domainlength+1)]
            if subdomainlocal == subdomain:
                mxsub[subdomain].append(dummyname.strip())
    for subdomain in mxsub:
        print("r53.set_mx(\n\t'{}',{}\n\t,{})".format(subdomain,mxsub[subdomain],rec[1]))

    print ("These are the required TXT Records")
    for subdomain in txtsub:
        for rec in txtrecords:
            lengthofrec = len(rec)
            needed_spots = lengthofrec - 4
            dummyname = ""
            for i in range(needed_spots):
                dummyname += rec[i+4] + " "
            subdomainlocal = rec[0][:-(domainlength+1)]
            if subdomainlocal == subdomain:
                txtsub[subdomain].append(dummyname.strip())
        print("r53.set_txt('{}',\n\t{}\n\t,{})".format(subdomain,txtsub[subdomain],rec[1]))

    print ("These are the required CNAME Records")
    for record in cnamerecords:
        subdomainlocal = record[0][:-(domainlength+1)]
        print("r53.add_cname('{}',{},{})".format(subdomainlocal,record[4],record[1]))


if __name__== "__main__":
  main()
