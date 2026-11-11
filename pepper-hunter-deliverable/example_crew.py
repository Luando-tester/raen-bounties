from crewai import Agent, Crew, Process, Task
from raen_tools import analyze_contract, draft_dispute_letter

# Define Agents
legal_analyst = Agent(
    role="Senior Legal Analyst",
    goal="Review contracts thoroughly and identify potential risks.",
    backstory="You are an expert corporate lawyer with years of contract review experience.",
    tools=[analyze_contract],
    verbose=True,
    memory=False
)

customer_advocate = Agent(
    role="Customer Advocacy Specialist",
    goal="Draft professional and forceful dispute letters to resolve billing issues.",
    backstory="You specialize in consumer protection and financial dispute resolution.",
    tools=[draft_dispute_letter],
    verbose=True,
    memory=False
)

# Define Tasks
contract_task = Task(
    description="Analyze the following contract excerpt for hidden liability clauses: {contract_excerpt}",
    expected_output="A structured breakdown of contract risks.",
    agent=legal_analyst
)

dispute_task = Task(
    description="Draft a dispute letter for account {account_id} regarding reason: {dispute_reason}.",
    expected_output="A formal dispute letter ready to be sent.",
    agent=customer_advocate
)

# Assemble Crew
raen_crew = Crew(
    agents=[legal_analyst, customer_advocate],
    tasks=[contract_task, dispute_task],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    inputs = {
        "contract_excerpt": "The vendor shall not be liable for any downtime exceeding 99.9% availability SLAs.",
        "account_id": "ACC-998877",
        "dispute_reason": "Unauthorized recurring monthly subscription fee."
    }
    
    print("## Starting RAEN CrewAI Automation Flow ##")
    result = raen_crew.kickoff(inputs=inputs)
    print("\n\n## Crew Execution Result ##")
    print(result)
