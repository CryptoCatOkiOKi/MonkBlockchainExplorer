# main.py

from flask import Flask, render_template, request, jsonify
# from flask_json import FlaskJSON, JsonError, json_response, as_json
import block, transaction, address

from bson import json_util, ObjectId
import json

from datetime import datetime

app = Flask(__name__)
# FlaskJSON(app)

@app.route("/", methods = ['POST', 'GET'])
def route_home():
   print('app.route /')
   last_blocks = block.get_last_blocks(5)
   print(last_blocks)

   return render_template('new_blocks.html', blocks=last_blocks)

@app.route("/block/<blockhash>", methods = ['POST', 'GET'])
def route_block(blockhash):
   print('app.route /block/<blockhash>')
   block_data = block.get_block(blockhash,None)
   txes = block.get_block_txes(blockhash,None)

   return render_template('block.html', block=block_data, txes=txes)  

@app.route("/blockno/<height>", methods = ['POST', 'GET'])
def route_block_no(height):
   print('app.route /blockno/<height>')
   block_data = block.get_block(None, height)
   txes = block.get_block_txes(None, height)

   return render_template('block.html', block=block_data, txes=txes)    

@app.route("/tx/<txhash>", methods = ['POST', 'GET'])
def route_transaction(txhash):
   print('app.route /tx/<txhash>')
   tx = transaction.get_tx(txhash)
   input_data = transaction.get_input_data(txhash)
   output_data = transaction.get_output_data(txhash)

   return render_template('transaction.html', tx=tx, input=input_data, output=output_data)

@app.route("/address/<p_address>", methods = ['POST', 'GET'])
def route_address(p_address):
   print('app.route /address/<p_address>')
   address_data = address.get_txes_data(p_address)

   return render_template('address.html', address_data=address_data)

#
# Search button
#    
@app.route("/submit", methods = ['POST', 'GET'])
def search_button():
   search_input = "".encode('utf-8')
   search_result = ""
   for key, value in request.form.items():
      # print("key: {0}, value: {1}".format(key, value))
      search_input = value.encode('utf-8')

   if search_input:
      blockhash = search_input
      print('blockhash')
      block_data = block.get_block(blockhash,None)
      txes = block.get_block_txes(blockhash,None) 
      if block_data and txes:
         print('blockhash block.html')
         return render_template('block.html', block=block_data, txes=txes)
      else:
         print('blockheight')
         blockheight = search_input
         block_data = block.get_block(None,blockheight)
         txes = block.get_block_txes(None,blockheight) 
         if block_data and txes:
            print('blockheight block.html')
            return render_template('block.html', block=block_data, txes=txes)
         else:
            print('transaction')
            try:
               txhash = search_input
               tx = transaction.get_tx(txhash)
               input_data = transaction.get_input_data(txhash)
               output_data = transaction.get_output_data(txhash)
               if tx and input_data and output_data:
                  return render_template('transaction.html', tx=tx, input=input_data, output=output_data)
               else:
                  try:
                     print('address 1')
                     address_input = search_input
                     address_data = address.get_txes_data(address_input)
                     if address_data:
                        return render_template('address.html', address_data=address_data)
                  except:
                     pass
            except:
               try:
                  print('address 2')
                  address_input = search_input
                  address_data = address.get_txes_data(address_input)
                  if address_data:
                     return render_template('address.html', address_data=address_data)
               except:
                  pass

   last_blocks = block.get_last_blocks(5)
   print('new_blocks.html')
   return render_template('new_blocks.html', blocks=last_blocks)

#
#  Procedures for formating data in templates 
#       

@app.route("/txjson/", methods=['GET'])
def route_get_tx_data():
   print('app.route /txjson/')
   tx_id = request.args.get('txid')
   tx = transaction.get_tx(tx_id)
   print(type(tx))
   tx_sanitized = json.loads(json_util.dumps(tx))
   # print(type(tx_sanitized))
   tx_json = jsonify(tx_sanitized)
   # tx_json = json.dumps(tx_sanitized)
   # print(type(tx_json))
   return tx_json

@app.template_filter()
def datetimefilter(timestamp):
   """Convert a timestamp to a date"""    
   return datetime.fromtimestamp(timestamp)

app.jinja_env.filters['datetimefilter'] = datetimefilter   

@app.template_filter()
def no_recipients(block_hash):
   """Number of recepients in block"""    
   return block.get_no_recipients_block(block_hash)

app.jinja_env.filters['no_recipients'] = no_recipients

@app.template_filter()
def no_txes_block(block_hash):
   """Number of txes in block"""    
   return block.get_no_txes_block(block_hash)

app.jinja_env.filters['no_txes_block'] = no_txes_block

@app.template_filter()
def amount_block(block_hash):
   """Total amount in block"""    
   return block.get_amount_block(block_hash)

app.jinja_env.filters['amount_block'] = amount_block

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)