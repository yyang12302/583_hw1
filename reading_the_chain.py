import random
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.providers.rpc import HTTPProvider


# If you use one of the suggested infrastructure providers, the url will be of the form
# now_url  = f"https://eth.nownodes.io/{now_token}"
alchemy_url = f"https://eth-mainnet.g.alchemy.com/v2/nbSCxYOO8iccH60-uMmNp0gZDdhGSJKT"
# infura_url = f"https://mainnet.infura.io/v3/{infura_token}"

def connect_to_eth():
	# TODO insert your code for this method from last week's assignment
	url = "https://eth-mainnet.g.alchemy.com/v2/nbSCxYOO8iccH60-uMmNp0gZDdhGSJKT"  # FILL THIS IN
	w3 = Web3(HTTPProvider(https://eth-mainnet.g.alchemy.com/v2/nbSCxYOO8iccH60-uMmNp0gZDdhGSJKT))
	assert w3.is_connected(), f"Failed to connect to provider at {https://eth-mainnet.g.alchemy.com/v2/nbSCxYOO8iccH60-uMmNp0gZDdhGSJKT}"
	return w3
	#return w3




def connect_with_middleware(contract_json): 
    with open(contract_json, "r") as f:
        d = json.load(f)
        d = d['bsc']
        address = d['address']
        abi = d['abi'] 

    # Connect to BNB provider
    bnb_url = "https://bsc-testnet-rpc.publicnode.com"  # Public BNB provider URL
    w3 = Web3(Web3.HTTPProvider(bnb_url))
    assert w3.is_connected(), f"Failed to connect to provider at {bnb_url}"

    # Inject the POA middleware for BSC
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Create the contract object
    contract = w3.eth.contract(address=address, abi=abi)

    # Check if the connection is successful
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to the Binance Smart Chain")

    return w3, contract
	


def is_ordered_block(w3, block_num):
	"""
	Takes a block number
	Returns a boolean that tells whether all the transactions in the block are ordered by priority fee

	Before EIP-1559, a block is ordered if and only if all transactions are sorted in decreasing order of the gasPrice field

	After EIP-1559, there are two types of transactions
		*Type 0* The priority fee is tx.gasPrice - block.baseFeePerGas
		*Type 2* The priority fee is min( tx.maxPriorityFeePerGas, tx.maxFeePerGas - block.baseFeePerGas )

	Conveniently, most type 2 transactions set the gasPrice field to be min( tx.maxPriorityFeePerGas + block.baseFeePerGas, tx.maxFeePerGas )
	"""
	block = w3.eth.get_block(block_num)
	ordered = True
	lastGP = float('inf')

	# TODO YOUR CODE HERE
	for transaction_hash in block['transactions']:
  	transaction = w3.eth.get_transaction(transaction_hash)
  	gasPrice = transaction['gasPrice']
    if 'maxPriorityFeePerGas' in transaction:
    	gasPrice = transaction['maxPriorityFeePerGas']
    if gasPrice > lastGP:
      ordered = False
    	break
    lastGP = gasPrice
  return ordered



def get_contract_values(contract, admin_address, owner_address):
	"""
	Takes a contract object, and two addresses (as strings) to be used for calling
	the contract to check current on chain values.
	The provided "default_admin_role" is the correctly formatted solidity default
	admin value to use when checking with the contract
	To complete this method you need to make three calls to the contract to get:
	  onchain_root: Get and return the merkleRoot from the provided contract
	  has_role: Verify that the address "admin_address" has the role "default_admin_role" return True/False
	  prime: Call the contract to get and return the prime owned by "owner_address"

	check on available contract functions and transactions on the block explorer at
	https://testnet.bscscan.com/address/0xaA7CAaDA823300D18D3c43f65569a47e78220073
	"""
	default_admin_role = int.to_bytes(0, 32, byteorder="big")

	# TODO complete the following lines by performing contract calls
	onchain_root = contract.functions.merkleRoot().call()  # Get and return the merkleRoot from the provided contract
	has_role = contract.functions.hasRole(default_admin_role, admin_address).call()  # Check the contract to see if the address "admin_address" has the role "default_admin_role"
	prime = contract.functions.prime(owner_address).call()  # Call the contract to get the prime owned by "owner_address"

	return onchain_root, has_role, prime


"""
	This might be useful for testing (main is not run by the grader feel free to change 
	this code anyway that is helpful)
"""
if __name__ == "__main__":
	# These are addresses associated with the Merkle contract (check on contract
	# functions and transactions on the block explorer at
	# https://testnet.bscscan.com/address/0xaA7CAaDA823300D18D3c43f65569a47e78220073
	admin_address = "0xAC55e7d73A792fE1A9e051BDF4A010c33962809A"
	owner_address = "0x793A37a85964D96ACD6368777c7C7050F05b11dE"
	contract_file = "contract_info.json"

	eth_w3 = connect_to_eth()
	cont_w3, contract = connect_with_middleware(contract_file)

	latest_block = eth_w3.eth.get_block_number()
	london_hard_fork_block_num = 12965000
	assert latest_block > london_hard_fork_block_num, f"Error: the chain never got past the London Hard Fork"

	n = 5
	for _ in range(n):
		block_num = random.randint(1, london_hard_fork_block_num - 1)
		ordered = is_ordered_block(block_num)
		if ordered:
			print(f"Block {block_num} is ordered")
		else:
			print(f"Block {block_num} is not ordered")
