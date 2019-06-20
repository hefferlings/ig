#!/usr/bin/python

# this is a selenium python script to unfollow losers

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time,sys,csv
import getpass
import custom_defs as ig

# set params

# get csv of losers
losers_flag = False
while not losers_flag:
    # losers_file = raw_input("losers csv filename: ")
    losers_file = '/home/mahonri/ig/custom_tim/data/All_users_eternal_swolemates_20190212_1447.csv'
    try:
        print 'Opening: ' + losers_file
        losers_list = ig.read_helper_tools_csv(losers_file)
################### TMP STUFF DELETE LATER ##########
        losers_list = []
        filename = '/home/mahonri/ig/custom_tim/data/new_losers.csv'
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                losers_list.append(row[0])
#####################################################
        losers_flag = True
    except Exception as e:
        print e
        print "Invalid file, please enter a valid csv file."
        sys.exit()

username = raw_input("Username: ")
password = getpass.getpass()

# Create a new instance of Chrome driver
driver = webdriver.Chrome()


# go to ig.com
print 'nav to ig.com'
driver.get("https://instagram.com/")
# wait for page to load
time.sleep(5)

succesful_login = False
username = 'eternal_swolemates'
password = 'browner7'
succesful_login = ig.login(driver,username,password)

if not succesful_login:
    print "Unsuccessful login, closing now."
    driver.quit()
    sys.exit()


losers_test_list = []
losers_test_list_backup = []
ig.unfollow_list_from_profile(driver,losers_list)

print "finished...closing now"
driver.quit()
