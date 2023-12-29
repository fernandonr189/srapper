from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

path = '/home/fernando/Web_scraping/photo/'
url = 'https://www.reddit.com/r/Nudes/'

# enable the headless mode
options = Options()
options.add_argument('--headless')
# options.add_experimental_option("detach", True)

# initialize a web driver to control Chrome
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)
# maxime the controlled browser window
driver.fullscreen_window()
driver.get('https://www.reddit.com/login/')
driver.implicitly_wait(5)
driver.find_element(by=By.ID, value="loginUsername").send_keys("fernando_spider")
driver.find_element(by=By.ID, value="loginPassword").send_keys("Enero2023!.")
driver.find_element(by=By.XPATH, value="/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button").click()
time.sleep(5)
driver.implicitly_wait(5)
driver.get(url)
driver.implicitly_wait(5)

post = driver.find_element(by=By.XPATH, value='//*[@id="AppRouter-main-content"]/div/div/div[2]/div[4]/div[1]/div[5]/div[2]')

counter = 0

def downloadImages(initialPost):
    post = initialPost
    limitExceeded = False
    repeatedPosts = 0
    while(not limitExceeded):
        title = post.find_element(by=By.TAG_NAME, value='h3').text
        desired_y = (post.size['height'] / 2) + post.location['y']
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        container = post.find_element(by=By.CSS_SELECTOR, value='[data-testid="post-container"]')
        if container.size['height'] > 500:
            try:
                img = post.find_element(by=By.CSS_SELECTOR, value='[alt="Post image"]')
                filename = title[0:30] + ".png"
                if(os.path.exists(path + filename)):
                    print("Error: " + filename + " -> already exists" + "(" + str(repeatedPosts + 1) + ")")
                    repeatedPosts += 1
                else:
                    img.screenshot(path + filename)
                    print("Success: " + filename + " -> Downloaded" + "(" + str(counter) + ")")
                    counter += 1
                    repeatedPosts = 0
                time.sleep(1)
            except:
                print("Error: " + title + " -> Not an image")
        try:
            next_sibling = post.find_element(By.XPATH, "following-sibling::*[1]")
        except:
            print("------------------------- Scroll limit Exceeded! -------------------------")
            limitExceeded = True
        post = next_sibling
        if(repeatedPosts == 10):
            print("------------------------- Too soon, no new posts! -------------------------")
            limitExceeded = True


ordinal = 1

def switchUrl(ord):
    if(ord == 1):
        url = 'https://www.reddit.com/r/Nudes/hot/'
        driver.get(url)
    elif(ord == 2):
        url = 'https://www.reddit.com/r/Nudes/new/'
        driver.get(url)
    elif(ord == 3):
        url = 'https://www.reddit.com/r/Nudes/top/?t=day'
        driver.get(url)


while(True):
    downloadImages(post)
    time.sleep(5)
    print("----------------------- Delay time completed, resuming -----------------------")

    if(ordinal == 3):
        ordinal = 1
    else:
        ordinal += 1
    switchUrl(ordinal)

    driver.implicitly_wait(15)
    time.sleep(15)
    post = driver.find_element(by=By.XPATH, value='//*[@id="AppRouter-main-content"]/div/div/div[2]/div[4]/div[1]/div[5]/div[2]')