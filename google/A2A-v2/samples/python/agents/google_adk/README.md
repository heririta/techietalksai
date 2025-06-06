## ADK Agent

This sample uses the Agent Development Kit (ADK) to create a simple "Expense Reimbursement" agent that is hosted as an A2A server.

This agent takes text requests from the client and, if any details are missing, returns a webform for the client (or its user) to fill out. After the client fills out the form, the agent will complete the task.

## Prerequisites

- Python 3.9 or higher
- UV
- Access to an LLM and API Key


## Running the Sample

1. Navigate to the samples directory:
    ```bash
    cd samples/python/agents/google_adk
    ```
2. Create an environment file with your API key:

   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

4. Run an agent:
    ```bash
    uv run .
    ```
5. Run one of the [client apps](/samples/python/hosts/README.md)