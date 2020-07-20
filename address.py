from pymongo import MongoClient
from bson import json_util, ObjectId
import json
import transaction

client = MongoClient('mongodb://localhost:27017')
db_txes = client.test001.txes

def get_txes(address):
   """
   Get list of transactions for an address
   """
   address_txes = db_txes.find({'vout.scriptPubKey.addresses' : address})
   address_txes_sanitized = json.loads(json_util.dumps(address_txes))
   return address_txes_sanitized

def get_txes_data(address):
   """
   Get data required for transaction page inputs data / outputs data
   """
   txes = get_txes(address)
   data = []
   # raw_data = []
   inputs = []
   outputs = []
   x = {}
   y = {}
   for tx in reversed(txes):
      tx_id = tx['txid']
      inputs = transaction.get_input_data(tx_id,address)
      x = {}
      y = {} 
      value_sent = float()     
      value_received = float()     
      if inputs:
         for input1 in inputs:
            for key, item in input1.items():
               if key == 'value':
                  value_sent = value_sent + item

         # raw_data.append(inputs)
         x = {
            'address': inputs[0]['address'],
            'tx': inputs[0]['tx'],
            'value_sent': value_sent,
            'time': inputs[0]['time'],
            'block': inputs[0]['block']
         }         
         

      outputs = transaction.get_output_data(tx_id,address)
      if outputs:
         for output1 in outputs:
            for key, item in output1.items():
               if key == 'value':
                  value_received = value_received + item         
         # raw_data.append(outputs)
         if x:
            y = { 'value_received': value_received,
                  'value_change': value_received - value_sent
               }
            x.update(y)
         else:
            x = {
               'address': outputs[0]['address'][0],
               'tx': outputs[0]['tx'],
               'value_received': value_received,
               'time': outputs[0]['time'],
               'block': outputs[0]['block'],
               'value_change': value_received
            } 

      if x:
         data.append(x)

   return data

# address_test = get_txes('Moz9YxkWDN93BpviKptjWUwF82MDTR1a6H')
# print(address_test)

# inputs = get_txes_data('Moz9YxkWDN93BpviKptjWUwF82MDTR1a6H')
# print(inputs)
