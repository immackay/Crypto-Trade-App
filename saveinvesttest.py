#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:32:46 2017

@author: Ian
"""

#import math


savings = 0
investments = 0
investrate = 0.05
job = ''
wage = 0
hours = 0
salary = 0
finish = False
yearspassed = 0

def simpleCompoundInterest(principle, rate, amount):
    ret = principle*((1 + rate)**amount)
    return ret

def complexCompoundInterest(principle, rate, compound, amount):
    r = rate/compound
    t = compound*amount
    ret = principle*((1 + r)**t)
    return ret

#def repeat(amount, ):

def hourly(wage, hours):
    pass

def salary(amount):
    pass

def job():
    global job
    global wage
    global hours
    global salary
    job = input("Is your job this year wage or salary based? w/s:")
    if job in ('w', 'W'):
        wage = input("What is your hourly wage?")
        hours = input("How many hours do you work each week?")
    elif job in ('s', 'S'):

    else:
        print("Error, try again")
        job()

def invest():
    global savings
    global investments
    print("Your savings are: ${}".format(savings))
    print("Your investments total: ${}".format(investments))
    a = float(input("How much money would you like to move to investments?"))
    investments += a
    savings -= a

def finished():1
    global finish
    f = input("Are you finished? Y/n:")
    if f in ("Y", "y"):
        finish = True
    else:
        pass

def loop():
    job():
    invest()
    print(yearspassed)
    finished()
    if finish:
        return
    else:
        loop()

if __name__ == "__main__":
    savings = input("How much money do you have in savings currently?")
    investments = input("How much money do you have in investments currently?")
    investrate = (input("At what percentage do your investments grow?"))/100
    loop()
