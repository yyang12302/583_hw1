#!/bin/python
import hashlib
import os
import random
import secrets

def mine_block(k, prev_hash, rand_lines):
    if not isinstance(k, int) or k < 0:
        print("mine_block expects positive integer")
        return b'\x00'
    byte_str = b''
    for line in rand_lines:
        byte_str += line.encode('utf-8')
    combined_data = prev_hash + byte_str
    while True:
        nonce = secrets.token_bytes(16)
        hash_object = hashlib.sha256(combined_data + nonce)
        hash_result = hash_object.digest()
        binary_hash = bin(int.from_bytes(hash_result, byteorder='big'))
        if binary_hash.endswith('0' * k):
            break
    assert isinstance(nonce, bytes), 'nonce should be of type bytes'
    return nonce

def get_random_lines(filename, quantity):
    """
    This is a helper function to get the quantity of lines ("transactions")
    as a list from the filename given.
    Do not modify this function
    """
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())
    random_lines = []
    for x in range(quantity):
        random_lines.append(lines[random.randint(0, quantity - 1)])
    return random_lines

if __name__ == '__main__':
    # This code will be helpful for your testing
    filename = "bitcoin_text.txt"
    num_lines = 10  # The number of "transactions" included in the block

    # The "difficulty" level. For our blocks this is the number of Least Significant Bits
    # that are 0s. For example, if diff = 5 then the last 5 bits of a valid block hash would be zeros
    # The grader will not exceed 20 bits of "difficulty" because larger values take too long
    diff = 20
    rand_lines = get_random_lines(filename, num_lines)
    prev_hash = hashlib.sha256(b"previous hash").digest()
    nonce = mine_block(diff, prev_hash, rand_lines)
    print(nonce)
