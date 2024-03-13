import time
import hashlib
import json
import requests
import base64
from flask import Flask, request
# from multiprocessing import Process, pipes
import ecdsa

node = Flask(__name__)

MINER_PUBKEY="public_key1"
MINER_PRIVKEY="private_key1"
NETWORK="network"
BLOCKCHAIN=[]
PENDING_TXNS_L=[]
PENDING_TXNS_CNTR_L=0
DIFFICULTY_THRESHOLD_L=4
COINBASE_REWARD=25

class Block:
    def __init__(self, index, timestamp, txn_list, previous_hash, difficultly_threshold):
        self.index=index
        self.timestamp=timestamp
        self.txn_list=txn_list
        self.previous_hash=previous_hash
        self.hash=None
        self.nonce=None
        self.difficultly_threshold=difficultly_threshold
        self.merkle_tree_hash=create_merkle_tree(self.txn_list)

    def hash_block(self):
        sha=hashlib.sha256()
        sha.update((str(self.index)+str(self.timestamp)+str(self.data)+str(self.previous_hash)+str(self.nonce)+str(self.difficulty_threshold)).encode('utf-8'))
        return sha.hexdigest()
    
    def update_hash(self, nonce):
        self.nonce=nonce
        self.hash=self.hash_block()
        return self.hash

        
    def create_merkle_tree_hash_helper(transaction_hash_list):
        if len(transaction_hash_list)==1:
            return transaction_hash_list[0]
        if len(transaction_hash_list)%2!=0:
            transaction_hash_list.append(transaction_hash_list[-1])
        new_transaction_hash_list=[]
        for i in range(0,len(transaction_hash_list),2):
            new_transaction_hash_list.append(hashlib.sha256((transaction_hash_list[i]+transaction_hash_list[i+1]).encode('utf-8')).hexdigest())
        return create_merkle_tree_hash_helper(new_transaction_hash_list)
    
    def create_merkle_tree_hash(transaction_list):
        if len(transaction_list)==0:
            return None
        transaction_hash_list=[]
        for txn in transaction_list:
            transaction_hash_list.append(txn.txn_hash)
        return create_merkle_tree_hash_helper(transaction_hash_list)

class Transaction:
    def __init__(self, owner, input_list, output_list, signature):
        self.owner=owner
        self.input_list=input_list
        self.output_list=output_list
        self.signature=self.sign_txn()
    
    #signs the transaction hash
    def sign_txn(self):
        data = str(self.owner) + str(self.input_list) + str(self.output_list)
        hashed_data = hashlib.sha256(data.encode()).hexdigest()
        # Sign the hashed data with the global private key
        signature = MINER_PRIVKEY.sign(hashed_data)
        return signature
    
    #verifies the signature of the transaction given against the given public key
    def verify_signature(self, public_key):
        data = str(self.owner) + str(self.input_list) + str(self.output_list)
        hashed_data = hashlib.sha256(data.encode()).digest()
        try:
            # Verify the signature using the provided public key
            return public_key.verify(self.signature, hashed_data)
        except ecdsa.BadSignatureError:
            return False


class Txn_Input_Item:
    def __init__(self, block_index, prev_txn_hash, output_index):
        self.block_index=block_index
        self.prev_txn_hash=prev_txn_hash
        self.output_index=output_index


class Txn_Output_Item:
    def __init__(self, receiver, value):
        self.receiver=receiver
        self.value=value

def create_genesis_block():
    return Block(0, time.time(), "Genesis Block", "0", 0)

def verify_txn(transaction):
    #checking signature
    if not transaction.verify_sign():
        return False
    #checking input sources
    input_list = transaction.input_list
    #checking output sum

def mine():

    # Check the server for copies of peers

    # Assuming the server has sent the copies of peers
    if len(BLOCKCHAIN)==0:
        BLOCKCHAIN.append(create_genesis_block())
    
    while True:
        
        temp_pending_txn_list=PENDING_TXNS_L
        temp_txn_list=[]

        for idx in range(min(temp_pending_txn_list.size,5)):
            if verify_txn(temp_pending_txn_list[idx]):
                temp_txn_list.append(temp_pending_txn_list[idx])
                temp_pending_txn_list.pop(idx)
            else:
                temp_pending_txn_list.pop(idx)
                continue
        
        temp_txn_list.append(Transaction(NETWORK,None,MINER_PUBKEY,None))