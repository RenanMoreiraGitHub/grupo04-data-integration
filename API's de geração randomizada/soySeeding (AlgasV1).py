import datetime
import sys
import matplotlib.pyplot as plt
import random   
import mysql.connector  

# ##LOCAL
# mydb = mysql.connector.connect(
#     host="localhost",
#     user='root',
#     password="Jeremy420691",
#     database = "semeaduraSoja"
# )

##AZURE
mydb = mysql.connector.connect(
    host="semeadura-soja.mysql.database.azure.com",
    user="j9remy",
    password="Urubu100",
    database = "semeadurasoja",
    port="3306"
)

cursor = mydb.cursor()

# cursor.execute("CREATE DATABASE IF NOT EXISTS semeaduraSoja")
cursor.execute("USE semeaduraSoja")
cursor.execute("CREATE TABLE IF NOT EXISTS fluxo_graos (id INT AUTO_INCREMENT PRIMARY KEY, fluxo_graos INT, total_graos INT, tempo DECIMAL(15,4), taxa_ocupacao_silo DECIMAL(5,2), mem INT, ambiente VARCHAR(20))")

def get_input():
    min = 1
    measure = 0
    while measure not in [1, 2, 3]:
        measure = int(input("\nQual medida você deseja simular?\n1 - Simulação por sacas\n2 - Simulação por m2 de área colhida\n3 - Simulação por hectare\n\n"))
        if measure == 1:
            max = int(input("Quantas sacas de soja foram coletadas? "))
            step = 1
        elif measure == 2:
            max = int(input("Quantos m² de soja foram coletados? "))
            step = 1
        elif measure == 3:
            max = int(input("Quantos hectares de soja foram coletados? "))
            step = 1
        else:
            print("Opção inválida, selecione uma opção válida!")
    return min, max, step, measure

mem_usage = []
time_elapsed = []

def simul_fluxo_graos(min, max, step, measure):
    fluxo_graos = []
    total_graos = []
    tempo_graos = []
    mem_usage = []

    cursor = mydb.cursor()
    start_time = datetime.datetime.now()

    mem = 0
    dado_quantidade_total_graos = 0
    dado_tempo = 0
    capacidade_silo = int(input("\nQual a capacidade do seu silo em grãos?\nEstima-se que um silo de 100 m³ tem capacidade para armazenar cerca de 2,5 milhões de grãos de soja\n\n"))

    for i in range(min, max + 1, step):
        if measure == 1:
            dado_fluxo_graos = random.randint(140_000, 180_000)
        elif measure == 2:
            dado_fluxo_graos = random.randint(3_600, 4_800)
        elif measure == 3:
            dado_fluxo_graos = random.randint(2_500_000, 4_000_000)

        dado_quantidade_total_graos += dado_fluxo_graos
        taxa_ocupacao_silo = (dado_quantidade_total_graos / capacidade_silo) * 100
        dado_tempo = (datetime.datetime.now() - start_time).total_seconds()
        
        tempo_graos.append(dado_tempo)
        total_graos.append(dado_quantidade_total_graos)
        fluxo_graos.append(dado_fluxo_graos)
        fluxo_graos.sort()

        mem = sys.getsizeof(fluxo_graos) * 1024
        mem_usage.append(mem)

        sql = "INSERT INTO fluxo_graos values (null, %s, %s, %s, %s, %s, 'LOCAL');"

        values = (dado_fluxo_graos, dado_quantidade_total_graos, dado_tempo, taxa_ocupacao_silo, mem)

        cursor.execute(sql, values)
        mydb.commit()

    end_time = datetime.datetime.now()
    time_elapsed.append((end_time - start_time).total_seconds())


min, max, step, measure = get_input()
simul_fluxo_graos(min, max, step, measure)