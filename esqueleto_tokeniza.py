from textblob import TextBlob
from pprint import pp
import pandas as pd
import datetime
import boto3
import collections
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from dotenv import load_dotenv
from os import getenv
import sys
import json

boto3.setup_default_session(profile_name='faculdade')


# load_dotenv()
# chromedriver_autoinstaller.install()


# def is_duplicated(list: list, value: str):
#     count = 0
#     for i in list:
#         if i == value:
#             count += 1
#     return count > 1


# URL_TWITTER = 'https://twitter.com/i/flow/login'
# SEARCHS = [
#     'preço soja', 'agro soja', 'soja no agro',
#     'brasil na soja', 'soja no brasil', 'soja',
#     'uso da soja', 'soja para alimentos',
#     'alimentos de soja', 'soja faz bem',
#     'soja faz mal', 'aumento da soja',
#     'diminuição da soja'
# ]
# info = {}

# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome()
# driver.get(URL_TWITTER)
# WebDriverWait(driver, 60).until(EC.presence_of_element_located(
#     (By.NAME, "text"))).send_keys(getenv('twitter_email'))
# WebDriverWait(driver, 60).until(
#     EC.presence_of_element_located((
#         By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span"))).click()
# # WebDriverWait(driver, 60).until(EC.presence_of_element_located(
# #     (By.NAME, "text"))).send_keys(getenv('twitter_username'))
# # WebDriverWait(driver, 60).until(EC.presence_of_element_located(
# #     (By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div"))).click()
# WebDriverWait(driver, 60).until(EC.presence_of_element_located(
#     (By.NAME, "password"))).send_keys(getenv('twitter_passwd'))
# WebDriverWait(driver, 60).until(EC.presence_of_element_located(
#     (By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div"))).click()
# driver.maximize_window()
# for search in SEARCHS:
#     WebDriverWait(driver, 60).until(EC.presence_of_element_located(
#         (By.CSS_SELECTOR, "[placeholder='Buscar no Twitter']"))).send_keys(Keys.CONTROL + 'a')
#     WebDriverWait(driver, 60).until(EC.presence_of_element_located(
#         (By.CSS_SELECTOR, "[placeholder='Buscar no Twitter']"))).send_keys(Keys.DELETE)
#     WebDriverWait(driver, 60).until(EC.presence_of_element_located(
#         (By.CSS_SELECTOR, "[placeholder='Buscar no Twitter']"))).send_keys(search)
#     input_search = driver.find_element(
#         By.CSS_SELECTOR, "[placeholder='Buscar no Twitter']")
#     input_search.send_keys(Keys.ENTER)
#     WebDriverWait(driver, 60).until(EC.presence_of_element_located(
#         (By.CSS_SELECTOR, "[aria-label='Timeline: Buscar timeline']")))
#     timeline = driver.find_element(
#         By.CSS_SELECTOR, "[aria-label='Timeline: Buscar timeline']")
#     div_all_posts = timeline.find_elements(By.TAG_NAME, 'div')

#     text_posts = ''
#     for i in div_all_posts:
#         try:
#             text = i.text
#             text_posts += text
#         except Exception:
#             continue

#     text_posts = [x for x in text_posts.split('\n') if x != '' and len(
#         x) > 3 and not x[0].isdigit() and not x.startswith('@')]

#     text_posts_without_duplicateds = []
#     for i in text_posts:
#         if not is_duplicated(text_posts_without_duplicateds, i):
#             text_posts_without_duplicateds.append(i)

#     info.update({
#         search: text_posts_without_duplicateds
#     })

# driver.close()

# with open('scrapper_soybean_twitter.txt', 'w', encoding='UTF-8') as fp:
#     json.dump(info, fp, indent=4)


#############################################

f = open('scrapper_soybean_twitter.txt', 'r')
content = f.read()


TESTE = False

OPERADORES = "%*/+-!^="

DIGITOS = "0123456789"

PONTO = "."

# todos os caracteres usados em um números float
FLOATS = DIGITOS + PONTO

