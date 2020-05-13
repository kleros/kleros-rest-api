import os
from web3 import Web3

PROVIDER_URI = os.environ.get('PROVIDER_URI', 'https://mainnet.infura.io/v3/11fe61c1a83444adad75e22b30f60f68')

# Check if provider uses websockets or http
if PROVIDER_URI[0:3] == 'wss':
    w3 = Web3(Web3.WebsocketProvider(PROVIDER_URI))
else:
    w3 = Web3(Web3.HTTPProvider(PROVIDER_URI))
