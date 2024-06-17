import datetime
import logging
import re
import subprocess
from anyio import sleep
import socket
from contextlib import closing
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as BraveService
import time
import pytz
from flask import request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from supabase import create_client, Client
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import pickle
import io

import os
import psutil

process = psutil.Process(os.getpid())
# print(process.memory_percent())

dotenv_path = "../.env"
load_dotenv()

user = os.getenv("TWITTER_USER")
username = os.getenv("TWITTER_USERNAME")
passwrd = os.getenv("TWITTER_PASSWORD")
userbame2 = os.getenv("TWITTER_USERNAME2")
passwrd2 = os.getenv("TWITTER_PASSWORD2")
doubled = set()

inDb = set()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
if url is None or key is None:
    raise Exception("Environment variables for SUPABASE_URL and SUPABASE_KEY must be set.")

dbUser = "postgres"
dbPassword: str = os.getenv("DB_PASSWORD")
dbPort = "5432"
dbHost = "db.utvsxgfogcixgkztnvxo.supabase.co"
dbdDatabase = "postgres"
supabase: Client = create_client(url, key)
bucket = "pickle"
path = "cookies.pkl"

app = Flask(__name__)
cors = CORS(
    app,
    resources={
        r"/api/createList": {
            "origins": "*",
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
    supports_credentials=True,
)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
@cross_origin()
def post_example():
    return jsonify(message="POST request returned")


@app.route("/hello/<name>")
def hello_there(name):
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

inputUser = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input'
nextBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]'
followingNum = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span'
inputPass = "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input"
inputPass2 = "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input"
followingDiv = (
    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div'
)
# //*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button
followBtn = "css-18t94o4.css-1dbjc4n.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-15ysp7h.r-4wgw6l.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr"
logInBtn = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button'
user1 = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div'
listBtn = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[3]/div/a"
tweetBtn = '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a'
nameInput = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/label/div/div[2]/div/input"
descriptionBox = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/label/div/div[2]/div/textarea"
searchPeopleBox = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/form/div[1]/div/div/div/label/div[2]/div[1]/input"
textBox = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div"
search2 = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/form/div[1]/div/div/div/label/div[2]/div[1]/input'
usedSerachPeople = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/form/div[1]/div/div/div/label/div[3]/div"
setUpTweetBtn = "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a"
doneLisatBtn = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div/div/span/span"
listNextBtn = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div/div/span/span"
listBtn = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[3]/div/a"
tweetBtn = '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a'
addBtnList = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/form/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]"
descriptionBox = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/label/div/div[2]/div/textarea"
followingNum = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span'
followingDiv = (
    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div'
)
followBtn = "css-18t94o4.css-1dbjc4n.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-15ysp7h.r-4wgw6l.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr"
user1 = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div'
listBtn = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[3]/div/a"
tweetBtn = '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a'
tweetButton = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/div[4]'
tweetBox = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div[2]/div/div/article/div/div/div[2]/div[2]/div[2]/div"
tweetColumn = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div"
phoneButton='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
nextButton ='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button'

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
            "account": self.account,
            "username": self.username,
            "description": self.description,
            "followed_by": self.followed_by,
        }


length = 0
import logging

# Set the logging level for WebDriver manager to suppress logs
logging.getLogger('webdriver_manager').setLevel(logging.ERROR)
selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
# Only display possible problems
selenium_logger.setLevel(logging.ERROR)
# logging.getLogger().setLevel(logging.WARNING)
INFO = 500
logging.addLevelName(INFO,"INFO")
logg = logging.getLogger(__name__)


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
    

def load_onDriver():
    port = find_free_port()
    # service_chrome = Service(executable_path=r"/usr/bin/chromedriver")
    # service_chrome = Service(executable_path=r"C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe")
    options = Options()
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    # Add any necessary arguments
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    ###############################################Turn off or on if yu want to see the browser#######################################################
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-in-process-stack-traces")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=OFF")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--output=NUL")
    # driver = webdriver.Chrome(service=service_chrome, options=options)
    # CHROMEDRIVER_PATH=r"C:\\Program Files\\Google\\chromedriver.exe"
    try: 
        # options.binary_location = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'

        # Specify the path to your manually downloaded ChromeDriver
        path_to_chromedriver = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"  # Update this path
        service = BraveService(executable_path=path_to_chromedriver)

        service.command_line_args().append(f"--port={port}")
        driver = webdriver.Chrome(service=service, options=options)
        # service = BraveService(ChromeDriverManager(version='114.0.5735.90',path=options.binary_location).install(),options=options)
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # driver = webdriver.Chrome(options=options)
            # service=Service(ChromeDriverManager(latest_release_url="https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/win32/chromedriver-win32.zip").install()), options=options
        # )
        
        # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.207 Safari/537.36"
            },
        )
        # print("DRIVER: ",driver)
        return driver
    except Exception as e:
        logg.fatal(f"Could not load driver: {str(e)}")


