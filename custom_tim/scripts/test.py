#!/usr/bin/python

# selenium script to login to instagram
import time
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains

##############
#####Init#####
##############

# init variables
username = '3_times_a_sadie'
password = 'Aminus'
num_feed_like_attempts = 0
num_feed_likes = 0
num_hashtag_like_attempts = 0
num_hashtag_likes = 0
did_nothing = False

###################
#####Functions#####
###################

# loop that waits for page to load
def wait_and_click(driver,seconds,element):
    for i in range(seconds):
        time.sleep(1)
        try:
            click_element(driver,element)
        except:
            if i != seconds:
                print "Click failed, trying again..."
            else:
                print "Done trying, I give up :/"


# scroll down
def scroll_down(driver):
    time.sleep(1)
    # print driver.execute_script('return document.body.scrollHeight')
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    # print "scroll finished"

def click_element(browser, element, tryNum=0):
    time.sleep(1)
    print 'Click attempt'
    # There are three (maybe more) different ways to "click" an element/button.
    # 1. element.click()
    # 2. element.send_keys("\n")
    # 3. browser.execute_script("document.getElementsByClassName('" + element.get_attribute("class") + "')[0].click()")

    # I'm guessing all three have their advantages/disadvantages
    # Before committing over this code, you MUST justify your change
    # and potentially adding an 'if' statement that applies to your
    # specific case. See the following issue for more details
    # https://github.com/timgrossmann/InstaPy/issues/1232

    # explaination of the following recursive function:
    #   we will attempt to click the element given, if an error is thrown
    #   we know something is wrong (element not in view, element doesn't
    #   exist, ...). on each attempt try and move the screen around in
    #   various ways. if all else fails, programmically click the button
    #   using `execute_script` in the browser.

    try:
        # use Selenium's built in click function
        element.click()
        did_nothing = False
        print "clicked!!!"
    except:
        # click attempt failed
        # try something funky and try again

        if tryNum == 0:
            print 'Click attempt: try scrolling element into view'
            # try scrolling the element into view
            try:
                time.sleep(2)
                browser.execute_script("document.getElementsByClassName('" +  element.get_attribute("class") + "')[0].scrollIntoView({ inline: 'center' });")
            except:
                print 'Click attempt: unable to scroll to element'
        elif tryNum == 1:
            print 'Click attempt: try scrolling to the top and clicking again'
            # well, that didn't work, try scrolling to the top and then clicking again
            browser.execute_script("window.scrollTo(0,0);")
        elif tryNum == 2:
            print 'Click attempt: try scrolling to the bottom and clicking again'
            # that didn't work either, try scrolling to the bottom and then clicking again
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        else:
            print 'Click attempt: try execute_script as last resort'
            # try `execute_script` as a last resort
            # print("attempting last ditch effort for click, `execute_script`")
            try:
                time.sleep(1)
                browser.execute_script("document.getElementsByClassName('" +  element.get_attribute("class") + "')[0].click()")
                did_nothing = False
                print "clicked!!!"
            except:
                print 'skip THIS shiz'
                did_nothing = True
            return # end condition for the recursive function


        # sleep for 1 second to allow window to adjust (may or may not be needed)
        time.sleep(1)

        tryNum += 1

        # try again!
        click_element(browser, element, tryNum)


# get username and caption for a post
def get_post_description(driver):
    # Gets the description of the post's link and checks for the dont_like tags
    graphql = 'graphql' in post_page[0]
    if graphql:
        media = post_page[0]['graphql']['shortcode_media']
        is_video = media['is_video']
        user_name = media['owner']['username']
        image_text = media['edge_media_to_caption']['edges']
        image_text = image_text[0]['node']['text'] if image_text else None
    else:
        media = post_page[0]['media']
        is_video = media['is_video']
        user_name = media['owner']['username']
        image_text = media['caption']

# like posts in feed
def like_feed_posts(driver,percentage):
    scroll_down(driver)
    element_likes = driver.find_elements_by_xpath("//button/span[@aria-label='Like']")
    print "element_likes: ", element_likes
    print len(element_likes)
    while len(element_likes) > 0:
        click_element(driver,element_likes.pop(0))
        print len(element_likes),' elements left!'
    element_unlikes = driver.find_elements_by_xpath("//button/span[@aria-label='Unlike']")
    total_likes = len(element_unlikes)
    print "total_likes: ",total_likes



#################
#####Hackage#####
#################

# create a new instance of chrome driver
driver = webdriver.Chrome()
print "Opening Chrome"
# maximize window
driver.maximize_window()
print "Maximizing window"

# go to instagram website
print "Navigating to Instagram"
driver.get('https://www.instagram.com/accounts/login/')
time.sleep(1)

# login with provided username and password
element_username = driver.find_element_by_name('username')
element_username.send_keys(username)

element_password = driver.find_element_by_name('password')
element_password.send_keys(password)

element_login_button = driver.find_element_by_xpath("//form/span/button[text()='Log in']")
element_login_button.click()
print 'Logging in'

scroll_down(driver)
like_feed_posts(driver,100)
