from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
api_url = "https://mainnet.infura.io/v3/aafeae9b6729474abd0aec8eaf878d77=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"  #YOU WILL NEED TO TO PROVIDE THE URL OF AN ETHEREUM NODE
provider = HTTPProvider(api_url)
web3 = Web3(provider)
contract = web3.eth.contract(address=bayc_address, abi=abi)


def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	
	gateway=f"https://gateway.pinata.cloud/ipfs/{cid}"
	headers={
		'pinata_api_key':'6bf509970b4e9c3ecee6',
		'pinata_secret_api_key':'d935f96f288a65d6fd2b5984af63efa47d6022cc03cba8aeebefd65a330fa9a6'

	}
	response = requests.get(gateway, headers=headers)
	print(response.json())
	if content_type =="json":
		data = response.json()
	else:
		data = response.content

	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data

def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"
	assert apeID < 10000, f"{apeID} must be at most 9999"


	data = {'owner': "", 'image': "", 'eyes': "" }
	
	#YOUR CODE HERE
	owner = contract.functions.ownerOf(apeID).call()
	data['owner'] = owner

	uri = contract.functions.tokenURI(apeID).call()
	bayc_cid = uri.replace('ipfs://', '')
	content_data = get_from_ipfs(bayc_cid)

	data['image'] = content_data['image']

	for attr in content_data['attributes']:
		if attr['trait_type'] == 'Eyes':
			data['eyes'] = attr['value']

	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

