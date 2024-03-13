import time
import hashlib
import json
import requests
import base64
from flask import Flask, request
# from multiprocessing import Process, pipes
import ecdsa

node = Flask(__name__)

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
    
    def create_merkle_tree_hash(transaction_list):
        if len(transaction_list)==0:
            return None
        if len(transaction_list)==1:
            return transaction_list[0].txn_hash
        if len(transaction_list)%2!=0:
            transaction_list.append(transaction_list[-1])
        new_txn_list=[]
        for i in range(0, len(transaction_list), 2):
            new_txn_list.append(hashlib.sha256((transaction_list[i]+transaction_list[i+1]).encode('utf-8')).hexdigest())
        return create_merkle_tree_hash(new_txn_list)

class Transaction:
    def __init__(self, owner, input_list, output_list, signature):
        self.owner=owner
        self.input_list=input_list
        self.output_list=output_list
        self.signature=signature
        if signature!=None:
            self.txn_hash=self.hash_txn()
    
    def hash_txn(self):
        sha=hashlib.sha256()
        sha.update((str(self.owner)+str(self.input_list)+str(self.output_list)+str(self.signature)).encode('utf-8'))
        return sha.hexdigest()


class Txn_Input_Item:
    def __init__(self, prev_txn_hash, block_index, output_index):
        self.prev_txn_hash=prev_txn_hash
        self.block_index=block_index
        self.output_index=output_index


class Txn_Output_Item:
    def __init__(self, receiver, value):
        self.receiver=receiver
        self.value=value

def create_genesis_block():
    return Block(0, time.time(), "Genesis Block", "0", 0)


BLOCKCHAIN=[]
PENDING_TXNS=[]
DIFFICULTY_THRESHOLD=4

# def mine(blockchain, utxo, pipe):

#     # Check the server for copies of peers

#     # Assuming the server has sent the copies of peers
#     if len(BLOCKCHAIN)==0:
#         BLOCKCHAIN.append(create_genesis_block())
    
#     while True:
        
