from flask import Flask, jsonify, request
from blockchain import Blockchain

# Create Flask App
app = Flask(__name__)

# Init blockchain
blockchain = Blockchain(difficulty=4)

# Get the full blockchain
@app.route('/chain', methods=['Get'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "hash": block.hash,
            "previous_hash": block.previous_hash,
            "data": block.data,
            "nonce": block.nonce,
            "timestamp": block.timestamp
        })
    return jsonify({"length": len(chain_data), "chain": chain_data}), 200

# Add a new block
@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.get_json().get("data")
    if not data:
        return jsonify({"error": "Data is required"}), 400
    blockchain.add_block(data)
    return jsonify({"message": "Block added successfully"}), 201

if __name__ == "__main__":
    app.run(port=5000)