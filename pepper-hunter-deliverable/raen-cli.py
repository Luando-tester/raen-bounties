#!/usr/bin/env python3
"""
RAEN x402 Fleet CLI Client
Single-file Python CLI client that lists RAEN x402 services,
fires a paid call, handles the 402 payment loop, and prints receipts.
"""

import sys
import os
import json
import argparse
import requests
from ecdsa import SigningKey, SECP256k1

AGENTS_FILE = "agents.json"

def load_services():
    if not os.path.exists(AGENTS_FILE):
        print(f"Error: {AGENTS_FILE} not found.", file=sys.stderr)
        sys.exit(1)
    with open(AGENTS_FILE, "r") as f:
        data = json.load(f)
    return data.get("services", {})

def sign_payment(payload: dict, priv_key_hex: str) -> str:
    sk = SigningKey.from_string(bytes.fromhex(priv_key_hex), curve=SECP256k1)
    message = json.dumps(payload, sort_keys=True).encode("utf-8")
    signature = sk.sign(message)
    return signature.hex()

def call_service(service_name: str, prompt: str):
    services = load_services()
    if service_name not in services:
        print(f"Error: Service '{service_name}' not found in {AGENTS_FILE}.", file=sys.stderr)
        print(f"Available services: {', '.join(services.keys())}", file=sys.stderr)
        sys.exit(1)

    svc = services[service_name]
    url = svc["url"]
    price = svc["price_sats"]

    print(f"[*] Targeting service: {service_name} ({url})")
    print(f"[*] Price: {price} sats")
    print(f"[*] Sending initial request with prompt: '{prompt}'")

    headers = {"Content-Type": "application/json"}
    payload = {"prompt": prompt}

    # Initial request
    try:
        response = requests.post(url, json=payload, headers=headers)
    except requests.RequestException as e:
        print(f"Error connecting to service: {e}", file=sys.stderr)
        sys.exit(1)

    # Check for x402 Payment Required
    if response.status_code == 402:
        print("[*] Received 402 Payment Required.")
        challenge = response.json()
        invoice_id = challenge.get("invoice_id", "inv_mock_123")
        
        priv_key = os.environ.get("RAEN_PRIVATE_KEY")
        if not priv_key:
            # Fallback mock key for test runs if none provided
            priv_key = "1" * 64
            print("[!] Warning: RAEN_PRIVATE_KEY not set in environment. Using dummy key.")

        payment_payload = {
            "invoice_id": invoice_id,
            "amount_sats": price,
            "sender": "raen-cli-client"
        }
        sig = sign_payment(payment_payload, priv_key)

        payment_headers = headers.copy()
        payment_headers["X-402-Payment-Signature"] = sig
        payment_headers["X-402-Invoice-Id"] = invoice_id
        payment_headers["X-402-Amount"] = str(price)

        print("[*] Submitting payment proof...")
        response = requests.post(url, json=payload, headers=payment_headers)

    if response.status_code == 200:
        result = response.json()
        print("\n=== x402 SETTLEMENT RECEIPT ===")
        print(json.dumps(result, indent=2))
        print("================================")
    else:
        print(f"[-] Request failed with status {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="RAEN x402 Fleet CLI Client")
    parser.add_argument("service", nargs="?", help="Name of the service to call")
    parser.add_argument("prompt", nargs="?", help="Prompt to send to the service")
    parser.add_argument("--list", action="store_true", help="List all available services")

    args = parser.parse_args()

    if args.list or not args.service:
        services = load_services()
        print("Available RAEN x402 Services:")
        for name, details in services.items():
            print(f"  - {name}: {details['url']} ({details['price_sats']} sats)")
        if not args.service:
            sys.exit(0)

    if not args.prompt:
        print("Error: Prompt is required.", file=sys.stderr)
        sys.exit(1)

    call_service(args.service, args.prompt)

if __name__ == "__main__":
    main()
