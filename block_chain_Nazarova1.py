﻿# Ссылки
# http://127.0.0.1:5000/mine_block
# http://127.0.0.1:5000/display_chain
# http://127.0.0.1:5000/valid

import hashlib
import json
from flask import Flask, jsonify
import psycopg2
import pandas as pd

# Класс для представления блокчейна
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

# Функция для подключения к базе данных
def connect_db():
    # Использование PostgreSQL для подключения к базе данных
    conn = psycopg2.connect(dbname='BD_Nazarova', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kino")
    df = cursor.fetchall()
    df = pd.DataFrame(df)
    return df

# Получение данных из базы данных
database = connect_db()

# Класс для представления блокчейна
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    # Создание нового блока в блокчейне
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            
            'name': str(database[1].iloc[len(self.chain)]),
            'year': str(database[2].iloc[len(self.chain)]),
            'budget': str(database[3].iloc[len(self.chain)]),
            'viewers': str(database[4].iloc[len(self.chain)]),
            'company': str(database[5].iloc[len(self.chain)]),
            'ocenka': str(database[6].iloc[len(self.chain)]),
            'sbory': str(database[7].iloc[len(self.chain)]),
            'gener': str(database[8].iloc[len(self.chain)]),
            'proof': proof,
            'previous_hash': previous_hash
        }
        # Добавление блока в цепочку
        self.chain.append(block)
        return block

    # Получение предыдущего блока в блокчейне
    def print_previous_block(self):
        return self.chain[-1]

    # Поиск подходящего proof для нового блока
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # Вычисление хеша с использованием proof
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # Проверка условия наличия '00000' в начале хеша
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    # Хеширование блока в блокчейне
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # Проверка целостности блокчейна
    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # Проверка соответствия previous_hash хешу предыдущего блока
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            # Вычисление хеша для проверки условия наличия '00000' в начале хеша
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1
        return True

# Создание объекта блокчейна
blockchain = Blockchain()

# Создание веб-приложения с использованием Flask
app = Flask(__name__)

# Определение маршрутов (endpoints) для веб-приложения
@app.route('/')
def index():
    return "Mine a new block: /mine_block  " \
           "Display the blockchain in JSON format: /display_chain  " \
           "Check the validity of the blockchain: /valid  "

@app.route('/mine_block', methods=['GET'])
def mine_block():
    # Получение предыдущего блока
    previous_block = blockchain.print_previous_block()
    # Получение proof для нового блока
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_block['proof'])
    # Получение хеша предыдущего блока
    previous_hash = blockchain.hash(previous_block)
    # Создание нового блока
    block = blockchain.create_block(proof, previous_hash)
    # Формирование ответа с данными нового блока
    response = {'message': 'A block is MINED',
                'index': block['index'],
                'name': block['name'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

@app.route('/display_chain', methods=['GET'])
def display_chain():
    # Формирование цепочки блоков для вывода
    chain = []
    for block in blockchain.chain:
        data = {
            'ID': block['index'],
            'Film_name': block['name'],
            'Viewers': block['viewers'],
            'Sbory': block['sbory'],
            'Ocenka': block['ocenka']
        }
        chain.append(data)
    # Формирование ответа с цепочкой блоков
    response = {'chain': chain, 'length': len(chain)}
    return jsonify(response), 200

@app.route('/valid', methods=['GET'])
def valid():
    # Проверка целостности блокчейна
    valid = blockchain.chain_valid(blockchain.chain)
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200

# Запуск веб-приложения
app.run(debug=True, port=5000)