def update_last_num(amt):
    try:
        supabase.table("sign").update(
            {
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "new_amount": amt,
            }
        ).eq("id", 0).execute()
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if amt:
            print("Added to Database")


def remove_at_sign(usersToAdd):
    return [user.replace("@", "") for user in usersToAdd]

every_account = {}


def get_All_Tracked():
    accounts = None
    try:
        accounts = (
            supabase.table("Tracking")
            .select("account")
            .order(column="created_at", desc=True)
            .execute()
        )
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if accounts:
            print("PostgreSQL connection is closed")
    return accounts


def get_all_accounts():
    try:
        accounts = supabase.table("Followed").select("*").execute()

        return accounts.data
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if accounts:
            print("PostgreSQL connection is closed")


def fetch_all_records(size=1000):
    all_records = []
    page = 0

    while True:
        start = page * size
        end = start + size - 1
        records = (
            supabase.table("Followed").select("account").range(start, end).execute()
        )
        if len(records.data) > 0:
            all_records.extend(records.data)
            page += 1
        else:
            break

    return all_records


def update_or_insert(account, username, description, followed_by):
    try:
        supabase.table("Followed").upsert(
            {
                "account": account,
                "username": username,
                "description": description,
                "followed_by": followed_by,
                "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ).execute()
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if account:
            print(f"Added {account} to Database")



def add_accounts_to_db(all_accounts):
    num = 0
    for account in all_accounts.values():
        username = account.username
        description = account.description
        followed_by = account.followed_by
        accounts = account.account
        num+=1
        print("accounts",accounts)
        if not accounts.startswith("@"):
            continue
        update_or_insert(accounts, username, description, followed_by)
    global length
    print("Accounts added: ",len(all_accounts),num)
   
iterator = 0


@app.route("/api/follow/<path:followList>")
def create_tweet(followList):
    print("I'm inside create_tweet()", followList)
    return f"Tweet: {followList}"

@app.after_request
def add_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response



@app.route("/api/jobs")
def jobs():
    print("I'm inside jobs()")
    jobs = scheduler.get_jobs()
    
    # Format the jobs for JSON response
    jobs_list = [{'Job': 'Running sweep','Next_run_time': str(j.next_run_time),'Last Run Time':last_run_time,'Last accounts scraped claim':last_amount_claimed,'Is Scheduler Running':scheduler.running, 'Last time taken to run': time_mintutes} for j in jobs]
    
    return jsonify(jobs_list)


@app.route("/api/test")
def test():
    return run_man()


def log_In():
    # create instance of Chrome webdriver
    supabase.storage().from_(bucket).remove(path)
    wdriver = load_onDriver()
    print("loading twitter.com.............")
    wdriver.get("https://twitter.com/login")
    time.sleep(1.5)
    # adjust the sleep time according to your internet speed
    print("sending twitter username")
    try:
        wdriver.find_element(by="xpath", value=inputUser).send_keys(user)
        # find the element next button
        # request using xpath
        # clicking on that element
        time.sleep(2)
        print("Clicking next")
        wdriver.find_element(by="xpath", value=nextBtn).click()
        # adjust the sleep time according to your internet speed
        time.sleep(2)
        # find the element where we have to
        # enter the xpath
        print("sending twitter password")
        # fill the password
        inputPass_box = wdriver.find_element(by="xpath", value=inputPass)
        print("Found input pass box")
        if inputPass_box:
            inputPass_box.send_keys(passwrd)
        else:
            print('checking the other box')
            inputPass_box = wdriver.find_element(by="xpath", value=inputPass2)
            inputPass_box.send_keys(passwrd2)
            time.sleep(3)
        # find the element login button
        # request using xpath
        # clicking on that element
        wdriver.find_element(by="xpath", value=logInBtn).click()
        time.sleep(3)

        try:
            phoneInputBox = wdriver.find_element(by="xpath", value=phoneButton)
            print("Found PHONE BUTTON")
            phoneInputBox.send_keys("7342740259")
            time.sleep(2)
            wdriver.find_element(by="xpath",value=nextButton).click()
            time.sleep(2)
        except:
            print("No phone number")
        print("Uploading pickle the cookies")
        time.sleep(2)
        upload_pickle(wdriver)
    except Exception as e:
        print("OH NOOOOOO: ",e)
        exit()
    # save_cookie_file(wdriver)
    # pickle.dump(wdriver.get_cookies(), open("cookies.pkl", "wb"))

    return wdriver


multi_acc = {}


def upload_pickle(wdriver):
    # Upload the serialized cookies
    cookies = wdriver.get_cookies()
    # Serialize the cookies into a bytes object
    serialized_cookies = pickle.dumps(cookies)
    # Open the serialized cookies as a file-like object
    file_like_object = io.BytesIO(serialized_cookies)
    # Convert the BytesIO object to bytes
    data = file_like_object.getvalue()
    response = supabase.storage().from_(bucket).upload(path, data)
    json_response = response.json()

    if "error" in json_response:
        print("Error uploading file:", json_response["error"])
    else:
        print("File uploaded successfully")


def load_pickle():
    downloaded_file = supabase.storage().from_(bucket).download(path)

    if downloaded_file is None:
        print("Error downloading file: File might not exist or access might be denied.")
        return None

    # Convert the bytes object to a file-like object
    file_like_object = io.BytesIO(downloaded_file)

    # Load the cookies from the file-like object
    cookies = pickle.load(file_like_object)

    return cookies


def read_ares_tweets(driver):
    driver.get("https://twitter.com/AresLabs_xyz")
    time.sleep(2)
    # Determine the height of the viewport
    viewport_height = driver.execute_script("return window.innerHeight")
    # Determine the height of the entire document
    document_height = driver.execute_script(
        "return document.documentElement.scrollHeight"
    )
    # Calculate the number of scrolls needed
    num_scrolls = document_height // viewport_height
    all_accounts = {}
    try:
        for _ in range(num_scrolls):
            # Scroll down to the bottom
            driver.execute_script("window.scrollBy(0, arguments[0])", viewport_height)
            time.sleep(0.5)
            elemnt = driver.find_element(By.XPATH, value=tweetColumn)
            tweets = elemnt.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            for tweet in tweets:
                if isinstance(tweet, webdriver.remote.webelement.WebElement):
                    try:
                        tweetText = tweet.text
                        tweetText = tweetText.split("\n")
                        joined_string = " ".join(tweetText)
                        start = joined_string.find("Bio:") + 4
                        end = joined_string.find("alert follower:")
                        bio = joined_string[start:end]
                        if "New project:" in joined_string or "new project" in joined_string.lower():
                            joined_string = joined_string.lower()
                            if "(follower" in joined_string:
                                acc = joined_string[
                                    joined_string.find("new project:")
                                    + 13 : joined_string.find("(follower")
                                ]
                            else:
                                acc = joined_string[
                                    joined_string.find("new project:")
                                    + 13 : joined_string.find("(")
                                ]
                            if "we33house" in acc:
                                continue
                            elif acc not in inDb:
                                account = Account(acc, "New project: " + acc, bio)
                                account.add_follower("@AresLabs_xyz")
                                all_accounts[acc] = account

                                inDb.add(acc)
                    except Exception as e:
                        continue
                else:
                    continue
    except:
        print("complete cycle")
    print("done with scraping")
    multi_acc.update(all_accounts)


def process_trackers(trackers, max_workers=10):
    cookies = load_pickle()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for tracker in trackers:
            if tracker:
                futures.append(executor.submit(worker, tracker, cookies.copy()))
        
        # Wait for all futures to complete with a timeout
        done, not_done = wait(futures, timeout=360, return_when=ALL_COMPLETED)

        # Handle any tasks that did not complete in time
        for future in not_done:
            print(f"Task did not complete: {future}")
                


def worker(tracker, cookies):
    logg.log(INFO, f"Starting to get follows for {tracker}")
    if not isinstance(cookies, list):
        print("Error: Cookies should be a list of dictionaries.")
        return

    driver = load_onDriver()
    try:
        driver.get("https://twitter.com")
        time.sleep(4)

        # Check and print each cookie before adding
        try:
            for cookie in cookies:
                if isinstance(cookie, dict):
                    driver.add_cookie(cookie)
                else:
                    print(f"Invalid cookie data: {cookie}")  # This will help identify bad cookie data
        except Exception as e:
            print(f"ISSUE ADDING COOKIE: {e}")

        get_multiple_tracker(tracker, driver)
    except Exception as e:
        print("ISSUE RUNNING MULTI", e)

    finally:
        try:
            driver.close()
            driver.quit()
        except Exception as e:
            print("Cannot quit driver: ",e)

def get_multiple_tracker(tracker, driver):
    # new driver new url
    print(f"----------------------------------HELLLLLO--{tracker}-------------------------------")

    url = f"https://twitter.com/{tracker}/following"
    driver.get(url)
    time.sleep(3)
###########################################################################
    # if is present log in uploadcookies

    try:
        driver.find_element(by="xpath", value=inputUser).send_keys(user)
        # find the element next button
        # request using xpath
        # clicking on that element
        time.sleep(2)
        print("Clicking next")
        driver.find_element(by="xpath", value=nextBtn).click()
        # adjust the sleep time according to your internet speed
        time.sleep(2)
        # find the element where we have to
        # enter the xpath
        print("sending twitter password")
        # fill the password
        inputPass_box = driver.find_element(by="xpath", value=inputPass)
        print("Found input pass box")
        if inputPass_box:
            inputPass_box.send_keys(passwrd)
        else:
            print('checking the other box')
            inputPass_box = driver.find_element(by="xpath", value=inputPass2)
            inputPass_box.send_keys(passwrd2)
            time.sleep(3)
        # find the element login button
        # request using xpath
        # clicking on that element
        driver.find_element(by="xpath", value=logInBtn).click()
        time.sleep(3)

        try:
            phoneInputBox = driver.find_element(by="xpath", value=phoneButton)
            print("Found PHONE BUTTON")
            phoneInputBox.send_keys("7342740259")
            time.sleep(2)
            driver.find_element(by="xpath",value=nextButton).click()
            time.sleep(2)
        except:
            print("No phone number")
        print("Uploading pickle the cookies")
        time.sleep(2)
        upload_pickle(driver)
        # driver.get(url)
        # time.sleep(3)
    except:
        print("No need to log in")

##########################################

    all_accounts = {}
    # Determine the height of the viewport
    viewport_height = driver.execute_script("return window.innerHeight")
    # Determine the height of the entire document
    document_height = driver.execute_script(
        "return document.documentElement.scrollHeight"
    )
    # Calculate the number of scrolls needed
    num_scrolls = document_height // viewport_height
    numberOfAccounts = 0
    try:
        for _ in range(num_scrolls):
            wait = WebDriverWait(driver, 10)
            # Scroll down to the bottom
            time.sleep(0.5)
            driver.execute_script("window.scrollBy(0, arguments[0])", viewport_height)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            # Capture the elements
            elemnt = driver.find_element(by="xpath", value=followingDiv)
            # accounts = elemnt.find_elements(By.CSS_SELECTOR, '.css-1dbjc4n.r-18u37iz')
            fullacc = elemnt.find_elements(
                By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]'
            )
            for e in fullacc:
                if isinstance(e, webdriver.remote.webelement.WebElement):
                    try:
                        usernameForAcc = e.text.split("\n", 1)[0]
                        accountName = e.text.split("\n", 2)[1]
                        numberOfAccounts = numberOfAccounts+1

                        # logg.log(INFO,f"Checking if {accountName} is in DB")
                        if (
                            accountName == ""
                            or accountName == "Follow"
                            or accountName == "Follow\n"
                            or accountName in inDb
                        ):
                            continue
                        description = e.text.split("Follow", 1)[1]
                        if (
                            description == ""
                            or description == "Follow"
                            or description == "Follow\n"
                        ):
                            inDb.add(accountName)
                            continue
                        logg.log(INFO,f"Adding {accountName} to db")
                        acc = Account(accountName, usernameForAcc, description)
                        acc.add_follower(tracker)
                        all_accounts[accountName] = acc
                        inDb.add(accountName)
                    except:
                        # logg.warning(f"Waringing for {tracker} issue: {e}")
                        # print(f"Waringing err for {tracker} issue: {e}")
                        continue
                else:
                    print("Not instance")
                    continue
    except:
        logg.log(INFO,f"complete cycle number of accts gathered: ,{len(all_accounts.values())}")
    finally:
        multi_acc.update(all_accounts)
        global IS_SEEN
        if numberOfAccounts == 0:
            IS_SEEN = False
        else:
            IS_SEEN = True
        logg.log(INFO,f"{tracker} scraped: {len(all_accounts.values())}, multi_acc {len(multi_acc.values())} total accounts seen: {numberOfAccounts}")
        logg.log(INFO,f"done with scraping: {tracker}, gathered: {len(all_accounts.values())} acounts, mulit_acc {len(multi_acc.values())}")


# def kill_chrome():
#     # Command to kill all instances of Chrome on Windows
#     try:
#         subprocess.run("taskkill /F /IM chrome.exe /T", check=True, shell=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to kill Chrome processes: {e}")

#   # As a last resort, to clean up any leftover processes


def get_chrome_pids():
    """Get a set of PIDs for all running Chrome processes."""
    chrome_pids = set()
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'chrome.exe':
            chrome_pids.add(process.info['pid'])
    return chrome_pids

def format_duration(duration_seconds):
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = int(duration_seconds % 60)

    time_components = []

    if hours > 0:
        time_components.append(f"{hours} hour{'s' if hours != 1 else ''}")

    if minutes > 0:
        time_components.append(f"{minutes} minute{'s' if minutes != 1 else ''}")

    if seconds > 0:
        time_components.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    if len(time_components) == 0:
        return "0 seconds"

    if len(time_components) == 1:
        return time_components[0]

    return ", ".join(time_components[:-1]) + f", and {time_components[-1]}"

def kill_chrome(after_pids,before_pids):
    new_pids = after_pids - before_pids
    # Kill the new Chrome instances
    for pid in new_pids:
        try:
            p = psutil.Process(pid)
            p.terminate()  # Or p.kill() if terminate does not work
        except psutil.NoSuchProcess:
            pass
IS_SEEN = True

def run_guantlet():
    run_man()
    time.sleep(4*one_hour)
    run_man()

def run_man():
    start_time = time.time()
    print("Getting pids")
    # try:
    #     before_pids = get_chrome_pids()
    # except Exception as e:
    #     print(f"Exception getting ids {e}")
    #     return
    try:
        accounts = fetch_all_records()
    except Exception as e:
        print("Failed to get records: ",e)
        return
    print("Fecthed all records")
    for account in accounts:
        inDb.add(account["account"])
    trackers = get_All_Tracked()
    tracking = []
    for tracked in trackers.data:
        # if len(tracking) >=10:
        #     continue
        tracking.append(tracked["account"])

    max_retries = 5
    attempts = 0
    wdriver = None
    worked = False
    while wdriver is None and attempts < max_retries:
        try:
            wdriver = log_In()
            worked = True
        except Exception as e:
            attempts += 1
            print(f"Login attempt {attempts} failed: {e}")
            if attempts < max_retries:
                time.sleep(15 * one_minute)
            else:
                print("Max retries reached. Exiting.")
                worked = False
                break
    if worked:
        mid_time = time.time()
        read_ares_tweets(wdriver)
        wdriver.close()
        wdriver.quit()

        holdNum = 30
        total_elements = len(tracking)
        full_groups = total_elements // holdNum
        remainder_group = 1 if total_elements % holdNum > 0 else 0

        # Calculate the total number of groups
        total_tracking = full_groups + remainder_group
        i = 1
        total_multis = 0
        while tracking:
            if not IS_SEEN:
                print("waiting")
                time.sleep(15*one_minute)
                try:
                    wwdriver = log_In()
                    wwdriver.close()
                    wwdriver.quit()
                except Exception as e:
                    print(f"cannot quit or start bc {e}")
            
            logg.info(f"Proccessing tracking batch {i} of {total_tracking}")
            print(f"Proccessing tracking batch {i} of {total_tracking}")
            i = i+1
            current_batch = tracking[:holdNum]  # Take the first holdNum trackers
            # current_batch = tracking[0:5]
            process_trackers(current_batch)  # Process these holdNum trackers
            # Update the list of trackers by removing the processed ones
            tracking = tracking[holdNum:]
            print("getting after pids....")
            # after_pids = get_chrome_pids()

            # kill_chrome(after_pids,before_pids)

            add_accounts_to_db(multi_acc)
            total_multis += len(multi_acc.values())
            multi_acc.clear()
            print("getting before pids....") 
            try:
                update_last_num(total_multis)
            except:
                print("No multi")
            # before_pids = get_chrome_pids()
            # exit()

        print("done with scraping")
        try:
            wdriver.close()
            wdriver.quit()
            print("QUIT DRIVER")
        except:
            print("Cannot quit")


       
        print("done with scraping")
        global last_run_time
        last_run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        global last_amount_claimed
        last_amount_claimed = 0
        last_amount_claimed = total_multis
        end_time = time.time()
        total_time_taken = end_time - start_time 
        global time_mintutes
        print("Time waited till start processing: ", format_duration(mid_time-start_time))
        time_mintutes = format_duration(total_time_taken)
        print("Formatted duration:", time_mintutes)
        print(f"done {total_multis}")
        return "done " + str(total_multis)
    else:
        print("could not log in")

from apscheduler.schedulers.background import BackgroundScheduler

one_minute = 60
one_hour = 60 * one_minute
twelve_hours = 12 * one_hour

def get_time_difference(now, start_time):
    # now = datetime.datetime.now().strftime("%H:%M:%S")
    # start_time = datetime.datetime.now().strftime("%H:%M:%S")
    FMT = "%H:%M:%S"
    tdelta = datetime.datetime.strptime(start_time, FMT) - datetime.datetime.strptime(now, FMT)
    return tdelta

scheduler = BackgroundScheduler()
last_run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# last_amount_claimed = 0
def start_job_at(start_time):
    # startr job at time speified as start_time
    scheduler.add_job(run_man, 'interval', hours=24, start_date=start_time)
    scheduler.start()
    print("started",datetime.datetime.now().strftime("%H:%M:%S"))

import utils

if __name__ == "__main__":
    # run_man()
    # # 10 hours and 15 minutes
    # time.sleep(10 * one_hou r + 10 * one_minute)
    # run_man()
    utils.run_panda()
    run_man()
    # test_basic_options()
    print("starting")
    # exit()
    # exit()
    # start_job_at("12:00:00")
    start_date='2024-06-16 23:00:00'
    last_amount_claimed = 0
    time_mintutes = 0
    start_job_at(start_date)
    app.run(debug=True, use_reloader=False,port=8000)
    
# dertischoenig@gmail.com : does no exist found different spelling attributed
#  wklisch@googlemail.com: 0x2b96db2c9de2dc1bb500648ea3b46e68851c7d99 : "not referred by anyone" Max Mustermann
# ellba0815@gmail.com: 0xf7596e9277ee569dd412743d687d6d57591f4109 "not referrede by anyone" NO TWITTER
# supercarsofaustria@gmail.com : 0xa79f41ee19fde0e0f988e984a1a27f53cd4b8119:"not referred by anyone" NO TWITTER
# lechnerdominik.1998@gmail.com : 0x33405ac410c8054efa18ae0943c6424c98efb385 :"not referred by anyone" NO TWITTER
# markus.bek@gmx.at: 0x6ef8174b60ea5e180a7ded7efaf21e5d228bf5e4 :"not referred by anyone" NO TWITTER
# liviants31@gmail.com: 0xd12c28bd5b44fe43313222070a11206ba3b9471a : "not referred by anyone" NO TWITTER


# peace.maker1@gmx.at: 0x1427f5d52449F1c362bE5498600634638a8aB98c : "good" Livia Habitzl


# dmiglar1@gmail.com:0xc3ec1a6c088136e8e2e7bea8384e868aa1aac6f7 : "not said but clicked" dmiglar1

# donverde11@gmail.com: 0x00C5e143b034408bbd8058AC5D320c5F01Ecbd0A : "not said but clicked" NO TWITTER

# daniel.miglar@gmx.at :0x0d063635857a51d8debb65de11619a351bec9a70 " not said but good" dxkami
# depperschmidt-roman@web.de: 0x99fe1d538ae8cc061fe028b1872402601ba10c05 "now added"
# ryueuiyeol@gmail.com :0xca63198ab2819a33501a160b34af6a1734ac64e3 :"now added"
# alex.miglar@gmail.com: 0xd1edf6ad65f3af6141c563a009ba6c812945fb0e : now added
# max.strauss@kumondo.at: 0xd5718903296323a9315c6023ce1af7e93affe25e


#0xed4c5bb5076b4f6641f83798b08ddadd4f822535
# 0xe95d41abe7091bda8e605ff6b10b228600f51a66