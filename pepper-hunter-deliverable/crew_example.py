import os
from crewai import Agent, Task, Crew, Process
from raen_crewai_tools import dispute_letter_tool, contract_analyze_tool


def main():
    # Set required environment variables
    # os.environ["RAEN_MCP_API_KEY"] = "your-raen-mcp-key"
    # os.environ["OPENAI_API_KEY"] = "your-openai-key"

    # Define Agent equipped with RAEN tools
    legal_specialist = Agent(
        role="Senior Legal Analyst",
        goal="Analyze contracts for legal risks and draft appropriate dispute letters.",
        backstory="You are an expert corporate legal consultant who leverages RAEN MCP tools to analyze agreements and enforce rights.",
        tools=[contract_analyze_tool, dispute_letter_tool],
        verbose=True
    )

    sample_contract = """
    SOFTWARE DEVELOPMENT AGREEMENT
    Vendor shall deliver the custom module by March 1, 2025. 
    In event of delay exceeding 14 days, Client may terminate immediately without compensation. 
    Vendor liability is capped at $500 regardless of breach impact.
    """

    # Task 1: Contract Analysis
    analysis_task = Task(
        description=f"Analyze the following contract snippet using the Contract Analyzer tool:\n{sample_contract}",
        expected_output="A list of legal risks and unbalanced terms found in the contract.",
        agent=legal_specialist
    )

    # Task 2: Draft Dispute Letter
    dispute_task = Task(
        description=(
            "Using the Dispute Letter Generator tool, draft a formal notice to 'Acme Tech Solutions' "
            "regarding late delivery of software modules past the agreed March 1 date."
        ),
        expected_output="A ready-to-send formal legal dispute letter.",
        agent=legal_specialist
    )

    crew = Crew(
        agents=[legal_specialist],
        tasks=[analysis_task, dispute_task],
        process=Process.sequential
    )

    print("=== Running CrewAI Flow with RAEN Tools ===")
    result = crew.kickoff()
    print("\n=== Final Result ===")
    print(result)


if __name__ == "__main__":
    main()
