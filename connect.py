#! /usr/bin/env python3

import os, menu
from time import sleep

def main():
    account = input("What account do you want to workon? ")
    command = "cloudtools awsh workon {}".format(account)
    response = os.system(command)
    menu.main()
if __name__== "__main__":
  main()
