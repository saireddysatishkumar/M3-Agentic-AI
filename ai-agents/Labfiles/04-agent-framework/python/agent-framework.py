import os
import asyncio
from pathlib import Path

# Add references
from agent_framework import AgentThread, ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from pydantic import Field
from typing import Annotated
from dotenv import load_dotenv
from azure.identity import AzureCliCredential

load_dotenv()  # make sure .env values are available

AZURE_AI_PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
AZURE_AI_MODEL_DEPLOYMENT_NAME = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")


async def main():
    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load the expnses data file
    script_dir = Path(__file__).parent
    file_path = script_dir / 'data.txt'
    with file_path.open('r') as file:
        data = file.read() + "\n"

    # Ask for a prompt
    user_prompt = input(f"Here is the expenses data in your file:\n\n{data}\n\nWhat would you like me to do with it?\n\n")
    
    # Run the async agent code
    await process_expenses_data (user_prompt, data)
    
async def process_expenses_data(prompt, expenses_data):
    # Create the credential
    credential = AzureCliCredential()
    # Create a chat agent
    async with ChatAgent(
        chat_client=AzureAIAgentClient(
            credential=credential,
            project_endpoint=AZURE_AI_PROJECT_ENDPOINT,
            model_deployment_name=AZURE_AI_MODEL_DEPLOYMENT_NAME,
        ),
        name="expenses_agent",
        instructions="""You are an AI assistant for expense claim submission.
                        When a user submits expenses data and requests an expense claim, use the plug-in function to send an email to expenses@contoso.com with the subject 'Expense Claim`and a body that contains itemized expenses with a total.
                        Then confirm to the user that you've done so.""",
        tools=send_email,
    ) as agent:


        # Use the agent to process the expenses data    
        try:
            # Add the input prompt to a list of messages to be submitted
            prompt_messages = [f"{prompt}: {expenses_data}"]
            # Invoke the agent for the specified thread with the messages
            response = await agent.run(prompt_messages)
            # Display the response
            print(f"\n# Agent:\n{response}")
        except Exception as e:
            # Something went wrong
            print (e)


# Create a tool function for the email functionality
def send_email(
to: Annotated[str, Field(description="Who to send the email to")],
subject: Annotated[str, Field(description="The subject of the email.")],
body: Annotated[str, Field(description="The text body of the email.")]):
    print("\nTo:", to)
    print("Subject:", subject)
    print(body, "\n")



if __name__ == "__main__":
    asyncio.run(main())
