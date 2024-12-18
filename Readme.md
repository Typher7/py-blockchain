# To fetch the Blockchain 
curl http://127.0.0.1:5000/chain

# To mine/add a New Block
curl -X POST -H "Content-Type: application/json" -d '{"data":"New Block Data"}' http://127.0.0.1:5000/add_block
