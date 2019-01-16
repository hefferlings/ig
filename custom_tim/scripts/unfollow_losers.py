#!/usr/bin/python

# this is a selenium python script to unfollow losers

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time,sys
import custom_defs as ig

# set params

# get csv of losers
losers_flag = False
while not losers_flag:
    losers_file = raw_input("losers csv filename: ")
    try:
        print 'fake open: ' + losers_file
        #open file here
        losers_flag = True
    except:
        print "Invalid file, please enter a valid csv file."


# Create a new instance of Chrome driver
driver = webdriver.Chrome()


# go to ig.com
print 'nav to ig.com'
driver.get("https://instagram.com/")

# wait for page to load
time.sleep(5)

succesful_login = False
succesful_login = ig.login(driver,'3_times_a_sadie','Aminus')

if not succesful_login:
    try:
        print driver.title
        print "Finished, closing now."

    finally:
        driver.quit()
