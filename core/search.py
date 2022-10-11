import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from constants import LANG, MAX_PAGINATION, SLEEP_TIME, TIKTOK_URL


def _get_hashtags(soup_itens):
    hashtags = []
    for item in soup_itens:
        if not item.text.startswith("#"):
            continue
        hashtags.append(item.text.strip())
    return hashtags

def _get_trends(results):
    if not results:
        return []

    for video in results:
        data = video.get_attribute("innerHTML")
        soup = BeautifulSoup(data, "html.parser")
        titles = soup.find_all('div', "tiktok-1ejylhp-DivContainer ejg0rhn0")
        usernames = soup.find_all('div', "tiktok-dq7zy8-DivUserInfo etrd4pu5")
        counts = soup.find_all('div', "tiktok-1lbowdj-DivPlayIcon etrd4pu4")
        url = soup.find_all('div', "tiktok-bbkab3-DivContainer e1cg0wnj0")
        date = soup.find_all('div', "tiktok-11u47i-DivCardFooter e148ts220")
        hashtags = soup.find_all('div', "tiktok-1ejylhp-DivContainer ejg0rhn0")
        trends = []
        for index, title in enumerate(titles):
            trend = {
                "title": title.text,
                "username": usernames[index].text.strip(),
                "views": counts[index].text,
                "url": url[index].find('a').get('href'),
                "date": date[index].text,
                "hashtags": _get_hashtags(hashtags[index]),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "shares": 0,
                "comments": 0,
                "likes": 0,

            }
            trends.append(trend)
    return trends


def get_videos(subject_to_search):
    # get data from a user using the username
    url_root = TIKTOK_URL
    url_search = f"{url_root}search?lang={LANG}&q={subject_to_search}"
    driver = Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url_search)
    time.sleep(3)
    page = 0
    while page < MAX_PAGINATION:
        try:
            element_path = "//*[@id='app']/div[2]/div[2]/div[2]/div[2]/button"
            element = driver.find_element("xpath", element_path)
            element.click()
            time.sleep(SLEEP_TIME)
            page += 1
        except NoSuchElementException as error:
            print('No more results', error)
            break
    path_element = "//*[@id='app']/div[2]/div[2]/div[2]/div[1]/div"
    results = driver.find_elements("xpath", path_element)
    trends = _get_trends(results)
    driver.close()
    return trends

