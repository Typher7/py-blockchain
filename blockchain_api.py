from flask import Flask, jsonify, request
from blockchain import Blockchain
import os
from cryptography.hazmat.primitives import serialization


# Create Flask App
app = Flask(__name__)
port = int(os.getenv('PORT', 5000))

# Init blockchain
blockchain = Blockchain(difficulty=3)

# Get the full blockchain
@app.route('/chain', methods=['GET'])
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
    return jsonify({"length": blockchain.length, "chain": chain_data}), 200



# Add a transaction
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    values = request.get_json()
    require_fields = ['data', 'private_key']
    if not all(field in values for field in require_fields):
        return "Missing fields", 400
    
    private_key = serialization.load_pem_private_key(
        values['private_key'].encode(),
        password=None
    )
    blockchain.add_block(values['data'], private_key)
    return jsonify({"message": "Transaction added"}), 200


# Add n transactions
@app.route('/add_transactions', methods=['POST'])
def add_transactions():
    values = request.get_json()

    # Check for required fields
    required_fields = ['data', 'private_key']
    if not all(field in values for field in required_fields):
        return jsonify({"error": "Missing required fields: 'data' and 'private_key'"}), 400
    
    # Ensure data is a non-empty list
    if not isinstance(values['data'], list) or not values['data']:
        return jsonify({"error": "Field 'data' must be a non-empty list."}), 400
    
    try:
        private_key = serialization.load_pem_private_key(
            values['private_key'].encode(),
            password=None
        )
    except ValueError:
        return jsonify({"error": "Invalid private key format"}), 400
    
    # Process each transaction
    successful_blocks = 0
    for data in values['data']:
        try:
            blockchain.add_block(data, private_key)
            successful_blocks += 1
        except Exception as e:
            return jsonify({
                "error": f"Failed to add block for data: {data}",
                "exception": str(e),
                "successful_blocks": successful_blocks
            }), 400
    
    return jsonify({
        "message": "Successfully added {successful_blocks}",
        "total_attempted": len(values['data'])
                    }), 201

# Validate the Chain
@app.route('/validate_hashes', methods=["GET"])
def validate_chain():
    for i in range(1, blockchain.length):
        current_block = blockchain.chain[i]
        prev_block = blockchain.chain[i-1]

        if current_block.hash != current_block.calculate_hash():
            return jsonify({"valid": False, "error": "Hash mismatch"}), 400
        
        if current_block.previous_hash != prev_block.hash:
            return jsonify({"valid": False, "error": "Broken chain"}), 400
    
    return jsonify({"valid": True}), 200

#Validate the Blockchain
@app.route('/validate_keys', methods=['POST'])
def validate():
    values = request.get_json()
    required_fields = ['public_key']
    if not all(field in values for field in required_fields):
        return "Missing fields", 400
    
    public_key = serialization.load_pem_public_key(values['public_key'].encode())
    is_valid = blockchain.validate_chain(public_key)
    return jsonify({"valid": is_valid}), 200

# Query block by index
@app.route('/block/<int:index>', methods=['GET'])
def get_block(index):
    if index < 0 or index >= blockchain.length:
        return jsonify({"error": "Block doesn't exist"}), 404
    
    block = blockchain.chain[index]
    block_data = {
        "index": block.index,
        "hash": block.hash,
        "previous_hash": block.previous_hash,
        "data": block.data,
        "nonce": block.nonce,
        "timestamp": block.timestamp
    }
    return jsonify(block_data), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
    blockchain.load_chain()