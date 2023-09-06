
def hash_item(item: str) -> str:    
    data_hash = list(item[::-1])
    for i in range(len(data_hash)):
        data_hash[i] = ord(data_hash[i])
    return data_hash

def unhash_item(item: str):
    unhashed_item = item[::-1]
    for i in range(len(unhashed_item)):
        unhashed_item[i] = chr(unhashed_item[i])
    
    return unhashed_item

item = 'enan.oliveira'
hashed_item = hash_item(item)
print(f'hashed_item={hashed_item}')
unhashed_item = unhash_item(hashed_item)
print(f'unhashed_item={unhashed_item}')
