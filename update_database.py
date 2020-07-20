import subprocess
from pymongo import MongoClient
import json 

client = MongoClient('mongodb://localhost:27017')
db_blocks = client.test001.blocks
db_txes = client.test001.txes
last_db_height = 0

blockcount = int(subprocess.check_output('/root/bin/monkey-cli_p01.sh getblockcount', shell=True, universal_newlines=True))
print(str(blockcount))

for block in db_blocks.find().sort([("_id", -1)]).limit(1):
    last_db_height = int(block['height'])

last_db_height = last_db_height + 1 # start from next block from last inserted
print(str(last_db_height))

if blockcount > last_db_height:
    for index in range(last_db_height,blockcount+1):
        print('index: {}'.format(index))
        # break
        blockhash = subprocess.check_output('/root/bin/monkey-cli_p01.sh getblockhash ' + str(index), shell=True, universal_newlines=True) 

        # print(blockhash)

        block = subprocess.check_output('/root/bin/monkey-cli_p01.sh getblock ' + blockhash, shell=True, universal_newlines=True) 

        # print(block)

        block_dict = json.loads(block)
        db_blocks.insert_one(block_dict)

        for tx_hash in block_dict['tx']:
            print(tx_hash)
            # raw_tx = subprocess.check_output('/root/bin/monkey-cli_p01.sh getrawtransaction ' + tx_hash, shell=True, universal_newlines=True) 
            # print(str(raw_tx))
            # tx = subprocess.check_output('/root/bin/monkey-cli_p01.sh decoderawtransaction ' + raw_tx, shell=True, universal_newlines=True) 
            tx = subprocess.check_output('/root/bin/monkey-cli_p01.sh getrawtransaction ' + tx_hash + ' 1', shell=True, universal_newlines=True) 
            # print(str(tx))
            db_txes.insert_one(json.loads(tx))


