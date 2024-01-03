import os 
import json
from jira import JIRA
from bardapi import Bard

# TODO: add type alias for each input 
# TODO: add comments

def get_api_key():
    file_path = os.getenv("BARD_API_TOKEN_FILE")

    try:
        with open(file_path, 'r') as file:
            api_token = file.read()

        return api_token.strip()

    except Exception as e:
        print(f"Error reading API token file: {e}")
        raise RuntimeError("Failed to read API token file")


def get_jira_credentials():
    file_path = os.getenv("JIRA_CREDENTIALS_FILE")

    try:
        with open(file_path, 'r') as file:
            credentials = json.load(file)
        return credentials

    except Exception as e:
        print(f"Error reading jira credentials: {e}")
        raise RuntimeError("Failed to read jira credentials")


def generate_ticket(ticket_title, api_key):

    prompt = f"Task title: {ticket_title}\n Generate a well scoped ticket"

    bard = Bard(token = api_key.strip())
    generated_details = bard.get_answer(prompt)['content']

    final_ticket = f"""
    h2. Task Scope:
    Description: {generated_details}

    h2. Acceptance Criteria:
    - Criteria 1
    - Criteria 2
    - ...

    h2. Sub-tasks:
    - Sub-task 1
    - Sub-task 2
    - ...

    h2. Assumptions:
    - Assumption 1
    - Assumption 2
    - ...
    """


    return final_ticket


def upload_ticket_jira(credentials, ticket):
    jira = JIRA(options = {"server": credentials["server"]}, basic_auth=(credentials["email_address"] ,credentials["token"])) 

    issue_dict = {
    'project': {'key': credentials["key"]},
    'summary': 'Testing issue from Python Jira Handbook',
    'description': f'{ticket}',
    'issuetype': {'name': 'Task'},
    }

    try:
        jira.create_issue(fields=issue_dict)
        print(f"Jira issue successfully created and uploaded")
    except Exception as e:
        print(f"Failed to create Jira issue. Error: {str(e)}")


if __name__ == "__main__":

    api_key = get_api_key()
    credentials = get_jira_credentials()
    print("Server:", credentials["server"])
    print("Email Address:", credentials["email_address"])
    print("Token:", credentials["token"])
    print("Key:", credentials["key"])
    # Get input task title from the user
    task_title = input("Enter the title of the ticket: ")
    
    final_ticket = generate_ticket(task_title, api_key)

    # Print the generated task scope
    print(final_ticket)

    upload_ticket_jira(credentials, final_ticket)



