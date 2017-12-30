#! /usr/bin/env python3

"""
This is the menu for the AWS Support Toolkit
"""
import os, sys
import prepstaging, dnsreader, instance_list, dnswriter, commands.ssm, analyzelogs, sslcert

def menu():
    print ("Welcome to the AWS Support Toolkit")
    print ("1. Log Analysis")
    print ("2. Prepare Staging/Dev for Deploy")
    print ("3. DNS Reader")
    print ("4. DNS Writer")
    print ("5. SSM Toolkit")
    print ("6. List Instances")
    print ("7. Request SSL Certificate")
    print ("q. Quit")

def main():
    while True:
        menu()
        option = input ("Please select an option to continue: ")

        if option == 'q':
            break
        else:
            os.system('clear')
            dostuff(option)


def dostuff(option):
    if option == '1':
        analyzelogs.main()
    elif option == '2':
        prepstaging.main()
    elif option == '3':
        dnsreader.main()
    elif option == '4':
        dnswriter.main()
    elif option == '5':
        commands.ssm.main()
    elif option == '6':
        instance_list.main()
    elif option == '7':
        sslcert.main()
    else:
        print ("Invalid Selection, Please Try Again")



if __name__== "__main__":
  main()
