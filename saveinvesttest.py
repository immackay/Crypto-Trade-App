#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:32:46 2017

@author: Ian
"""

#import math


savings = 0
investments = 0
finish = False

def simpleCompoundInterest(principle, rate, amount):
    ret = principle*((1 + rate)**amount)
    return ret

def complexCompoundInterest(principle, rate, compound, amount):
    r = rate/compound
    t = compound*amount
    ret = principle*((1 + r)**t)
    return ret

def repeat(amount, )

def hourly(wage, hours):
    pass
    
def salary(amount):
    pass

def job():
    pass

def invest():
    global savings
    global investments
    print("Your savings are: ${}".format(savings))
    print("Your investments total: ${}".format(investments))
    a = float(input("How much money would you like to move to investments:"))
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
    invest()
    finished()
    if finish:
        return
    else:
        loop()

if __name__ == "__main__":
    loop()
