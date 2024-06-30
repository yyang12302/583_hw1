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

    # Inject the POA middleware for BSC
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    
    # Create the contract object
    contract = w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)

    return w3, contract

if __name__ == "__main__":
    connect_to_eth()
