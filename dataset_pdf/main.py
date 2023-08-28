from faker import Faker
from pypdf import PdfReader
import re
import pandas as pd
from random import randint
from os import getenv
from dotenv import load_dotenv; load_dotenv()
from pathlib import Path
from os.path import join

from mysql_connection import MysqlConnection

def get_all_pages_text_pdf(pdf: str) -> str:
    reader = PdfReader(pdf)
    all_text = ''
    for page in reader.pages:
        all_text+=page.extract_text()
    return all_text

def anonymization(string: str, left: int, right: str):
    character_left = ''
    for i in range(left):
        character_left+='*'
    character_right = ''
    for i in range(right):
        character_right+='*'
    string = character_left + string[left:]
    string = string[:-right] + character_right
    return string

def correct_cpf(cpf: str) -> str:
    while len(cpf) < 11:
        cpf+=str(randint(1,9))
    while len(cpf) > 11:
        cpf = cpf[:-1]
    return anonymization(cpf, 3, 3)

def correct_rg(rg: str) -> str:
    while len(rg) < 9:
        rg+=str(randint(1,9))
    while len(rg) > 9:
        rg = rg[:-1]
    return anonymization(rg, 2, 2)

all_text = get_all_pages_text_pdf('./dataset_students.pdf')

list_rgs = []
list_cpfs = []
list_names = []
list_cpfs.append('***07916***')
for line in all_text.splitlines():
    if not line.isspace() and \
    not line.startswith('2013 -PROFMAT') and \
    not line.startswith('Exame Nacional de Acesso') and \
    not line.startswith('Listagem de Candidatos'):
        cpf = re.findall(r'CPF\: \d+', line)
        if len(cpf) > 0:
            cpf_insert = cpf[0][4:].replace(' ', '').replace('-', '').replace('.', '')
            cpf_insert = correct_cpf(cpf_insert)
            list_cpfs.append(cpf_insert)

        rg_name = re.findall(r'RG\: .+', line)
        if len(rg_name) > 0:
            rg: str = rg_name[0].split('AT4')[0][3:]
            rg_insert = rg.replace(' ', '').replace('-', '').replace('.', '')
            rg_insert = correct_rg(rg_insert)
            list_rgs.append(rg_insert)
            
            name: str = rg_name[0].split('AT4')[1]
            splitter = re.findall(r' - SALA \d+', name)
            if len(splitter) > 0:
                list_names.append(name.split(splitter[0])[-1].replace('2013 -PROFMAT -', '').strip())

def label_race(row):
   name = row['name'].split(' ')[0].upper()
   random_sex = ['feminine', 'masculine']
   if name.endswith('A'):
      return 'feminine'
   elif name.endswith('O'):
      return 'masculine'
   return random_sex[randint(0,1)]

generator = Faker()
def generate_address(row):
    return generator.address()

df = pd.DataFrame({'name': list_names, 'cpf': list_cpfs, 'rg': list_rgs})
df['age'] = pd.Series(range(18, 35)).sample(int(173), replace=True).array
df['gender'] = df.apply(lambda row: label_race(row), axis=1)
df['adress'] = df.apply(lambda row: generate_address(row), axis=1)

print(df.head())

downloads_path = str(join(Path.home(), "Downloads"))
print(f'Downloading dataset pdf to {downloads_path}...')
df.to_excel(join(downloads_path, 'dados_vazados_clientes_pdf.xlsx'), index=True)

mysql_db = MysqlConnection(
    getenv('USER_BD'), getenv('PASS_BD'), getenv('HOST_BD'))
mysql_db.connect()
mysql_db.insert_dataframe(df, 'dados_vazados_clientes_pdf', 'soybean', index=True)
mysql_db.disconnect()
