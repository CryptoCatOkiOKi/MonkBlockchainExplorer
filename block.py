from pymongo import MongoClient
from bson import json_util, ObjectId
import json
import transaction

client = MongoClient('mongodb://localhost:27017')
db_blocks = client.test001.blocks

def get_block(block_hash,height):
    """
    Get block data from block_hash or height(block number)
    """
    if block_hash is not None:
        block = db_blocks.find({"hash": block_hash})
    elif height is not None:
        try:
            block = db_blocks.find({"height": int(height)})
        except:
            return None

    block_dump = json_util.dumps(block)
    if block_dump and block_dump != '[]':
        block_sanitized = json.loads(block_dump)[0]
        return block_sanitized
    return None

def get_last_blocks(number_of_blocks):
    """
    Get last blocks from db
    """
    # tx_id = '55883a76c3f10a61fb5f8ab32bb43c8880a7e971ee3c38f2fa13d907185fcdbc'
    return db_blocks.find().limit(number_of_blocks).sort('height', -1)

def get_block_txes(block_hash,height):
    """
    Get list of transactions of a block
    """
    if block_hash is not None:
        block = db_blocks.find({"hash": block_hash})
    elif height is not None:
        try:
            block = db_blocks.find({"height": int(height)})
        except:
            return None
        
    block_dump = json_util.dumps(block)
    if block_dump and block_dump != '[]':
        block_sanitized = json.loads(block_dump)[0]
    else:
        return None          

    txes = set()

   # for tx_id in block_sanitized['tx']:
   #    txes.add(tx_id)

    txes = [tx for tx in block_sanitized['tx']]

    return txes   


def get_no_recipients_block(block_hash):
    """
    Get number of recipients in a block
    * this function is not used!
    """
    # print(block_hash)
    block = db_blocks.find({"hash": block_hash})
    block_sanitized = json.loads(json_util.dumps(block))[0]
    addys = set()
    # print(block_sanitized)
    # print(block_sanitized['tx'])

    for tx_id in block_sanitized['tx']:
        tx = transaction.get_tx(tx_id)
        for vout in tx['vout']:
            # print(vout)
            for vout_key, vout_value in vout.items():
                if vout_key == 'scriptPubKey':
                    # print(vout_key + ': ' + str(vout_value))
                    for scriptPubKey_key, scriptPubKey_value in vout_value.items():
                        if scriptPubKey_key == 'addresses':
                            # print(key + ': ' + str(value))
                            for address in scriptPubKey_value:
                                # print('address: ' + address)
                                addys.add(address)

    return ( len(addys) )

def get_no_txes_block(block_hash):
    """
    Get number of transactions in a block
    """
    block = get_block(block_hash, None)
    return len(block['tx']) 

def get_amount_block(block_hash):
    """
    Get amount transfered in a block
    * this function is not used!
    """
    # print(block_hash)
    block = db_blocks.find({"hash": block_hash})
    block_sanitized = json.loads(json_util.dumps(block))[0]
    # print(block_sanitized)
    # print(block_sanitized['tx'])
    block_amount = 0

    for tx_id in block_sanitized['tx']:
        tx = transaction.get_tx(tx_id)
        for vout in tx['vout']:
            # print(vout)
            for vout_key, vout_value in vout.items():
                if vout_key == 'value':
                    # print(vout_key + ': ' + str(vout_value))
                    block_amount = block_amount + vout_value

    return ( block_amount )     
      