# To fetch the Blockchain from the CLI

curl http://127.0.0.1:5000/chain

# To mine/add a New Block from the CLI

curl -X POST -H "Content-Type: application/json" -d '{"data":"New Block Data"}' http://127.0.0.1:5000/add_block

# This fixed the "port-binding" issues

port = int(os.getenv('PORT', 5000))

# The error suggests your app on Render isn't binding to the correct port. Flask defaults to port 5000, but Render expects you to bind to the port specified by the PORT environment variable.
