from pymongo import MongoClient
from bson import json_util, ObjectId
import json
import block

client = MongoClient('mongodb://localhost:27017')
db_blocks = client.test001.blocks
db_txes = client.test001.txes

def get_tx(tx_id):
   """
   Get transaction data from db
   """
   # tx_id = '55883a76c3f10a61fb5f8ab32bb43c8880a7e971ee3c38f2fa13d907185fcdbc'
   # print(f'tx_id: {tx_id}')
   tx = db_txes.find({"txid": tx_id})
   tx_sanitized = json.loads(json_util.dumps(tx))[0]   
   return tx_sanitized

def get_input_data(tx_id, p_address = None):
   """
   Get input data from transaction
   tx_id = transaction ID
   p_address = data for a specific address
   """
   tx = get_tx(tx_id)
   addy = str()
   value = int()
   data = []
   
   for vin in tx['vin']:
      if 'txid' in vin:
         input_tx = get_tx(vin['txid'])      
         for input_vout in input_tx['vout']:
            if (input_vout['scriptPubKey']['type'] == 'pubkey' or input_vout['scriptPubKey']['type'] == 'pubkeyhash') and vin['vout'] == input_vout['n']:
               for address in input_vout['scriptPubKey']['addresses']:
                  if p_address is None or p_address == address:
                     addy = address
                     value = input_vout['value']   
                     block_height = block.get_block(tx['blockhash'],None)['height']
                     vin_data = {
                        'tx': tx_id,
                        'address': addy,
                        'value': value,
                        'tx_vin': vin['txid'],
                        'time': tx['time'],
                        'block': block_height
                     }
                     data.append(vin_data)

   return data

def get_output_data(tx_id, p_address = None):
   """
   Get output data from transaction
   tx_id = transaction ID
   p_address = data for a specific address
   """   
   tx = get_tx(tx_id)
   value = int()
   data = []
   
   for vout in tx['vout']:
      addys = []
      value = vout['value']   
      block_height = block.get_block(tx['blockhash'],None)['height'] 
      if 'addresses' in vout['scriptPubKey']:    
         for address in vout['scriptPubKey']['addresses']:
            # print(address)
            addys.append(address)
         
      if (p_address is None) or (p_address in addys):
         vout_data = {
            'tx': tx_id,
            'address': addys,
            'value': value,
            'time': tx['time'],
            'block': block_height         
         }
         data.append(vout_data)

   return data   

def get_amount(tx_id):
   """
   Get output ammount from transaction
   tx_id = transaction ID
   """   
   tx = get_tx(tx_id)
   tx_amount = 0.0
   for vout in tx['vout']:
      for vout_key, vout_value in vout.items():
         if vout_key == 'value':
            tx_amount = tx_amount + vout_value   
   
   return tx_amount 


# output = get_output_data('a38862ed2bd5154aad79e56a7dad32ba7f3d9a5d20327ebe254bf2c8011797ac','Moz9YxkWDN93BpviKptjWUwF82MDTR1a6H')
# print(output) 