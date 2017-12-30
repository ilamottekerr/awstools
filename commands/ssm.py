#! /usr/bin/env python3

"""
This is the menu for the AWS Support Toolkit
"""
import os

def ssm():
    print ("SSM Toolkit")
    print ("1. Restart Apache")
    print ("2. Restart Nginx")
    print ("3. Restart PHP-FPM")
    print ("4. Check Disk Space")
    print ("q: Quit")

def main():
    while True:
        ssm()
        option = input ("Please select an option to continue: ")

        if option == 'q':
            break
        else:
            os.system('clear')
            domorestuff(option)


def domorestuff(option):
    print (option)
    if option == '1':
        import commands.restartapache
    elif option == '2':
        import commands.restartnginx
    elif option == '3':
        import commands.restartphpfpm
    elif option == '4':
        import commands.diskspace
    else:
        print ("Invalid Selection, Please Try Again")


if __name__== "__main__":
    main()
