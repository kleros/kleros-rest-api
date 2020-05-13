import json
from src.w3 import w3

def get_contract(contract_address, abi_file_name):
    try:
        contract_abi_file = open(file='src/abi/%s' % abi_file_name)
    except:
        raise RuntimeError("There is no file %s in /src/abi" % abi_file_name)

    abi = json.loads(contract_abi_file.read())['abi']
    return w3.eth.contract(address=contract_address, abi=abi)
