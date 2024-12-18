from blockchain import Blockchain

if __name__ == "__main__":
    blockchain = Blockchain(difficulty=4)  # Increase difficulty for more security
    blockchain.add_block("Block 1 Data")
    blockchain.add_block("Block 2 Data")
    blockchain.add_block("Block 3 Data")
    print("\n")

    for block in blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Data: {block.data}")
        print(f"Nonce: {block.nonce}")
        print(f"Timestamp: {block.timestamp}")
        print("\n")
        
