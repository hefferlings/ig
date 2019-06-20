from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import csv


###############################################################
# returns bool based on successful login
def login(browser,username,password):
    login_elem = browser.find_elements_by_xpath("//*[contains(text(), 'Log in')]")
    switch_acc_elem = browser.find_elements_by_xpath("//*[contains(text(), 'Switch Accounts')]")
    # if Login text is not found and no "switch accounts" option, user already logged in
    if len(login_elem) == 0 and len(switch_acc_elem) == 0:
        return True

    # Check if the first div is 'Create an Account' or 'Log In'
    login_elem = browser.find_element_by_xpath("//article/div/div/p/a[text()='Log in']")
    if login_elem is not None:
        ActionChains(browser).move_to_element(login_elem).click().perform()

    time.sleep(2)

    input_username = browser.find_elements_by_xpath("//input[@name='username']")

    ActionChains(browser).move_to_element(input_username[0]).click().send_keys(username).perform()

    time.sleep(1)

    input_password = browser.find_elements_by_xpath("//input[@name='password']")
    if not isinstance(password, str):
        password = str(password)
    ActionChains(browser).move_to_element(input_password[0]).click().send_keys(password).perform()
    input_password[0].send_keys(Keys.ENTER)
    comment = '''
    try:
        login_button = browser.find_element_by_xpath("//div/button/div[text()='Log in']")
    except NoSuchElementException:
        try:
            login_button = browser.find_element_by_xpath("//div/button[text()='Log in']")
        except NoSuchElementException:
            print "Can't find login button, aborting..."
            return False
'''
    print 'logging in...'
#    ActionChains(browser).move_to_element(login_button).click().perform()

    time.sleep(1)

    return True

###############################################################
def unfollow_from_profile(browser,username):
    print '\nnav to ' + username + '\'s profile'
    url = "https://instagram.com/" + username
    browser.get(url)
    print 'unfollowing ' + username + '...'
    time.sleep(1)

    # # check if valid profile page
    # valid_page = browser.find_elements_by_xpath("//div[contains(h2,'Sorry, this page isn\'t available')]")
    # print 'is page valid: ' + str(len(valid_page))

    # get follow/unfollow button element
    follow_elems = browser.find_elements_by_xpath("//span/button[text()='Follow']")
    follow_elems += browser.find_elements_by_xpath("//span/button[text()='Follow Back']")
    unfollow_elems = browser.find_elements_by_xpath("//span/button[text()='Following']")
    unfollow_confirm_elems = browser.find_elements_by_xpath("//div/button[text()='Unfollow']")

    if unfollow_elems:
        ActionChains(browser).move_to_element(unfollow_elems[0]).click().perform()

        # get follow/unfollow element again to check for unfollow confirm dialog
        follow_elems = browser.find_elements_by_xpath("//span/button[text()='Follow']")
        follow_elems += browser.find_elements_by_xpath("//div/button[text()='Follow']")
        follow_elems += browser.find_elements_by_xpath("//span/button[text()='Follow Back']")
        follow_elems += browser.find_elements_by_xpath("//div/button[text()='Follow Back']")
        unfollow_elems = browser.find_elements_by_xpath("//span/button[text()='Following']")
        unfollow_elems += browser.find_elements_by_xpath("//div/button[text()='Following']")
        unfollow_confirm_elems = browser.find_elements_by_xpath("//div/button[text()='Unfollow']")

        if unfollow_confirm_elems:
            ActionChains(browser).move_to_element(unfollow_confirm_elems[0]).click().perform()
            time.sleep(1)
        else:
            print 'no unfollow confirm button, skipping...'

        # get follow/unfollow element again to check for unfollow success
        follow_elems = browser.find_elements_by_xpath("//span/button[text()='Follow']")
        follow_elems += browser.find_elements_by_xpath("//div/button[text()='Follow']")
        follow_elems += browser.find_elements_by_xpath("//span/button[text()='Follow Back']")
        follow_elems += browser.find_elements_by_xpath("//div/button[text()='Follow Back']")
        unfollow_elems = browser.find_elements_by_xpath("//span/button[text()='Following']")
        unfollow_elems += browser.find_elements_by_xpath("//div/button[text()='Following']")
        unfollow_confirm_elems = browser.find_elements_by_xpath("//div/button[text()='Unfollow']")

        if follow_elems:
            print "unfollow action successful, hopefully they never find out..."
            time.sleep(1)
            return True
        else:
            return False

    else:
        print 'no unfollow button, skipping...'
        return False


    time.sleep(1)

###############################################################
def unfollow_list_from_profile(browser,list):
    successCount = 0
    totalCount = 0
    for user in list:
        didUnfollow = unfollow_from_profile(browser,user)
        if didUnfollow:
            successCount += 1
        totalCount += 1
        didUnfollow = False
        print "Unfollowed " + str(successCount) + " out of " + str(totalCount)
        if successCount == 55:
            'Getting too close to the limit, exiting...'
            # maybe just put 60min delay here so this can run overnight
            return

###############################################################
def read_helper_tools_csv(filename,save_losers=False):

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        user_list = []
        for row in csv_reader:
            if line_count == 0:
                col_names = row
                line_count += 1
            else:
                user_list.append(row)
                line_count += 1
        print('Processed ' + str(line_count) + ' lines.')

    followers_list = []
    following_list = []
    not_following_back = []

    try:
        username_row = col_names.index('username')
        followers_row = col_names.index('user_followed_by')
        following_row = col_names.index('user_follows')
    except ValueError:
        username_row = -1
        followers_row = -1
        following_row = -1

    for row in user_list:
        if following_row != -1 and followers_row != -1:
            if row[following_row] == 'TRUE':
                following_list.append(row)
            if row[followers_row] == 'TRUE':
                followers_list.append(row)
            if row[following_row] == 'TRUE' and row[followers_row] == 'FALSE':
                not_following_back.append(row[username_row])

    print '\nnum followers: ' + str(len(followers_list))
    print 'num following: ' + str(len(following_list))
    print str(len(not_following_back)) + ' users not following you back'

    return not_following_back

    save_losers = False
    if save_losers:
        print '\nwriting not_following_back-ers to csv...'
        with open('../data/not_following_back.csv', mode='w') as _file:
            _writer = csv.writer(_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in not_following_back:
                _writer.writerow([row,])

        with open('../data/not_following_back.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                print row
        print('\ndone')
