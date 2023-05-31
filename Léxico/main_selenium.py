from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import requests
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv()
chromedriver_autoinstaller.install()

def is_duplicated(list: list, value: str):
    count = 0
    for i in list:
        if i == value:
            count += 1
    return count > 1

URL_TWITTER = 'https://twitter.com/i/flow/login'
SEARCHS = [
    'colheita soja',
    'soja brasil',
    'preço soja',
    'semeadura soja'
]
info = {}

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.get(URL_TWITTER)
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "text"))).send_keys(getenv('twitter_email'))
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((
        By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span"))).click()
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "text"))).send_keys(getenv('twitter_username'))
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div"))).click()
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(getenv('twitter_passwd'))
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div"))).click()
driver.maximize_window()
for search in SEARCHS:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[placeholder='Buscar no Twitter']"))).send_keys(Keys.CONTROL + 'a')
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[placeholder='Buscar no Twitter']"))).send_keys(Keys.DELETE)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[placeholder='Buscar no Twitter']"))).send_keys(search)
    input_search = driver.find_element(By.CSS_SELECTOR, "[placeholder='Buscar no Twitter']")
    input_search.send_keys(Keys.ENTER)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Timeline: Buscar timeline']")))
    timeline = driver.find_element(By.CSS_SELECTOR, "[aria-label='Timeline: Buscar timeline']")
    div_all_posts = timeline.find_elements(By.TAG_NAME, 'div')

    text_posts = ''
    for i in div_all_posts:
        try:
            text = i.text
            text_posts += text
        except Exception:
            continue

    text_posts = [x for x in text_posts.split('\n') if x != '' and len(x) > 3 and not x[0].isdigit() and not x.startswith('@')]

    text_posts_without_duplicateds = []
    for i in text_posts:
        if not is_duplicated(text_posts_without_duplicateds, i):
            text_posts_without_duplicateds.append(i)

    info.update({
        search: text_posts_without_duplicateds
    })

driver.close()

with open('scrapper_soybean_twitter.json', 'w', encoding='UTF-8') as fp:
    json.dump(info, fp, indent=4)
    
headers = {'Content-type': 'application/json'}

requests.put('https://e3w3e8wui0.execute-api.us-east-1.amazonaws.com/dev/0211033-raw-sprint-3/scrapper_soybean_twitter.json',
             data=open('scrapper_soybean_twitter.json', 'rb'), headers=headers) 
