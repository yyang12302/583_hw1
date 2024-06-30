import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.providers.rpc import HTTPProvider

def connect_to_eth():
    url = "https://eth-mainnet.g.alchemy.com/v2/nbSCxYOO8iccH60-uMmNp0gZDdhGSJKT"  # FILL THIS IN
    w3 = Web3(HTTPProvider(url))
    assert w3.is_connected(), f"Failed to connect to provider at {url}"
    return w3

def connect_with_middleware(contract_json):
    with open(contract_json, "r") as f:
        d = json.load(f)
        d = d['bsc']
        address = d['address']
        abi = d['abi']

    # Connect to BSC
    bnb_url = "https://bsc-dataseed.binance.org/"  # Public BNB provider URL
    w3 = Web3(Web3.HTTPProvider(bnb_url))
    assert w3.is_connected(), f"Failed to connect to provider at {bnb_url}"
    print("Successfully connected to BSC")

    # Inject the POA middleware for BSC
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print("Successfully injected middleware into the web3 object")

    # Create the contract object
    contract = w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)
    print("Contract object created successfully")

    # Check if we can interact with the contract
    try:
        # Example: Check the contract's total supply (assuming it's an ERC20 token)
        total_supply = contract.functions.totalSupply().call()
        print(f"Total Supply: {total_supply}")
    except Exception as e:
        print(f"Could not transact with/call contract function, is contract deployed correctly and chain synced? Error: {e}")

    return w3, contract

if __name__ == "__main__":
    eth_w3 = connect_to_eth()
    print("Connected to Ethereum Mainnet")
    try:
        eth_block = eth_w3.eth.get_block('latest')
        print(f"Successfully retrieved block {eth_block['number']}")
    except Exception as e:
        print(f"Failed to retrieve Ethereum block: {e}")

    bsc_w3, contract = connect_with_middleware("path_to_your_contract.json")  # Replace with the correct path to your JSON file
    if bsc_w3.is_connected():
        print("w3 instance is connected to BSC")
        try:
            bsc_block = bsc_w3.eth.get_block('latest')
            print(f"Successfully retrieved block {bsc_block['number']}")
        except Exception as e:
            print(f"Failed to retrieve BSC block: {e}")
    else:
        print("w3 instance is not connected to BSC")
