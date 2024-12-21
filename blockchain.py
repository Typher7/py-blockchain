import hashlib, time, json, base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class Block:
    def __init__(self, index, previous_hash, data, timestamp=None, nonce=0, signature=None):
        self.index = index 
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()
        self.signature = signature

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def sign_block(self, private_key):
        message = f"{self.index}{self.previous_hash}{self.data}"
        self.signature = private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    
    def verify_block(self, public_key):
        message = f"{self.index}{self.previous_hash}{self.data}"
        try:
            public_key.verify(
                self.signature,
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
class Blockchain:
    def __init__(self, difficulty=4, length=1):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.length = length

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block")
    
    def add_block(self, data, private_key):
        last_block = self.chain[-1]
        new_block = Block(self.length, last_block.hash, data)
        new_block.sign_block(private_key)
        self.mine_block(new_block)
        self.chain.append(new_block)
        self.length += 1
        self.save_chain()
    
    def validate_chain(self, public_key):
        for block in self.chain[1:]: #This bypasses the Genesis Block
            if not block.verify_block(public_key):
                return False
        return True

    def mine_block(self, block):
        while not block.hash.startswith("0" * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        print(f"Block mined: {block.hash}")
    
    def save_chain(self):
        with open('chain.json', 'w') as file:
            json.dump([{
                "index": block.index,
                "hash": block.hash,
                "previous_hash": block.previous_hash,
                "data": block.data,
                "signature": base64.b64encode(block.signature).decode('utf-8') if block.signature else '',
                "timestamp": block.timestamp
            } for block in self.chain], file)
    
    def load_chain(self):
        try:
            with open('chain.json', 'r') as file:
                chain_data = json.load(file)
                self.chain = [Block(**block) for block in chain_data]
        except FileNotFoundError:
            self.chain = [self.create_genesis_block()]
    