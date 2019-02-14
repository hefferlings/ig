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
    # losers_file = raw_input("losers csv filename: ")
    losers_file = '../data/All_users_eternal_swolemates_20190212_1447.csv'
    try:
        print 'Opening: ' + losers_file
        losers_list = ig.read_helper_tools_csv(losers_file)
        losers_flag = True
    except:
        print "Invalid file, please enter a valid csv file."

username = raw_input("username: ")
password = raw_input("password: ")

# Create a new instance of Chrome driver
driver = webdriver.Chrome()


# go to ig.com
print 'nav to ig.com'
driver.get("https://instagram.com/")

# wait for page to load
time.sleep(5)

succesful_login = False
succesful_login = ig.login(driver,username,password)

if not succesful_login:
    print "Unsuccessful login, closing now."
    driver.quit()


losers_test_list = ['bretlloyd_zyia.active','fastpacept','paige.kilner','marieovchinniknov','taymair','kimberlybeard2','kenna_flores10',
'oliviachristine22','chrissylovesyoga','tanyesworkoutplan','tonishadreilinger','reelmuscle','against_the_grain_sandwiches',
'dwilding7','rachelhughesfitness','energiefitnessborough','yo.its.didi','logan.moiroux','gymsta_sam','boar_canoe']
losers_test_list_backup = ['kimchimp','danasiracuse','davidpatt0n','juanenriquecamposofficial','kimberlyshannonmurphystunts','jomarie__','hayley_brown6',
'kayla_luvs_frogs','doyoursports_fitness','sixpackqueen_','deusasmarombas','king__brother','xtreme_fitness_gyms','thecultoffitness',
'justmartathings','miss_lauren_elyse','f_kellerman','mitchccosta','trainwithalana','tomjaneredding','atomictattoossarasotasquare',
'katealcaraz','jamestjunior','gym_map','kris_leonard_','gaylewagner2671','damian_powerbuilder','kleyver_z,annikakrebeduenkel',
'livetomakehistory','britkneerox','mcvictoryinmyveins','brianna.dixonn','muscle_knight_','oatsovernight','seanmurphy.vfit']
loser_test_list_backup = ['snow.the.canaandog','neville_the_westie','gino_englishbulldog']

ig.unfollow_list_from_profile(driver,losers_test_list)

print "finished...fake close"
