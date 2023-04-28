from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from getpass import getpass

# good reference : https://www.scrapingbee.com/blog/web-scraping-twitter/

# for wait time 
import time 
import csv



# selenium docs - https://selenium-python.readthedocs.io/locating-elements.html

def get_tweet_data(card):
    # username , getting the first span tag after the current tag
    username = card.find_element(By.XPATH,'.//span').text 
    print("Username: " + username + "\n")
    # twitter handle 
    handle = card.find_element(By.XPATH,'.//span[contains(text(),"@")]').text 
    print("Twitter Handle: " + handle + "\n")
    # post date 
    try:
        postDate = card.find_element(By.XPATH,'.//time').get_attribute('datetime')
        print("Post Date: " + postDate + "\n")
    except NoSuchElementException:
        return
    # content of tweet 
    # comment = card.find_element(By.XPATH, './/div[2]/div[2]/div[1]').text
    # print("Comment: " + comment + "\n")
    responding = card.find_element(By.XPATH, './/div[2]/div[2]/div[2]').text
    print("Responding: " + responding + "\n")
    # retweet 
    retweets = card.find_element(By.CSS_SELECTOR,'div[data-testid="retweet"]').text
    print("Retweets: " + retweets + "\n")
    # likes 
    likes = card.find_element(By.CSS_SELECTOR,'div[data-testid="like"]').text
    print("Likes: " + likes + "\n")
    
    tweet = (username,handle,postDate,responding,retweets,likes)
    return tweet

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.add_experimental_option("detach", True)

# setting the options & going to website 
chrome_driver = webdriver.Chrome(options=chrome_options)

# open the browser and maximize the window
chrome_driver.maximize_window()

chrome_driver.get('https://twitter.com/i/flow/login')
# chrome_driver.get('https://www.reddit.com/login/')

# / = selects from root node , // = starts from current node & matches anywhere 
# looking for an input tag, with property name 
# find_element_by_xpath [deprecated] - https://stackoverflow.com/questions/72754651/attributeerror-webdriver-object-has-no-attribute-find-element-by-xpath
# https://bobbyhadz.com/blog/python-attributeerror-webdriver-object-has-no-attribute-find-element-by-id
# username = chrome_driver.find_element(By.XPATH,'/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/input')
# some issue with twitter's flow login page - https://stackoverflow.com/questions/73748693/twitter-logging-automatically-by-using-the-selenium-module-unable-to-locate-ele
username = WebDriverWait(chrome_driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))
)
username.send_keys('emailUsername@gmail.com')

## find element using xpath 
login_button = chrome_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')
chrome_driver.execute_script("arguments[0].click();", login_button)

# verification of username 
verify_username = WebDriverWait(chrome_driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))
)
verify_username.send_keys('twitterUsername')
verify_login_button = chrome_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')

# Wait for 10 seconds before clicking the login button
chrome_driver.execute_script("arguments[0].click();", verify_login_button)

# # password letmein77
# my_password = getpass()
my_password = WebDriverWait(chrome_driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="password"]'))
)
my_password.send_keys('password')

# log in button second
login_button_second = chrome_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
chrome_driver.execute_script("arguments[0].click();", login_button_second)


search_input = WebDriverWait(chrome_driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'))
)
# search_input = chrome_driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
search_input.send_keys('#tesla')
search_input.send_keys(Keys.RETURN)

latest_tab = WebDriverWait(chrome_driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a'))
    
)
chrome_driver.execute_script("arguments[0].click();", latest_tab)


# chrome_driver.execute_script('window_scrollTo(0, document.body.scrollHeight);')

# help from : https://stackoverflow.com/questions/70379706/driver-find-elements-by-xpath-divdata-testid-tweet-gives-no-output
# getting a list of cards that contains the tweet cards 
tweet_data = []
tweet_ids = set()
last_position = chrome_driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    if WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]'))):
        cards = chrome_driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

    if len(cards) > 0:
        # only care about the last 15 items 
        for card in cards[-15:]:
            data = get_tweet_data(card)
            if data:
                tweet_id = ''.join(data)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    tweet_data.append(data)
    else:
        # Print text in red
        raise NoSuchElementException('No cards were found')
    scrollAttempt = 0
    while True:
        # check scroll position
        chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(1)
        currentPosition = chrome_driver.execute_script("return window.pageYOffset;")
        if last_position == currentPosition:
            scrollAttempt += 1
            
            # end of scroll region 
            if scrollAttempt >= 3:
                scrolling = False
                break
            else:
                time.sleep(2) # attempt to scroll again 
        else:
            last_position = currentPosition
            break
        
# saving the tweet 
with open('tesla.csv','w',newline='', encoding='utf-8') as f:
    header = ['username','handle','postDate','responding','retweets','likes']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(tweet_data)



