import os
import requests
from typing import Optional
from crewai.tools import tool

RAEN_MCP_GATEWAY_URL = os.getenv("RAEN_MCP_GATEWAY_URL", "https://gateway.raen.ai/v1")


def _call_raen_mcp(tool_name: str, arguments: dict) -> str:
    """Helper function to dispatch tool calls to RAEN MCP Gateway API."""
    api_key = os.getenv("RAEN_MCP_API_KEY")
    if not api_key:
        return "Error: RAEN_MCP_API_KEY environment variable is missing. Please set it before executing."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "tool": tool_name,
        "arguments": arguments
    }

    try:
        response = requests.post(
            f"{RAEN_MCP_GATEWAY_URL}/execute",
            json=payload,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data.get("result") or data.get("content") or str(data)
    except requests.exceptions.RequestException as e:
        return f"Error executing '{tool_name}' via RAEN MCP Gateway: {str(e)}"


@tool("RAEN Dispute Letter Generator")
def dispute_letter_tool(dispute_details: str, party_name: str, issue_summary: str) -> str:
    """Drafts a formal legal dispute letter using the RAEN MCP Gateway.

    Args:
        dispute_details: Comprehensive narrative or factual background of the dispute.
        party_name: Name of the opposing party or entity being addressed.
        issue_summary: Brief summary of key claims or requested remedies.
    """
    return _call_raen_mcp(
        tool_name="dispute_letter",
        arguments={
            "dispute_details": dispute_details,
            "party_name": party_name,
            "issue_summary": issue_summary
        }
    )


@tool("RAEN Contract Analyzer")
def contract_analyze_tool(contract_text: str, focus_areas: Optional[str] = "liabilities, indemnification, termination, key risks") -> str:
    """Analyzes legal contract text for legal risks, obligation clauses, and anomalies using RAEN MCP Gateway.

    Args:
        contract_text: Full text or key excerpt of the contract to analyze.
        focus_areas: Specific clauses or legal topics to focus analysis on.
    """
    return _call_raen_mcp(
        tool_name="contract_analyze",
        arguments={
            "contract_text": contract_text,
            "focus_areas": focus_areas
        }
    )
