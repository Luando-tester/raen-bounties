# RAEN x402 CLI Client

A single-file Python CLI client for interacting with the 12-service x402 RAEN agent fleet, handling the 402 Payment Required handshake, signing payments, and printing settlement receipts.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Set your private key environment variable and run the CLI:

```bash
export RAEN_PRIVATE_KEY="your_hex_private_key_here"
python raen-cli.py echo "Hello, x402 fleet!"
```
