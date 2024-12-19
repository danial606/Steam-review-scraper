from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

driver.get("https://store.steampowered.com/login/")
while "login" in driver.current_url:
    time.sleep(60)

reviews_url = "https://steamcommunity.com/app/3231090/reviews/?browsefilter=toprated&snr=1_5_100010_"
driver.get(reviews_url)
time.sleep(5)

reviews = []
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    review_elements = driver.find_elements(By.CLASS_NAME, 'apphub_Card')
    for elem in review_elements:
        try:
            user = elem.find_element(By.CLASS_NAME, 'apphub_CardContentAuthorName').text
            review_text = elem.find_element(By.CLASS_NAME, 'apphub_CardTextContent').text
            review_entry = f'"{user}" {review_text}'
            if review_entry not in reviews:
                reviews.append(review_entry)
        except:
            continue

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

with open('steam_reviews.txt', 'w', encoding='utf-8') as file:
    file.write("\n".join(reviews))

input("enter to close")
driver.quit()