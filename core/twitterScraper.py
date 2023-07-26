from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from getpass import getpass

# good reference : https://www.scrapingbee.com/blog/web-scraping-twitter/

# for wait time 
import time 
import csv

# selenium docs - https://selenium-python.readthedocs.io/locating-elements.html
class TwitterScraper():
    def __init__(self,pEmail,pPassword,pUsername,pTag, pIsUsernameVerChecked, pBrowserOptions):

        if pBrowserOptions == 1: 
            chrome_options = Options()
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_experimental_option("detach", True)
            self.web_driver = webdriver.Chrome(options=chrome_options)
        elif pBrowserOptions == 2:
            edge_options = EdgeOptions()
            edge_options.add_argument('--log-level=3')
            edge_options.add_experimental_option("detach", True)
            self.web_driver = webdriver.Edge(options=edge_options)

        # open the browser and maximize the window
        self.web_driver.maximize_window()

        self.web_driver.get('https://twitter.com/i/flow/login')

        # / = selects from root node , // = starts from current node & matches anywhere 
        # looking for an input tag, with property name 
        # find_element_by_xpath [deprecated] - https://stackoverflow.com/questions/72754651/attributeerror-webdriver-object-has-no-attribute-find-element-by-xpath
        # https://bobbyhadz.com/blog/python-attributeerror-webdriver-object-has-no-attribute-find-element-by-id
        # username = web_driver.find_element(By.XPATH,'/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/input')
        # some issue with twitter's flow login page - https://stackoverflow.com/questions/73748693/twitter-logging-automatically-by-using-the-selenium-module-unable-to-locate-ele
        username = WebDriverWait(self.web_driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))
        )
        username.send_keys(pEmail)

        ## find element using xpath 
        login_button = self.web_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')
        self.web_driver.execute_script("arguments[0].click();", login_button)
        if pIsUsernameVerChecked == True:
            # verification of username 
            verify_username = WebDriverWait(self.web_driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))
            )
            verify_username.send_keys(pUsername)
            verify_login_button = self.web_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')

            # Wait for 10 seconds before clicking the login button
            self.web_driver.execute_script("arguments[0].click();", verify_login_button)

        # my_password = getpass()
        my_password = WebDriverWait(self.web_driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="password"]'))
        )
        my_password.send_keys(pPassword)

        # log in button second
        login_button_second = self.web_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
        self.web_driver.execute_script("arguments[0].click();", login_button_second)


        search_input = WebDriverWait(self.web_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'))
        )
        # search_input = web_driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
        search_input.send_keys(pTag)
        search_input.send_keys(Keys.RETURN)
        
        self.tag = pTag

        latest_tab = WebDriverWait(self.web_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a'))
            
        )
        self.web_driver.execute_script("arguments[0].click();", latest_tab)

    def get_tweet_data(self,card):
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

    def scrape_data(self,pIterations):
        # web_driver.execute_script('window_scrollTo(0, document.body.scrollHeight);')

        # help from : https://stackoverflow.com/questions/70379706/driver-find-elements-by-xpath-divdata-testid-tweet-gives-no-output
        # getting a list of cards that contains the tweet cards 
        self.tweet_data = []
        self.tweet_ids = set()
        self.last_position = self.web_driver.execute_script("return window.pageYOffset;")
        self.scrolling = True
        self.currentIterations = 0

        while self.scrolling == True:
            
            if WebDriverWait(self.web_driver, 10).until(EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]'))):
                self.cards = self.web_driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

            if len(self.cards) > 0:
                # only care about the last 15 items 
                for card in self.cards[-15:]:
                    data = self.get_tweet_data(card)
                    if data:
                        tweet_id = ''.join(data)
                        if tweet_id not in self.tweet_ids:
                            self.tweet_ids.add(tweet_id)
                            self.tweet_data.append(data)
                            if self.currentIterations >= pIterations:
                                self.scrolling = False
                                self.save_data()
                                return
                            self.currentIterations = self.currentIterations + 1
            else:
                # Print text in red
                raise NoSuchElementException('No cards were found')
            scrollAttempt = 0
            while True:
                # check scroll position
                self.web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                time.sleep(1)
                self.currentPosition = self.web_driver.execute_script("return window.pageYOffset;")
                if self.last_position == self.currentPosition:
                    scrollAttempt += 1
                    
                    # end of scroll region 
                    if scrollAttempt >= 3:
                        self.scrolling = False
                        break
                    else:
                        time.sleep(2) # attempt to scroll again 
                else:
                    self.last_position = self.currentPosition
                    break   
                
        self.save_data()
         
    def save_data(self):    
        # saving the tweet 
        with open(self.tag + '.csv','w',newline='', encoding='utf-8') as f:
            header = ['username','handle','postDate','responding','retweets','likes']
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(self.tweet_data)



    



