"""Module to get data from TikTok"""
import time
from datetime import datetime

from bs4 import BeautifulSoup
from constants import LANG, MAX_PAGINATION, SLEEP_TIME, TIKTOK_URL
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def _get_hashtags(soup_itens):
    hashtags = []
    for item in soup_itens:
        if not item.text.startswith("#"):
            continue
        hashtags.append(item.text.strip())
    return hashtags


def _open_page(driver, url):
    driver.get(url)
    time.sleep(SLEEP_TIME)
    return driver


def _make_soup(driver):
    source = driver.get_attribute("innerHTML")
    soup = BeautifulSoup(source, "html.parser")
    return soup


def _extract_data_from_video(driver):
    path = "//*[@id='app']/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[3]"
    element = driver.find_element("xpath", path)
    soup = _make_soup(element)
    items = soup.find_all('strong', 'tiktok-wxn977-StrongText edu4zum2')
    items = [item.text for item in items]
    data = {}
    data['likes'] = items[0]
    data['comments'] = items[1]
    data['shares'] = items[2]
    return data


def _get_trends(driver, results):
    if not results:
        return []

    for video in results:
        soup = _make_soup(video)
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
            }
            page = _open_page(driver, trend["url"])
            data = _extract_data_from_video(page)
            trend.update(data)
            trends.append(trend)
    return trends


def get_videos(subject_to_search):
    """Get videos from a subject"""
    url_root = TIKTOK_URL
    url_search = f"{url_root}search?lang={LANG}&q={subject_to_search}"
    driver = Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url_search)
    time.sleep(SLEEP_TIME)
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
    trends = _get_trends(driver, results)
    driver.close()
    return trends


def get_video_metadata(url):
    """Get metadata from a video"""

    driver = Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(SLEEP_TIME)
    path = "//*[@id='app']/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[3]"
    element = driver.find_element("xpath", path)
    soup = _make_soup(element)
    items = soup.find_all('strong', 'tiktok-wxn977-StrongText edu4zum2')
    items = [item.text for item in items]
    data = {}
    data['like'] = items[0]
    data['comment'] = items[1]
    data['share'] = items[2]
    return data


def get_comments_from_video(url):
    """Get comments from a video using the URL"""
    driver = Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(SLEEP_TIME)
    i = 0
    while i < MAX_PAGINATION:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)", "")
        time.sleep(SLEEP_TIME)
        driver.execute_script("window.scrollTo(0,-50)", "")
        i += 1
        time.sleep(SLEEP_TIME)
    path = "//*[@id='app']/div[2]/div[2]/div[1]/div[3]/div[1]/div[3]"
    element = driver.find_element("xpath", path)
    soup = _make_soup(element)
    items = soup.find_all('div', 'tiktok-1ko6l9n-DivCommentListContainer ekjxngi0')
    replys = []
    for item in items:
        comments = item.find_all('div', 'tiktok-16r0vzi-DivCommentItemContainer eo72wou0')
    for comment in comments:
        username = comment.find('a', 'tiktok-bhsg9d-StyledUserLinkName e1g2efjf4')['href']
        msg = comment.find('p', 'tiktok-q9aj5z-PCommentText e1g2efjf6').text
        reply = {'username': username, 'reply': msg}
        replys.append(reply)
    return replys
