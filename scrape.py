from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

def steam_login(driver):
    login_url = "https://store.steampowered.com/login/"
    driver.get(login_url)    
    while "login" in driver.current_url:
        print("login")
        time.sleep(5)
    print("Login success")

def extract_appid_from_link(steamdb_link):
        app_id = steamdb_link.split('/app/')[1].split('/')[0]
        if app_id.isdigit():
            return app_id

def scrape_reviews_from_page(game_id, driver):
    url = f"https://steamcommunity.com/app/{game_id}/reviews/?browsefilter=toprated"
    driver.get(url)
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

    return reviews

def load_existing_reviews(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(file.read().splitlines())
    return set()

def save_reviews_to_file(reviews, file_path):
    existing_reviews = load_existing_reviews(file_path)
    new_reviews = [review for review in reviews if review not in existing_reviews]
    if new_reviews:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write("\n".join(new_reviews) + "\n")
        print(f"Added {len(new_reviews)} new reviews to {file_path}.")
    else:
        print(f"No new reviews to add to {file_path}.")

if __name__ == "__main__":
    steamdb_links = [
        "https://steamdb.info/app/12345/charts/"
    ]
    driver = webdriver.Chrome()
    
    steam_login(driver)

    for steamdb_link in steamdb_links:
            app_id = extract_appid_from_link(steamdb_link)
            print(f"Extracted appID: {app_id}")
            print(f"Scraping reviews for appID: {app_id}")
            reviews = scrape_reviews_from_page(app_id, driver)
            reviews_output_file = f'steam_reviews_{app_id}.txt'
            save_reviews_to_file(reviews, reviews_output_file)
    driver.quit()