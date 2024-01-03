from bardapi import Bard
import os 


def get_api_key():
    file_path = os.getenv("BARD_API_TOKEN_FILE")

    try:
        with open(file_path, 'r') as file:
            api_token = file.read()

        return api_token.strip()

    except Exception as e:
        # Log or print the error if needed
        print(f"Error reading API token file: {e}")
        raise RuntimeError("Failed to read API token file")


def generate_ticket(ticket_title, api_key):

    prompt = f"Task title: {ticket_title}\n Generate a well scoped ticket"


    bard = Bard(token = api_key.strip())
    generated_details = bard.get_answer(prompt)['content']

    final_ticket = f"""
    **Task Scope:**
    Title: {ticket_title}
    Description: {generated_details}

    **Acceptance Criteria:**
    - Criteria 1
    - Criteria 2
    - ...

    **Sub-tasks:**
    - Sub-task 1
    - Sub-task 2
    - ...

    **Assumptions:**
    - Assumption 1
    - Assumption 2
    - ...

    **Additional Details:**
    {generated_details}
    """

    return final_ticket



if __name__ == "__main__":

    # Get input task title from the user
    task_title = input("Enter the title of the ticket: ")

    api_key = get_api_key()
    final_ticket = generate_ticket(task_title, api_key)

    # Print the generated task scope
    print(final_ticket)
