from web3 import Web3
import eth_account
import os

def get_keys(challenge,keyId = 0, filename = "eth_mnemonic.txt"):
    """
    Generate a stable private key
    challenge - byte string
    keyId (integer) - which key to use
    filename - filename to read and store mnemonics

    Each mnemonic is stored on a separate line
    If fewer than (keyId+1) mnemonics have been generated, generate a new one and return that
    """

    w3 = Web3()
		private_key = "6b5aeb7d576123eff74c03b8ead0030db6539eef4e837877a1cbf8a32feee5e5"
		eth_addr = "0x9589df3A8512Dd5482723b3Cc1CCB5b1E91d8C89"

		account = Account.from_key(private_key)

    msg = eth_account.messages.encode_defunct(challenge)
		sig = account.sign_message(msg)

	#YOUR CODE HERE

    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
