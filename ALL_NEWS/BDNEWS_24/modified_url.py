import json
import time
import urllib.parse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


def scrape_links(output_file_name, urls_to_scrape):
    # Configure ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-webgl")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--use-gl=swiftshader")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-accelerated-2d-canvas")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")
    chrome_options.add_argument("--disable-3d-apis")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/116.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    def get_news_type(url):
        if 'politics' in url:
            return ['politics', 'general']
        elif 'business' in url:
            return ['economics', 'business']
        elif 'economy' in url:
            return ['economics', 'economy']
        elif 'stocks' in url:
            return ['economics', 'stocks']
        elif 'topic/ঢাকা' in url:
            return ['national', 'capital-city']
        elif 'topic/চট্টগ্রাম' in url:
            return ['national', 'chittagong']
        elif 'topic/রাজশাহী' in url:
            return ['national', 'rajshahi']
        elif 'topic/খুলনা' in url:
            return ['national', 'khulna']
        elif 'topic/সিলেট' in url:
            return ['national', 'sylhet']
        elif 'topic/বরিশাল' in url:
            return ['national', 'barisal']
        
        else:
            return ['others', 'others']

    def scroll_down():
        driver.execute_script(f"window.scrollBy(0, 600);")
        time.sleep(1)

    def click_see_more_button(news_type, news_subcategory):
        count = 0
        max_scroll_attempts = 10
        scroll_attempts = 0
        all_links = set()

        while scroll_attempts < max_scroll_attempts:
            try:
                wait = WebDriverWait(driver, 5)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/main/section[4]/div/div/div[2]/div[2]/div/div/a | '
                               '/html/body/main/section/div[2]/div/div[1]/div[3]/div/div/a')
                ))
                see_more_button.click()
                count += 1
                print(f"Clicked 'See More' button {count} time(s).")
                time.sleep(1)
                scroll_attempts = 0

                if count % 200 == 0:
                    print(f"Processing links after {count} clicks...")
                    links_data = extract_links()
                    for link in links_data:
                        all_links.add((link, news_type, news_subcategory))
                    save_links_to_json(all_links, output_file_name)
                    all_links.clear()

            except TimeoutException:
                scroll_down()
                scroll_attempts += 1
                print(f"'See More' button not found. Scrolling attempt {scroll_attempts}.")
                scroll_height = driver.execute_script("return document.body.scrollHeight;")
                current_scroll_position = driver.execute_script("return window.pageYOffset;")
                if current_scroll_position + 400 >= scroll_height:
                    print("Reached the end of the page. No more content to load.")
                    break
            except ElementClickInterceptedException:
                print("Click intercepted. Retrying...")
                scroll_down()
                time.sleep(1)

        links_data = extract_links()
        for link in links_data:
            all_links.add((link, news_type, news_subcategory))
        save_links_to_json(all_links, output_file_name)

    def extract_links():
        links = set()
        paths = ['/html/body/main/section[4]/div/div/div[2]/div[1]/div/div',
                 '/html/body/main/section[2]/div/div/div/div/div/div/div',
                 '/html/body/main/section/div[2]/div/div[1]/div[1]/div/div']
        for path in paths:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, path))
                )
                card_elements = driver.find_elements(By.XPATH, path)
                print(f"Found {len(card_elements)} elements for path: {path}")

                for card in card_elements:
                    try:
                        link_element = card.find_element(By.TAG_NAME, "a")
                        link = link_element.get_attribute("href")
                        if link:
                            links.add(link)
                    except Exception as e:
                        print(f"Error extracting link: {e}")
            except Exception as e:
                print(f"Error extracting links for path {path}: {e}")
        return links

    def save_links_to_json(all_links, output_file):
        unique_links = [{"url": link[0], "news_type": link[1], "news_subcategory": link[2]} for link in all_links]
        try:
            with open(output_file, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        existing_urls = {item['url'] for item in existing_data}
        filtered_new_data = [item for item in unique_links if item['url'] not in existing_urls]

        if filtered_new_data:
            existing_data.extend(filtered_new_data)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=4)
            print(f"Saved {len(filtered_new_data)} new links to {output_file}.")
        else:
            print("No new data to append.")

    for url in urls_to_scrape:
        url = urllib.parse.unquote(url)
        print(f"Processing: {url}")
        driver.get(url)
        driver.maximize_window()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
        news_type, news_subcategory = get_news_type(url)
        click_see_more_button(news_type, news_subcategory)

    driver.quit()


# Example usage:
start_urls = [
    # 'https://bangla.bdnews24.com/business',
    # 'https://bangla.bdnews24.com/economy',
    # 'https://bangla.bdnews24.com/stocks',
    # 'https://bangla.bdnews24.com/topic/%E0%A6%A2%E0%A6%BE%E0%A6%95%E0%A6%BE%20%E0%A6%AC%E0%A6%BF%E0%A6%AD%E0%A6%BE%E0%A6%97',
    # 'https://bangla.bdnews24.com/topic/%E0%A6%9A%E0%A6%9F%E0%A7%8D%E0%A6%9F%E0%A6%97%E0%A7%8D%E0%A6%B0%E0%A6%BE%E0%A6%AE%20%E0%A6%AC%E0%A6%BF%E0%A6%AD%E0%A6%BE%E0%A6%97',
    # 'https://bangla.bdnews24.com/topic/%E0%A6%B0%E0%A6%BE%E0%A6%9C%E0%A6%B6%E0%A6%BE%E0%A6%B9%E0%A7%80%20%E0%A6%AC%E0%A6%BF%E0%A6%AD%E0%A6%BE%E0%A6%97',
    # 'https://bangla.bdnews24.com/topic/%E0%A6%96%E0%A7%81%E0%A6%B2%E0%A6%A8%E0%A6%BE%20%E0%A6%AC%E0%A6%BF%E0%A6%AD%E0%A6%BE%E0%A6%97',
    # 'https://bangla.bdnews24.com/topic/%E0%A6%B8%E0%A6%BF%E0%A6%B2%E0%A7%87%E0%A6%9F%20%E0%A6%AC%E0%A6%BF%E0%A6%AD%E0%A6%BE%E0%A6%97',
    'https://bangla.bdnews24.com/topic/%E0%A6%AC%E0%A6%B0%E0%A6%BF%E0%A6%B6%E0%A6%BE%E0%A6%B2%20%E0%A6%AC%E0%A6%BF%E0%A6%AD%E0%A6%BE%E0%A6%97',
]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\ALL_NEWS\\BDNEWS_24\\final_news_links.json", start_urls)
