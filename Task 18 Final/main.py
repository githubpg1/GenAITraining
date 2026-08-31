# Main entry point for the Ticket Intelligence System

from orchestrator.orchestrator import Orchestrator
import json

def main():
    # Initialize the orchestrator
    orchestrator = Orchestrator()
    
    # Example user query (in a real system, this would come from user input)
    user_query = "Which customers had the same login issue as ticket 4021, and did any of them churn afterward?"
    
    # Execute the query
    result = orchestrator.execute(user_query)
    
    # Print the result as JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()