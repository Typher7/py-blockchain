from flask import Flask
from web3 import Web3

app = Flask(__name__)

w3 = Web3(Web3.HTTPProvider("http://localhost:5000"))

@app.route('/')
def index():
    return w3.eth.block_number

if __name__ == '__main__':
    app.run()