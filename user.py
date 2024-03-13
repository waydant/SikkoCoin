import requests
import time
import base64
import ecdsa
import json

def generate_ECDSA_keys():
    """This function takes care of creating your private and public (your address) keys.
    It's very important you don't lose any of them or those wallets will be lost
    forever. If someone else get access to your private key, you risk losing your coins.

    private_key: str
    public_ley: base64 (to make it shorter)
    """
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)  # this is your sign (private key)
    private_key = sk.to_string().hex()  # convert your private key to hex
    vk = sk.get_verifying_key()  # this is your verification key (public key)
    public_key = vk.to_string().hex()
    # we are going to encode the public key to make it shorter
    public_key = base64.b64encode(bytes.fromhex(public_key))

    filename = input("Write the name of your new address: ") + ".txt"
    with open(filename, "w") as f:
        f.write(F"Private key: {private_key}\nWallet address / Public key: {public_key.decode()}")
    print(F"Your new address and private key are now in the file {filename}")

def check_transcations(blockchain, address):
    
    

def propose_transaction(owner, input_list, output_list, signature):
    owner = USER_PUBLIC_KEY
    