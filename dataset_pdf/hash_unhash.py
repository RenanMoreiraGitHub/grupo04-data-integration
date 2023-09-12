import pandas as pd
from os.path import join
from pathlib import Path

def hash_item(item: str) -> int:
    data_hash = list(item[::-1])
    aux = []
    for i in range(len(data_hash)):
        n = str(ord(data_hash[i]))
        data_hash[i] = n
        aux.append(str(len(n)))
    final_hash = int(''.join(data_hash))
    return hex(final_hash) + '.' + hex(int(''.join(aux)))

def unhash_item(item: str):
    item_aux = item.split('.')
    number = int(item_aux[0], base=16)
    aux = int(item_aux[1], base=16)
    ascii = []
    last_posit = 0
    for i in list(str(aux)):
        i = int(i)
        ascii.append(list(str(number))[last_posit:i+last_posit])
        last_posit = i+last_posit
    final_number_list = []
    for i in ascii:
        final_number_list.append(''.join(i))
    for i, v in enumerate(final_number_list):
        final_number_list[i] = chr(int(v))

    return ''.join(final_number_list[::-1])

def unhash_item_df(row, column):
    passwd = row[column]
    return unhash_item(passwd)

# item = '265273973'
# print(f'initial item ={item}')

# hashed_item = hash_item(item)
# print(f'hashed_item={hashed_item}')

# unhashed_item = unhash_item(hashed_item)
# print(f'unhashed_item={unhashed_item}')

if __name__ == "__main__":
    downloads_path = str(join(Path.home(), "Downloads"))
    df = pd.read_excel(join(downloads_path,'dados_vazados_clientes_pdf.xlsx'))
    df['password'] = df.apply(lambda row: unhash_item_df(row, 'password'), axis=1)
    df['cpf'] = df.apply(lambda row: unhash_item_df(row, 'cpf'), axis=1)
    df['rg'] = df.apply(lambda row: unhash_item_df(row, 'rg'), axis=1)
    print(df['password'].head())
    print(df['cpf'].head())
    print(df['rg'].head())
