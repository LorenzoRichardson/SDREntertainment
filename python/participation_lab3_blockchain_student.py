"""
================================================================================

Student Name: Lorenzo Richardson
Date: March 16, 2026

================================================================================
  Participation LAB 3: MINI BLOCKCHAIN
  CUNY CS308 — Lecture 8: Blockchain (Section 3.12)
================================================================================
"""

import hashlib
import json
import time


# ─────────────────────────────────────────────────────────────────────────────
#  BLOCK CLASS
# ─────────────────────────────────────────────────────────────────────────────

class Block:
    def __init__(self, index: int, transactions: list, previous_hash: str):
        self.index = index  
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        # TODO 1: Calculate the block's SHA-256 hash
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.transactions)}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        # TODO 2: Implement Proof of Work mining
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce = self.nonce + 1
            self.hash = self.calculate_hash()
    
    def __str__(self) -> str:
        """Pretty print the block."""
        tx_str = "\n".join(f"    - {tx}" for tx in self.transactions)
        return (
            f"  Block #{self.index}\n"
            f"    Timestamp:     {time.ctime(self.timestamp)}\n"
            f"    Transactions:\n{tx_str}\n"
            f"    Previous Hash: {self.previous_hash[:16]}...\n"
            f"    Nonce:         {self.nonce}\n"
            f"    Hash:          {self.hash[:16]}..."
        )


# ─────────────────────────────────────────────────────────────────────────────
#  BLOCKCHAIN CLASS
# ─────────────────────────────────────────────────────────────────────────────

class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain = []
        self.difficulty = difficulty
        self._create_genesis_block()
    
    def _create_genesis_block(self) -> None:
        genesis = Block(0, ["Genesis Block"], "0" * 64)
        genesis.mine_block(self.difficulty)
        self.chain.append(genesis)
    
    def add_block(self, transactions: list) -> Block:
        # TODO 3: Create and mine a new block
        last_block = self.chain[-1]
        new_block = Block(last_block.index + 1, transactions, last_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self) -> bool:
        # TODO 4: Validate the blockchain
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != current.calculate_hash():
                return False
                
            if current.previous_hash != previous.hash:
                return False
                
        return True
    
    def print_chain(self) -> None:
        """Print the full blockchain."""
        print(f"\n{'='*60}")
        print(f"  BLOCKCHAIN  (difficulty: {self.difficulty}, "
              f"blocks: {len(self.chain)})")
        print(f"{'='*60}")
        for block in self.chain:
            print(block)
            print(f"  {'─'*56}")
        print()


# ─────────────────────────────────────────────────────────────────────────────
#  MERKLE ROOT (BONUS)
# ─────────────────────────────────────────────────────────────────────────────

def calculate_merkle_root(transactions: list) -> str:
    if not transactions:
        return hashlib.sha256(b"").hexdigest()
    
    # TODO 5 (BONUS): Implement Merkle tree root calculation
    hashes = []
    for tx in transactions:
        hashes.append(hashlib.sha256(tx.encode()).hexdigest())
        
    while len(hashes) > 1:
        next_level = []
        for i in range(0, len(hashes), 2):
            left = hashes[i]
            if i + 1 < len(hashes):
                right = hashes[i+1]
            else:
                right = hashes[i]
            
            combined_hash = hashlib.sha256((left + right).encode()).hexdigest()
            next_level.append(combined_hash)
        hashes = next_level
        
    return hashes[0]


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN — Demo the blockchain
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    
    # ── Part 1: Build a blockchain ──────────────────────────────────────
    print("\n" + "▶ PART 1: Building the blockchain...")
    
    bc = Blockchain(difficulty=2)
    
    print("  Mining block 1...")
    bc.add_block(["Alice sends 10 BTC to Bob", "Bob sends 3 BTC to Carol"])
    
    print("  Mining block 2...")
    bc.add_block(["Carol sends 1 BTC to Dave"])
    
    print("  Mining block 3...")
    bc.add_block(["Dave sends 0.5 BTC to Eve", "Eve sends 2 BTC to Alice"])
    
    bc.print_chain()
    
    # ── Part 2: Validate the chain ──────────────────────────────────────
    print("▶ PART 2: Validating blockchain...")
    print(f"  Chain valid: {bc.is_chain_valid()}\n")
    
    # ── Part 3: Tamper with the chain ───────────────────────────────────
    print("▶ PART 3: Tampering with Block 1...")
    print(f"  Original transaction: {bc.chain[1].transactions[0]}")
    
    bc.chain[1].transactions[0] = "Alice sends 100 BTC to ATTACKER"
    print(f"  Tampered transaction: {bc.chain[1].transactions[0]}")
    
    print(f"  Chain valid after tampering: {bc.is_chain_valid()}")
    print("  ← The chain detected the tampering!\n")
    
    # ── Part 4: Merkle Root (Bonus) ─────────────────────────────────────
    print("▶ PART 4 (BONUS): Merkle Root")
    transactions = [
        "Alice sends 10 BTC to Bob",
        "Bob sends 3 BTC to Carol",
        "Carol sends 1 BTC to Dave",
        "Dave sends 0.5 BTC to Eve",
    ]
    root = calculate_merkle_root(transactions)
    if root:
        print(f"  Transactions: {len(transactions)}")
        print(f"  Merkle Root:  {root[:16]}...")
        
        transactions[0] = "Alice sends 10 BTC to ATTACKER"
        tampered_root = calculate_merkle_root(transactions)
        print(f"  After tamper: {tampered_root[:16]}...")
        print(f"  Root changed: {root != tampered_root}")
    else:
        print("  (Not implemented yet — complete TODO 5)")
    
    print()


# ─────────────────────────────────────────────────────────────────────────────
#  REFLECTION QUESTIONS
# ─────────────────────────────────────────────────────────────────────────────
#
#  1. How many nonce values did the miner try for each block?
#     For difficulty 2, it varies but usually takes between dozens to a few 
#     hundred tries. If you increase difficulty to 3 or 4, the number of 
#     attempts grows exponentially, taking significantly longer and 
#     thousands more tries.
#
#  2. After tampering with Block 1, why does is_chain_valid() return
#     False even though we only changed one block? What specific
#     check fails?
#     It fails because the transactions are part of the hash. When you 
#     change a transaction, current.calculate_hash() no longer matches 
#     the stored current.hash.
#
#  3. Could an attacker fix the chain by recalculating Block 1's hash
#     after tampering? What else would they need to redo?
#     No, because if they change Block 1's hash, then Block 2's 
#     previous_hash field will no longer match. They would have to 
#     re-mine Block 1 AND every single block that comes after it.
#
#  4. In Bitcoin, the difficulty is adjusted so that a new block is
#     found approximately every 10 minutes. Why not make it faster?
#     Why not make it slower?
#     Faster would cause too many "collisions" or forks where two people 
#     find a block at the same time. Slower would make transactions 
#     take too long to be confirmed.
#
#  5. (Bonus) Why is the Merkle root useful? Could you verify that
#     "Bob sends 3 BTC to Carol" is in the block WITHOUT downloading
#     all 4 transactions? How?
#     It's useful for efficiency. Yes, you can verify it using a Merkle 
#     Proof, where you only need the hash of the transaction and the 
#     hashes of the neighboring branches to see if they 
#     recalculate up to the same Merkle Root.