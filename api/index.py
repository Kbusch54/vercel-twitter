import datetime
import logging
import re
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pytz
from flask import request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from supabase import create_client, Client
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
import pickle
import io

import os
dotenv_path = '../.env'
load_dotenv(dotenv_path=dotenv_path)

user = os.getenv('TWITTER_USER')
username = os.getenv('TWITTER_USERNAME')
passwrd = os.getenv('TWITTER_PASSWORD')
userbame2 = os.getenv('TWITTER_USERNAME2')
passwrd2 = os.getenv('TWITTER_PASSWORD2')
doubled = set()

inDb = set()
url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')
dbUser='postgres'
dbPassword: str = os.getenv('DB_PASSWORD')
dbPort="5432"
dbHost = 'db.utvsxgfogcixgkztnvxo.supabase.co'
dbdDatabase='postgres'
supabase: Client = create_client(url, key)
bucket = 'pickle'
path = 'cookies.pkl'

app = Flask(__name__)
cors = CORS(app, resources={
  r"/api/createList": {
    "origins": "*",
    "allow_headers": [
      "Content-Type", 
      "Authorization"
    ]
}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route("/")
@cross_origin()
def post_example():
    return jsonify(message="POST request returned")
@app.route("/hello/<name>")
def hello_there(name):
    print("I'm inside hello_there()",name)
    now = datetime.datetime.now()
    formatted_now = now.strftime("%a, %d %b, %y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content
inputUser = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'

nextBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
followingNum ='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span'
inputPass ='/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
followingDiv = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div'
followBtn = 'css-18t94o4.css-1dbjc4n.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-15ysp7h.r-4wgw6l.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr'
logInBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div'
user1 = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div'
listBtn ='/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[3]/div/a'
nextBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
logInBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div'
tweetBtn ='//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a'
nameInput='/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/label/div/div[2]/div/input'
descriptionBox = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/label/div/div[2]/div/textarea'
searchPeopleBox = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/form/div[1]/div/div/div/label/div[2]/div[1]/input'
textBox = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div'
search2 = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/form/div[1]/div/div/div/label/div[2]/div[1]/input'
usedSerachPeople = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/form/div[1]/div/div/div/label/div[3]/div'
setUpTweetBtn = '/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a'
doneLisatBtn="/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div/div/span/span"
listNextBtn = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div/div/span/span'
listBtn ='/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[3]/div/a'
nextBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
logInBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div'
tweetBtn ='//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a'
addBtnList = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/form/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]'
descriptionBox = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/label/div/div[2]/div/textarea'
nextBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
followingNum ='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span'
followingDiv = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div'
followBtn = 'css-18t94o4.css-1dbjc4n.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-15ysp7h.r-4wgw6l.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr'
logInBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div'
user1 = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div'
listBtn ='/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[3]/div/a'
nextBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
logInBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div'
tweetBtn ='//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a'
tweetButton = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/div[4]'
class Account:
    def __init__(self, account, username, description):
        self.account = account
        self.username = username
        self.description = description
        self.followed_by = []

    def add_follower(self, follower):
        if follower not in self.followed_by:
            self.followed_by.append(follower)

    def get_info(self):
        return {
            'account': self.account,
            'username': self.username,
            'description': self.description,
            'followed_by': self.followed_by
        }
length = 0
def load_onDriver():
    service_chrome = Service(executable_path=r'/usr/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')  
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-software-rasterizer')
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager(version=r'/usr/bin/chromedriver').install()), options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome(service=service_chrome, options=options)
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36'})
    return driver
def load_chrome_driver():
    global driver
    service_chrome = Service(executable_path=r'/usr/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')  
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-software-rasterizer')
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager(version=r'/usr/bin/chromedriver').install()), options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver = webdriver.Chrome(service=service_chrome, options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36'})
def  update_last_num(amt):
    try:
        supabase.table('sign').update({
            'last_updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'new_amount': amt
        }).eq('id', 0).execute()
    except (Exception) as error:
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(amt):
            print("Added to Database") 
def remove_at_sign(usersToAdd):
    return [user.replace("@", "") for user in usersToAdd]
def logIn_Credentials(cred_user,cred_password):
    # create instance of Chrome webdriver
    load_chrome_driver() 
    driver.get("https://twitter.com/login")
        # adjust the sleep time according to your internet speed
    time.sleep(2)
    # find the element where we have to 
    # enter the xpath
    # driver.find_element.__getattribute__
    # fill the number or mail
    driver.find_element(
        by='xpath', value=inputUser).send_keys(cred_user)
    # find the element next button 
    # request using xpath 
    # clicking on that element 
    driver.find_element(
        by='xpath',
        value=nextBtn).click()

    # adjust the sleep time according to your internet speed
    time.sleep(2)

    # find the element where we have to 
    # enter the xpath
    # fill the password
    driver.find_element(
        by='xpath',value=inputPass).send_keys(cred_password)
    # find the element login button
    # request using xpath
    # clicking on that element
    driver.find_element(by='xpath',value=logInBtn).click()
    # adjust the sleep time according to your internet speed
    time.sleep(2)

    driver.find_element(by='xpath',value=tweetBtn).click()
    time.sleep(2)
    return driver

def logIn():
    # create instance of Chrome webdriver
    load_chrome_driver()
    driver.get("https://twitter.com/login")
        # adjust the sleep time according to your internet speed
    time.sleep(2)
    # find the element where we have to 
    # enter the xpath
    # driver.find_element.__getattribute__
    # fill the number or mail
    driver.find_element(
        by='xpath', value=inputUser).send_keys(user)
    # find the element next button 
    # request using xpath 
    # clicking on that element 
    time.sleep(1)
    driver.find_element(
        by='xpath',
        value=nextBtn).click()
    # adjust the sleep time according to your internet speed
    time.sleep(2)

    # find the element where we have to 
    # enter the xpath
    # fill the password
    driver.find_element(
        by='xpath',value=inputPass).send_keys(passwrd)
    # find the element login button
    # request using xpath
    # clicking on that element
    driver.find_element(by='xpath',value=logInBtn).click()
 
    # adjust the sleep time according to your internet speed
def tweetThis(tweet):
    twitter_log_in()
    time.sleep(2)
    driver.get("https://twitter.com/compose/tweet")
    time.sleep(2)
    driver.find_element(by='xpath',value=textBox).send_keys(tweet)
    time.sleep(2)
    driver.find_element(by='xpath',value=tweetButton).click()
    driver.quit()
def followList(list):
    logIn()
    for user in list:
        driver.get("https://twitter.com/"+user)
        time.sleep(2)
        followBtn = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div/div/div'
        driver.find_element(by='xpath',value=followBtn).click()
        time.sleep(2)
def twitter_log_in():
    # create instance of Chrome webdriver
    load_chrome_driver()  # or driver = load_chrome_driver("")
    driver.get("https://twitter.com/login")
        # adjust the sleep time according to your internet speed
    time.sleep(2)
    driver.find_element(
        by='xpath', value=inputUser).send_keys(user)
    # find the element next button 
    # request using xpath 
    # clicking on that element 
    driver.find_element(
        by='xpath',
        value=nextBtn).click()

    # adjust the sleep time according to your internet speed
    time.sleep(2)

    # find the element where we have to 
    # enter the xpath
    # fill the password
    driver.find_element(
        by='xpath',value=inputPass).send_keys(passwrd)
    # find the element login button
    # request using xpath
    # clicking on that element
    driver.find_element(by='xpath',value=logInBtn).click()
    # adjust the sleep time according to your internet speed
    return driver
every_account = {}  
def start_process():
    accounts = get_all_accounts()
    global length
    for account in accounts:
        # acc = Account(account['account'], account['username'], account['description'])
        # acc.followed_by = account['followed_by']
        # all_accounts[account['account']] = acc
        # doubled.add(account['account'])
        inDb.add(account['account'])
    # length = len(all_accounts)
    print('accounts length')
    print(len(accounts))
    trackers = get_All_Tracked()
    tracking = []
    print(trackers)
    
    
    for tracked in trackers.data:
        tracking.append(tracked['account'])
        if(len(tracked['account']) == 0):
            print('No accounts to track')
            exit()
    twitter_log_in()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(scrape_and_push_data, tracking)
    # for tracker in tracking:
    #     scrape_and_push_data(tracker)
    print('done with scraping')
    print(len(every_account))
    add_accounts_to_db(every_account)
    driver.quit()
    print('done')
def scrape_and_push_data(tracker):
    print('starting to get follows for '+tracker)
    get_following(tracker)
def get_All_Tracked():
    accounts = None
    try:
        accounts = supabase.table('Tracking').select("account").order(column='created_at',desc=True).execute()
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if accounts:
            print("PostgreSQL connection is closed")
    return accounts
def get_all_accounts():
    try:
        accounts = supabase.table('Followed').select("*").execute()
        
        return accounts.data
    except (Exception) as error:
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(accounts):
            print("PostgreSQL connection is closed")
def update_or_insert(account, username, description, followed_by):
    try:
        supabase.table('Followed').upsert({
            'account': account,
            'username': username,
            'description': description,
            'followed_by': followed_by,
            'updated_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }).execute()
    except (Exception) as error:
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(account):
            print("Added to Database")

def twitter_log_in():
    # create instance of Chrome webdriver
    load_chrome_driver()
    driver.get("https://twitter.com/login")
        # adjust the sleep time according to your internet speed
    time.sleep(2)
    # find the element where we have to 
    # enter the xpath
    # driver.find_element.__getattribute__
    # fill the number or mail
    driver.find_element(
        by='xpath', value=inputUser).send_keys(user)
    # find the element next button 
    # request using xpath 
    # clicking on that element 
    driver.find_element(
        by='xpath',
        value=nextBtn).click()

    # adjust the sleep time according to your internet speed
    time.sleep(2)

    # find the element where we have to 
    # enter the xpath
    # fill the password
    driver.find_element(
        by='xpath',value=inputPass).send_keys(passwrd)
    # find the element login button
    # request using xpath
    # clicking on that element
    driver.find_element(by='xpath',value=logInBtn).click()
    # adjust the sleep time according to your internet speed
    time.sleep(2)
    return driver

    split_record = record.split("@")
    
    if len(split_record) < 3:  
        print("There is no second '@' account in this record.")
        return "@" + split_record[1]
    
    # Add '@' back to the front
    return "@" + split_record[2][split_record[2]:split_record[2].find('Follow')-1]
def get_following(tracker):
        # new driver new url
        time.sleep(2)
        url = f"https://twitter.com/{tracker}/following"
        driver.get(url)
        time.sleep(2)
        all_accounts = {}
        # Determine the height of the viewport
        viewport_height = driver.execute_script("return window.innerHeight")
        # Determine the height of the entire document
        document_height = driver.execute_script("return document.documentElement.scrollHeight")
        # Calculate the number of scrolls needed
        num_scrolls = document_height // viewport_height
        seen = set()
        try:
            for _ in range(num_scrolls):
                # Scroll down to the bottom
                driver.execute_script("window.scrollBy(0, arguments[0])", viewport_height)
                time.sleep(0.5)
                # Capture the elements
                elemnt = driver.find_element(
                by='xpath',
                value=followingDiv
                )
                # accounts = elemnt.find_elements(By.CSS_SELECTOR, '.css-1dbjc4n.r-18u37iz')
                fullacc = elemnt.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
                for e in fullacc:
                    if isinstance(e, webdriver.remote.webelement.WebElement):
                        try:
                            usernameForAcc = e.text[0:e.text.find('\n')]
                            accountName = e.text[e.text.find(usernameForAcc)+1:e.text.find('Follow')-1].split('\n')[1]
                            if accountName in seen or accountName == '' or accountName == 'Follow' or accountName == 'Follow\n' or accountName in inDb:
                                continue
                            description = e.text[e.text.find('Follow'):].replace('Follow\n','',1)
                            if description == '' or description == 'Follow' or description == 'Follow\n':
                                seen.add(accountName)
                                continue
                            acc = Account(accountName, usernameForAcc, description)
                            acc.add_follower(tracker)
                            all_accounts[accountName] = acc
                            seen.add(accountName)
                        except Exception as e:
                            continue  
                    else:
                        continue
        except:
            print('complete cycle')
        every_account.update(all_accounts)
def add_accounts_to_db(all_accounts):
    for account in all_accounts.values():
        username = account.username
        description = account.description
        followed_by = account.followed_by
        accounts = account.account
        update_or_insert(accounts, username, description, followed_by)
    global length
    print(len(all_accounts))
    update_last_num(len(all_accounts))

def add_list(usersToAdd):
    twitter_log_in()
    time.sleep(2)
    driver.get("https://twitter.com/i/lists/create")
    eastern = pytz.timezone('US/Eastern')
    eastern_time = datetime.datetime.now(eastern)
    # Format the time in 'HH:MM AM/PM' format
    hour_am_pm = eastern_time.strftime('%I:%M %p')
    time.sleep(4)
    driver.find_element(by=By.NAME,value='name').send_keys('Joes list '+datetime.datetime.now().strftime("%m-%d ")+hour_am_pm)
    driver.find_element(by=By.TAG_NAME,value='textarea').send_keys('Twitter list to follow for joe '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    time.sleep(2)
    print('all ready to go')
    nextBtnC = driver.find_element(by=By.XPATH,value=listNextBtn)
    driver.execute_script("arguments[0].click();", nextBtnC)
    print('all ready to go clicked next')
    print(usersToAdd)
    for users in usersToAdd:
        print(users)
        time.sleep(2)
        driver.find_element(by='xpath', value=searchPeopleBox).send_keys(users)
        time.sleep(3)
        try:
            addMe = driver.find_element(by=By.XPATH, value=addBtnList)
            if addMe.is_displayed():
                print('og method')
                driver.execute_script("arguments[0].click();", addMe)
            else:
                print('other method')
                driver.find_element(by=By.LINK_TEXT, value='Add').click()
        except:
            print('not found')
        time.sleep(3)
        driver.find_element(by='xpath', value=usedSerachPeople).click()
    driver.quit() 
iterator = 0
@app.route("/api/tweets/<path:tweetToSend>")
def tweets(tweetToSend):
    tweetThis(tweetToSend)
    return f'Tweeted: {tweetToSend}'
@app.route("/api/start")
def start():
    start_process()
    return 'done'
logging.getLogger('flask_cors').level = logging.DEBUG
@app.route("/api/logIn")
def logIn_yes():
    logIn()
    driver.quit()
    return 'logged in'
@app.route("/api/follow/<path:followList>")
def create_tweet(followList):
    print("I'm inside create_tweet()",followList)
    return f'Tweet: {followList}'
@app.route("/api/createList", methods=["POST"])
@cross_origin()
def create_list():
    data = request.json # 'request' is part of the flask module
    usersToAdd = remove_at_sign(data)
    add_list(usersToAdd)
    return {"success": True}, 200
    
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

iterator =0
@app.route("/api/test")
def test():
    wdriver = log_In()
    time.sleep(2)
    # trackers = get_All_Tracked()
    # tracking = []
    # for tracked in trackers.data:
    #     tracking.append(tracked['account'])
    #     if(len(tracked['account']) == 0):
    #         print('No accounts to track')
    #         exit()
    tracking = ['elonmusk']
    process_trackers(tracking,wdriver)
    return 'done ' + str(len(multi_acc))
def log_In():
    # create instance of Chrome webdriver
    supabase.storage.from_(bucket).remove(path)
    wdriver = load_onDriver()
    wdriver.get("https://twitter.com/login")
        # adjust the sleep time according to your internet speed
    time.sleep(2)
    # find the element where we have to 
    # enter the xpath
    # wdriver.find_element.__getattribute__
    # fill the number or mail
    wdriver.find_element(
        by='xpath', value=inputUser).send_keys(user)
    # find the element next button 
    # request using xpath 
    # clicking on that element 
    time.sleep(1)
    wdriver.find_element(
        by='xpath',
        value=nextBtn).click()
    # adjust the sleep time according to your internet speed
    time.sleep(2)

    # find the element where we have to 
    # enter the xpath
    # fill the password
    wdriver.find_element(
        by='xpath',value=inputPass).send_keys(passwrd)
    # find the element login button
    # request using xpath
    # clicking on that element
    wdriver.find_element(by='xpath',value=logInBtn).click()
    time.sleep(2)
    upload_pickle(wdriver)
    # save_cookie_file(wdriver)
    # pickle.dump(wdriver.get_cookies(), open("cookies.pkl", "wb"))

    return wdriver
 

multi_acc={}
def upload_pickle(wdriver):
    # Upload the serialized cookies
    cookies = wdriver.get_cookies()
    # Serialize the cookies into a bytes object
    serialized_cookies = pickle.dumps(cookies)
    # Open the serialized cookies as a file-like object
    file_like_object = io.BytesIO(serialized_cookies)
    # Convert the BytesIO object to bytes
    data = file_like_object.getvalue()
    response = supabase.storage.from_(bucket).upload(path, data)
    json_response = response.json()

    if 'error' in json_response:
        print('Error uploading file:', json_response['error'])
    else:
        print('File uploaded successfully')

def load_pickle():
    downloaded_file = supabase.storage.from_(bucket).download(path)

    if downloaded_file is None:
        print('Error downloading file: File might not exist or access might be denied.')
        return None

    # Convert the bytes object to a file-like object
    file_like_object = io.BytesIO(downloaded_file)

    # Load the cookies from the file-like object
    cookies = pickle.load(file_like_object)

    return cookies

def process_trackers(trackers,wdriver, max_workers=5):
    cookies = load_pickle()
    # cookies = pickle.load(open("cookies.pkl", "rb"))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for tracker in trackers:
            driver = load_onDriver()
            driver.get("https://twitter.com/")
            for cookie in cookies:
                driver.add_cookie(cookie)
            executor.submit(get_multiple_tracker, tracker,driver)
    wdriver.quit()
def get_multiple_tracker(tracker,driver):
        # new driver new url
        time.sleep(2)
        url = f"https://twitter.com/{tracker}/following"
        driver.get(url)
        time.sleep(2)
        all_accounts = {}
        # Determine the height of the viewport
        viewport_height = driver.execute_script("return window.innerHeight")
        # Determine the height of the entire document
        document_height = driver.execute_script("return document.documentElement.scrollHeight")
        # Calculate the number of scrolls needed
        num_scrolls = document_height // viewport_height
        seen = set()
        try:
            for _ in range(num_scrolls):
                # Scroll down to the bottom
                driver.execute_script("window.scrollBy(0, arguments[0])", viewport_height)
                time.sleep(0.5)
                # Capture the elements
                elemnt = driver.find_element(
                by='xpath',
                value=followingDiv
                )
                # accounts = elemnt.find_elements(By.CSS_SELECTOR, '.css-1dbjc4n.r-18u37iz')
                fullacc = elemnt.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
                for e in fullacc:
                    if isinstance(e, webdriver.remote.webelement.WebElement):
                        try:
                            usernameForAcc = e.text[0:e.text.find('\n')]
                            accountName = e.text[e.text.find(usernameForAcc)+1:e.text.find('Follow')-1].split('\n')[1]
                            if accountName in seen or accountName == '' or accountName == 'Follow' or accountName == 'Follow\n' or accountName in inDb:
                                continue
                            description = e.text[e.text.find('Follow'):].replace('Follow\n','',1)
                            if description == '' or description == 'Follow' or description == 'Follow\n':
                                seen.add(accountName)
                                continue
                            acc = Account(accountName, usernameForAcc, description)
                            acc.add_follower(tracker)
                            all_accounts[accountName] = acc
                            seen.add(accountName)
                        except Exception as e:
                            continue  
                    else:
                        continue
        except:
            print('complete cycle')
        driver.quit()
        multi_acc.update(all_accounts)
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False )