LETRAS = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

ABRE_FECHA_PARENTESES = "()"

OPERADOR = 1  # para operadores aritméticos e atribuição
NUMERO = 2  # para números: todos são considerados float
VARIAVEL = 3  # para variáveis
PARENTESES = 4  # para '(' e ')

BRANCOS = [' ', '\n', '\t', '\v', '\f', '\r']

COMENTARIO = "#"


# ------------------------------------------------------------
def tokeniza(exp):
    tokens = []  # lista para armazenar os tokens

    i = 0

    while i < len(exp):
        char = exp[i]

        if char == COMENTARIO:
            break

        if char in BRANCOS:
            i += 1
            continue

        if char in OPERADORES:
            token = [char, OPERADOR]
            tokens.append(token)
            i += 1
            continue

        if char in FLOATS:
            # Constrói o número até encontrar um caractere que não seja dígito ou ponto decimal
            num = char
            i += 1
            while i < len(exp) and exp[i] in FLOATS:
                num += exp[i]
                i += 1
            token = [float(num), NUMERO]
            tokens.append(token)
            continue

        if char in LETRAS:
            var = char
            i += 1
            while i < len(exp) and exp[i] in LETRAS + DIGITOS:
                var += exp[i]
                i += 1
            token = [var, VARIAVEL]
            tokens.append(token)
            continue

        if char in ABRE_FECHA_PARENTESES:
            token = [char, PARENTESES]
            tokens.append(token)
            i += 1
            continue

        i += 1

    return tokens


tokens = tokeniza(content)


def analize_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 1  # positivo
    elif analysis.sentiment.polarity == 0:
        return 0  # neutro
    else:
        return -1  # negativo


palavras_boas = []
palavras_neutras = []
palavras_negativas = []

# pegando apenas palavras
for token in tokens:
    if token[1] == 3:
        word = token[0]
        if analize_sentiment(word) == 1:
            palavras_boas.append(word)
        elif analize_sentiment(word) == 0:
            palavras_neutras.append(word)
        elif analize_sentiment(word) == -1:
            palavras_negativas.append(word)


frequenciaPositivas = collections.Counter(palavras_boas)
palavras_mais_frequentes_positivas = frequenciaPositivas.most_common()

frequenciaNeutras = collections.Counter(palavras_neutras)
palavras_mais_frequentes_neutras = frequenciaNeutras.most_common()

frequenciaNegativas = collections.Counter(palavras_negativas)
palavras_mais_frequentes_negativas = frequenciaNegativas.most_common()

lengths = [len(palavras_mais_frequentes_positivas), len(
    palavras_mais_frequentes_neutras), len(palavras_mais_frequentes_negativas)]
max_length = max(lengths)

# Extend arrays to have the same length
palavras_mais_frequentes_positivas += [('N/A', 0)] * \
    (max_length - len(palavras_mais_frequentes_positivas))
palavras_mais_frequentes_neutras += [('N/A', 0)] * \
    (max_length - len(palavras_mais_frequentes_neutras))
palavras_mais_frequentes_negativas += [('N/A', 0)] * \
    (max_length - len(palavras_mais_frequentes_negativas))

# Create DataFrame
df = pd.DataFrame({
    'Palavras Positivas': [word for word, count in palavras_mais_frequentes_positivas],
    'Frequência Positivas': [count for word, count in palavras_mais_frequentes_positivas],
    'Palavras Neutras': [word for word, count in palavras_mais_frequentes_neutras],
    'Frequência Neutras': [count for word, count in palavras_mais_frequentes_neutras],
    'Palavras Negativas': [word for word, count in palavras_mais_frequentes_negativas],
    'Frequência Negativas': [count for word, count in palavras_mais_frequentes_negativas]
})

pp(df)


date_now = datetime.datetime.now()
s3 = boto3.client('s3')
bucket_name = 'raw-sprint-3'
file_name = f'{date_now}.csv'

df.to_csv(file_name, index=False)
s3.upload_file(file_name, bucket_name, file_name)
