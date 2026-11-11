# RAEN CrewAI Tool Wrappers

CrewAI `@tool` wrappers calling the RAEN MCP gateway to allow agents to draft dispute letters and analyze contracts within autonomous workflows.

## Features
- **Dispute Letter Tool**: Automatically drafts dispute letters via RAEN MCP gateway.
- **Contract Analysis Tool**: Analyzes agreements for high-risk clauses.
- **Ready-to-use Example**: Full CrewAI multi-agent script included.

## Installation

1. Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in a `.env` file:
```env
RAEN_MCP_URL=https://mcp.raen.ai/v1
RAEN_API_KEY=your_dev_key_here
```

## Running the Example

Execute the example CrewAI script:
```bash
python example_crew.py
```
