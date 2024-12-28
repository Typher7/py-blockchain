# To fetch the Blockchain from the CLI

curl http://127.0.0.1:5000/chain

# To mine/add a New Block from the CLI

curl -X POST -H "Content-Type: application/json" -d '{"data":"New Block Data"}' http://127.0.0.1:5000/add_block

# This fixed the "port-binding" issues

port = int(os.getenv('PORT', 5000))

# The error suggests your app on Render isn't binding to the correct port. Flask defaults to port 5000, but Render expects you to bind to the port specified by the PORT environment variable.


# Blockchain Project

## Overview
This project implements a simple blockchain system in Python, paired with a React frontend. The blockchain supports basic functionality, such as creating blocks, verifying the chain, and adding transactions. It features a RESTful API built with Flask, enhanced with CORS for cross-origin compatibility. The React frontend communicates with the backend to display the blockchain data and interact with its functionality.

## Features
1. **Blockchain Core**
   - Genesis block initialization.
   - Block creation with hashing and proof-of-work.
   - Chain validation ensuring integrity and consistency.

2. **API Backend**
   - Developed using Flask.
   - Endpoints to fetch the chain, add transactions, and validate the blockchain.
   - JSON responses for easy integration with frontend systems.

3. **Frontend**
   - Built using React with Tailwind CSS for responsive UI.
   - Displays blockchain data in a paginated table format.
   - Fetches data from backend API hosted on Render.

4. **Security**
   - Blocks are signed and verified using RSA keys from the `cryptography` library.
   - Protects against tampering with individual blocks.

5. **Cross-Origin Support**
   - Enabled CORS in Flask to allow seamless communication with the React frontend.

## Installation

### Backend
1. Clone the repository:
   ```bash
   git init
   git clone https://github.com/Typher7/py-blockchain.git
   cd py-blockchain
   ```
2. Set up a Python virtual environment:
   ```bash
   python -m venv myblockchain
   source myblockchain/bin/activate # For Linux/Mac
   myblockchain\Scripts\activate   # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   python blockchain_api.py
   ```
   By default, the backend will run at `http://127.0.0.1:5000`.
   i.e port 5000 on localhost

### Frontend
1. Navigate to the `Frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run start
   ```
   By default, the frontend will run at `http://localhost:3000`.

## API Endpoints
### GET `/chain`
Fetches the entire blockchain.

### POST `/add_transaction`
Adds a single transaction to the blockchain.
- **Body Parameters**:
  - `data`: The transaction data (string).
  - `private_key`: The RSA private key for signing.

### POST `/add_transactions`
Adds multiple transactions to the blockchain.
- **Body Parameters**:
  - `data`: List of transaction data (array of strings).
  - `private_key`: The RSA private key for signing.

### POST `/validate`
Validates the blockchain using the provided public key.
- **Body Parameters**:
  - `public_key`: The RSA public key for verification.

## Folder Structure
```
project-root
├── backend
│   ├── blockchain.py         # Core blockchain logic
│   ├── blockchain_api.py     # Flask app for API endpoints
│   ├── chain.json            # Persistent storage for the chain
│   └── requirements.txt      # Backend dependencies
├── frontend
│   ├── src
│   │   ├── components
│   │   │   ├── BlockchainViewer.jsx  # Component to display blockchain data
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## Deployment
### Backend
1. Deploy the Flask backend to a hosting service like [Render](https://render.com) or [Heroku](https://www.heroku.com).
2. Ensure `chain.json` is included in the deployment.
3. Add necessary environment variables for production.

### Frontend
1. Build the React frontend:
   ```bash
   npm run build
   ```
2. Deploy the `build` directory to a service like [Netlify](https://www.netlify.com) or [Vercel](https://vercel.com).
3. Update the API endpoint URLs in the React code to point to the live backend.

## Future Enhancements
- Add user authentication for transaction signing.
- Improve frontend UI for better visualization.
- Implement real-time updates using WebSockets.
- Add smart contract functionality.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements
- [Flask](https://flask.palletsprojects.com/)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Render](https://render.com/) for backend hosting.

