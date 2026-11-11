import os
import requests
from crewai.tools import tool

# Configuration for RAEN MCP Gateway
RAEN_MCP_URL = os.getenv("RAEN_MCP_URL", "https://mcp.raen.ai/v1")
RAEN_API_KEY = os.getenv("RAEN_API_KEY", "")

def _call_gateway(endpoint: str, payload: dict) -> str:
    headers = {
        "Authorization": f"Bearer {RAEN_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(f"{RAEN_MCP_URL}/{endpoint}", json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return str(response.json())
    except requests.exceptions.RequestException as e:
        return f"Error communicating with RAEN MCP gateway: {str(e)}"

@tool("Draft Dispute Letter")
def draft_dispute_letter(dispute_reason: str, account_id: str, transaction_details: str) -> str:
    """
    Drafts a formal financial dispute letter using the RAEN MCP gateway.
    Args:
        dispute_reason (str): The reason for the dispute (e.g., unauthorized charge).
        account_id (str): The user account identifier.
        transaction_details (str): Details regarding the disputed transaction.
    """
    payload = {
        "account_id": account_id,
        "dispute_reason": dispute_reason,
        "transaction_details": transaction_details
    }
    return _call_gateway("dispute_letter", payload)

@tool("Analyze Contract")
def analyze_contract(contract_text: str, focus_areas: str) -> str:
    """
    Analyzes a legal contract for risks and terms using the RAEN MCP gateway.
    Args:
        contract_text (str): The full text or excerpt of the contract.
        focus_areas (str): Specific clauses or risks to look out for.
    """
    payload = {
        "contract_text": contract_text,
        "focus_areas": focus_areas
    }
    return _call_gateway("contract_analyze", payload)
