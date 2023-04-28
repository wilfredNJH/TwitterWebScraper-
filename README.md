<h1 align="center"> Wilfred Ng </h1>
<h3 align="center"> Twitter Web Scraper </h3>  

</br>

<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents"> :book: Table of Contents</h2>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project"> ➤ About The Project</a></li>
    <li><a href="#Dependencies"> ➤ Dependencies</a></li>
    <li><a href="#HowToRun"> ➤ Folder Structure</a></li>
  </ol>
</details>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- ABOUT THE PROJECT -->
<h2 id="about-the-project"> :pencil: About The Project</h2>

<p align="justify"> 
  This project implements a twitter web scraper that automates the login process and scraping of twitter cards. It stores the collected information into a .CSV file which can be used for analysis. 
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<h2 id="Dependencies"> :cactus: Dependencies</h2>

- if you're using chrome - https://chromedriver.chromium.org/downloads 
- if you're using edge - https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

```
pip install selenium
```

**Note:** 
1. the chromedriver.exe might not match your chrome's version, if it does not match, please download the appropriate chrome driver from the link above
2. the lines of code below can be commented out if you did not encounter an **additional username verification** on twitter 
```

# verification of username 
verify_username = WebDriverWait(chrome_driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))
)
verify_username.send_keys('twitterUsername')
verify_login_button = chrome_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')

# Wait for 10 seconds before clicking the login button
chrome_driver.execute_script("arguments[0].click();", verify_login_button)

```

3. Remember to change the **usernameEmail** , **password** and **twitterUsername** to your own respective login details. 

<h2 id="HowToRun"> :large_blue_diamond: How To Run</h2>

```
python TwitterScraper.py
```