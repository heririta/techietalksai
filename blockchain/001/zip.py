import os

# Create directory structure for the project
base_path = "/mnt/data/simple_blockchain"
folders = [
    base_path,
    os.path.join(base_path, "blockchain"),
    os.path.join(base_path, "docker")
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Main blockchain Python code
blockchain_code = '''\
import hashlib
import json
from time import time
from flask import Flask, jsonify, request

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)  # Genesis block

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Flask web server to interact with the blockchain
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])

    blockchain.new_transaction(sender="0", recipient="you", amount=1)

    block = blockchain.new_block(proof)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
'''

with open(os.path.join(base_path, "blockchain", "main.py"), "w") as f:
    f.write(blockchain_code)

# Dockerfile
dockerfile = '''\
FROM python:3.11-slim
WORKDIR /app
COPY blockchain/ /app/
RUN pip install flask
EXPOSE 5000
CMD ["python", "main.py"]
'''

with open(os.path.join(base_path, "docker", "Dockerfile"), "w") as f:
    f.write(dockerfile)

# docker-compose.yml
compose_file = '''\
version: '3.8'

services:
  blockchain:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./blockchain:/app
'''

with open(os.path.join(base_path, "docker-compose.yml"), "w") as f:
    f.write(compose_file)

import shutil
shutil.make_archive("/mnt/data/simple_blockchain", 'zip', base_path)

