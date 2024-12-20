import hashlib, time, json

class Block:
    def __init__(self, index, previous_hash, data, timestamp=None, nonce=0):
        self.index = index 
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self, difficulty=4, length=1):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.length = length

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block")
    
    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), last_block.hash, data)
        self.mine_block(new_block)
        self.chain.append(new_block)
        self.length += 1

    def mine_block(self, block):
        while not block.hash.startswith("0" * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        print(f"Block mined: {block.hash}")
    
    def save__chain(self):
        with open('chain.json', 'w') as file:
            json.dump([block.__dict__ for block in self.chain], file)
    
    def load_chain(self):
        try:
            with open('chain.json', 'r') as file:
                chain_data = json.load(file)
                self.chain = [Block(**block) for block in chain_data]
        except FileNotFoundError:
            self.chain = [self.create_genesis_block()]
    