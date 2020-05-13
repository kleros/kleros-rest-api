import time
from flask import request, jsonify

from src.utils.contract import get_contract
from src.addresses import t2cr as t2cr_addresses
from src.w3 import w3

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
ZERO_ID = '0x0000000000000000000000000000000000000000000000000000000000000000'
CACHE_TIMEOUT_SECONDS = 600 # 10 minutes

STATUS_ENUM = {
    "absent": 0, # Token removed from list
    "registered": 1, # Token in list
    "requested": 2, # Token requested to be added to list
    "clearing": 3, # Token requested to be removed from list
    "disputed": 4, # Token in dispute over addition to list
    "clearing_disputed": 5 # Tokens in dispute over removal from list
}

# CACHE
RESULTS_CACHE = {}
CACHE_TIMESTAMPS = {}
ERC20_CACHE = []
ERC20_CACHE_TIMESTAMP = 0

TokenStatus = ["Absent", "Registered", "RegistrationRequested", "ClearingRequested"]

def json_serialize_tokens(tokens):
    json_tokens = []
    for token in tokens:
        if ('0x'+token[0].hex()) == ZERO_ID:
            continue

        json_tokens.append({
            "id": '0x'+token[0].hex(),
            "name": token[1],
            "ticker": token[2],
            "address": token[3],
            "symbolURI": token[4],
            "status": TokenStatus[int(token[5])],
            "decimals": token[6]
        })

    return json_tokens

def get_filter(request_object):
    filter = [False, False, False, False, False, False, False, False]
    seen_one = False
    for status in STATUS_ENUM.keys():
        if request_object.args.get(status, False):
            seen_one = True
            filter[STATUS_ENUM[status]] = True
    # No filters were passed, defaut to registered
    if not seen_one:
        filter[STATUS_ENUM['registered']] = True
    return filter

def register_t2cr_routes(app):
    @app.route('/t2cr/tokens', methods=['GET'])
    def get_t2cr_tokens():
        # ERC20
        erc20 = request.args.get('erc20', 'false')
        if erc20 == 'false':
            erc20 = False
        else:
            erc20 = True
        # Create the appropriate filter
        filter = get_filter(request)
        filter_hash = hash(str(filter))

        # Check if we need to refresh cache
        if not CACHE_TIMESTAMPS.get(filter_hash) or CACHE_TIMESTAMPS[filter_hash] + CACHE_TIMEOUT_SECONDS < int(time.time()):
            token_ids = []
            has_more = True
            cursor = ZERO_ID

            token_list_contract = get_contract(t2cr_addresses['token_list'], 'arbitrable-token-list.json')
            token_view_contract = get_contract(t2cr_addresses['view'], 'arbitrable-token-view.json')

            while has_more:
                token_results = token_list_contract.functions.queryTokens(cursor, 1000, filter, True, ZERO_ADDRESS).call()
                has_more = token_results[1]
                token_ids = token_ids + token_results[0]
                cursor = token_ids[-1]

            tokens = token_view_contract.functions.getTokens(t2cr_addresses['token_list'], token_ids).call()
            serialized_tokens = json_serialize_tokens(tokens)
            CACHE_TIMESTAMPS[filter_hash] = int(time.time())
            RESULTS_CACHE[filter_hash] = serialized_tokens

        if not erc20:
            return jsonify(results=RESULTS_CACHE[filter_hash]), 200
        else:
            global ERC20_CACHE_TIMESTAMP
            global ERC20_CACHE
            # Fetch ERC20 badge token ids
            if ERC20_CACHE_TIMESTAMP + CACHE_TIMEOUT_SECONDS < int(time.time()):
                erc20_badge_contract = get_contract(t2cr_addresses['erc20_list'], 'arbitrable-address-list.json')

                addresses = []
                has_more = True
                cursor = ZERO_ADDRESS
                erc20_filter = [False, True, False, False, False, False, False, False]

                while has_more:
                    address_values = erc20_badge_contract.functions.queryAddresses(cursor, 1000, erc20_filter, True).call()
                    addresses += address_values[0]
                    has_more = address_values[1]
                    cursor = addresses[-1]

                ERC20_CACHE_TIMESTAMP = int(time.time())
                ERC20_CACHE = addresses

            erc20_tokens = []
            for token in RESULTS_CACHE[filter_hash]:
                if token['address'] in ERC20_CACHE:
                    erc20_tokens.append(token)

            return jsonify(results=erc20_tokens)
